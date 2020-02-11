# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:13:43 2020

@author: Simon
"""

import pandas as pd
import numpy as np
#This function will compress all the data to keep only the first row for each AOI, allowing to detect patterns after
def clean_AOI(full_pd, seuil):
    cols=["Timestamp","AOI","AHRS"]#columns to keep
    full_pd=full_pd.copy(deep=True)
    clean = full_pd.loc[(full_pd.loc[:,"AOI"].shift() != full_pd.loc[:,"AOI"])].copy(deep=True)
    clean.loc[:,"delta"]=(-clean["timestamp"]+clean["timestamp"].shift(-1)).fillna(0)
    clean=clean.loc[(clean["delta"]>seuil)]

    clean.reset_index(drop=True,inplace=True)
    return clean




def count_transitions(AOI_pd):
    AOI_pd["next_AOI"]=AOI_pd.loc[:,"AOI"].shift(-1,fill_value="0")
    AOI_pd["prev_AOI"]=AOI_pd["AOI"].shift(1,fill_value="0")
    AOI_pd["transition"]=AOI_pd["AOI"]+"=>"+AOI_pd["next_AOI"]
    AOI_pd["prev_transition"]=AOI_pd["prev_AOI"]+"=>"+AOI_pd["AOI"]

    AOI=AOI_pd.drop_duplicates(subset="AOI").sort_values("AOI").set_index("AOI")
   
    transition=AOI_pd.drop_duplicates(subset="transition").sort_values("transition").set_index("transition")
    transition.loc[:,"count"]=0
    transition.loc[:,"average_time_bef"]=0
    transition.loc[:,"average_time_aft"]=0
    transition.loc[:,"%from"]=0 # Depuis l'AOI de départ, % de fois ou on arrive à AOI arrivé
    transition.loc[:,"%to"]=0  # D'ou vient on depuis cet AOI d'arrivé
    transition.loc[:,"%count"]=0

    for a in transition.index:
        AOI1=transition.loc[a,"AOI"]
        AOI2=transition.loc[a,"next_AOI"]
        transition.loc[a:,"count"]=AOI_pd.loc[a==AOI_pd["transition"]].count()["transition"]
        transition.loc[a:,"average_time_bef"]=AOI_pd.loc[a==AOI_pd["transition"],"delta"].mean()
        transition.loc[a:,"average_time_aft"]=AOI_pd.loc[a==AOI_pd["prev_transition"],"delta"].mean()
        transition.loc[a,"%from"]=int((100*transition.loc[a,"count"]/AOI_pd.loc[AOI_pd["AOI"]==AOI1].count()["AOI"]))
        transition.loc[a,"%to"]=int((100*transition.loc[a,"count"]/AOI_pd.loc[AOI_pd["next_AOI"]==AOI2].count()["next_AOI"]))
    for b in transition.index:
        transition.loc[b,"%count"]=int((100*transition.loc[b,"count"]/transition["count"].sum()))
    
    ind=[a for a in AOI.index]
    col=ind.copy()
    col.append("0")
    pivot=pd.DataFrame(index=col,columns=ind)
    pivot.fillna(0,inplace=True)
    for i in ind:
        for j in col:
            a=i+"=>"+j

            if a in transition.index:
                pivot.loc[j,i]=transition.loc[a,"%from"]
    pivot=pivot.astype(int)
    transition.drop(columns=["AOI","timestamp","next_AOI","average_time_aft","prev_AOI","prev_transition"],inplace=True)
    return pivot,transition




def tete_fixe_tunnel(aois,t1,t2):
    ref=aois.loc[t1,"AOI"]
    fixe=(aois.loc[aois.loc["FD_TIME_MS"]<t2].loc[aois.loc["FD_TIME_MS"]>t1,"AOI"]==ref).all
    return fixe


def tete_fixe(data,t1,t2,seuil=5):
    local=data.loc[data["FD_TIME_MS"]<t2].loc[data["FD_TIME_MS"]>t1,["FD_PILOT_HEAD_HEADING","FD_PILOT_HEAD_PITCH"]]
    mean=local.mean()
    fixe=((abs(local-mean)>seuil).all()).all()
    return fixe

def count_AOI(AOI_pd,full_pd):
    AOI=AOI_pd.drop_duplicates(subset="AOI").sort_values("AOI").set_index("AOI")
    AOI["count"]=0
    AOI["average_time"]=0
    AOI["total_time"]=0
    AOI["%_time"]=0
    total_time=full_pd["timestamp"].max()-full_pd["timestamp"].min()

    for a in AOI.index:
        AOI.loc[a,"count"]=AOI_pd.loc[a==AOI_pd["AOI"]].count()["AOI"]
        AOI.loc[a,"average_time"]=AOI_pd.loc[a==AOI_pd["AOI"],"delta"].mean()
        AOI.loc[a,"total_time"]=AOI_pd.loc[a==AOI_pd["AOI"],"delta"].sum()
    AOI.loc[:,"%_time"]=(100*AOI["total_time"]/total_time).astype(int)
    return AOI




def chain_AOI(pivot,liste_aoi):
    aois=pivot.index.copy().to_numpy()
    liste_aois="".join(liste_aoi)
    aoi_chain=pd.DataFrame(columns=["count"])    
    for i in aois:
        for j in np.delete(aois,np.where(aois==i)):
            if liste_aois.count(i+j)>0:
                for k in np.delete(aois,np.where(aois==j)):
                    if liste_aois.count(i+j+k)>0:
                        temp=liste_aois.count(i+j+k)
                        if temp>0 :
                            aoi_chain.loc[i+j+k,"count"]=temp
            
    aoi_chain["pourcent"]=100*aoi_chain.loc[:,"count"]/aoi_chain["count"].sum()
    aoi_chain=aoi_chain.loc[aoi_chain["pourcent"]>1]
    return aoi_chain


#d'une fonction qui marche entre t1 et t2 est appelée 
def cont(fonction,data,nom,seuil):
    true=[]
    seuil_cherche=seuil/2
    tr=False
    maxt=max(data["FD_TIME_MS"])-seuil_cherche
    ta=min(data["FD_TIME_MS"])
    while ta<=maxt :
        tb=ta+seuil_cherche
        
        trprec=tr
        tr=fonction(data,ta,tb,seuil_cherche)
        
        if tr:
            true.append((ta,tb))
        ta=ta+seuil_cherche    
    true2=[]
    i=0
    for while i<=len(true)-1:
        if true[i][1]==true[i+1][0]:
            true2.append((true[i][0],true[i+1][1]))
            i+=1
    return true2


def cont(fonction,data,nom,seuil=0.5):
    true=[]
    seuil_cherche=seuil
    tr=False
    maxt=max(data["FD_TIME_MS"])-seuil_cherche
    ta=min(data["FD_TIME_MS"])
    while ta<=maxt :
        tb=ta+seuil_cherche
        
        trprec=tr
        tr=fonction(data,ta,tb,seuil_cherche)
        
        if tr:
            true.append((ta,tb))
        ta=ta+seuil_cherche    
   
    return true