# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:13:43 2020

@author: Simon
"""

import pandas as pd
import numpy as np
#%matplotlib inline
import matplotlib.pyplot as plt
import time

#This function will compress all the data to keep only the first row for each AOI, allowing to detect patterns after
def clean_AOI(full_pd,seuil):
    seuil=seuil #minimal number of ms to consider we were in this AOI    
    cols=["Timestamp","AOI","AHRS"]#columns to keep
    clean = full_pd.loc[(full_pd["AOI"].shift() != full_pd["AOI"])]
    clean["delta"]=(-clean["timestamp"]+clean["timestamp"].shift(-1)).fillna(0)
    clean=clean.loc[(clean["delta"]>seuil)]
    
    clean.reset_index(drop=True,inplace=True)
    return clean




def count_transitions(AOI_pd):
    AOI_pd["next_AOI"]=AOI_pd["AOI"].shift(-1).fillna("0")
    AOI_pd["prev_AOI"]=AOI_pd["AOI"].shift(1).fillna("0")

    AOI_pd["transition"]=AOI_pd["AOI"]+"=>"+AOI_pd["next_AOI"]
    AOI_pd["prev_transition"]=AOI_pd["prev_AOI"]+"=>"+AOI_pd["AOI"]
    AOI=AOI_pd.drop_duplicates(subset="AOI").sort_values("AOI").set_index("AOI")

    transition=AOI_pd.drop_duplicates(subset="transition").sort_values("transition").set_index("transition")
    transition["count"]=0
    transition["average_time_bef"]=0
    transition["average_time_aft"]=0
    transition["%from"]=0 # Depuis l'AOI de départ, % de fois ou on arrive à AOI arrivé
    transition["%to"]=0  # D'ou vient on depuis cet AOI d'arrivé


    for a in transition.index:
        AOI1=transition["AOI"].loc[a]
        AOI2=transition["next_AOI"].loc[a]
        transition["count"].loc[a]=AOI_pd.loc[a==AOI_pd["transition"]].count()["transition"]
        transition["average_time_bef"].loc[a]=AOI_pd["delta"].loc[a==AOI_pd["transition"]].mean()
        transition["average_time_aft"].loc[a]=AOI_pd["delta"].loc[a==AOI_pd["prev_transition"]].mean()
        transition["%from"].loc[a]=int((100*transition["count"].loc[a]/AOI_pd.loc[AOI_pd["AOI"]==AOI1].count()["AOI"]))
        transition["%to"].loc[a]=int((100*transition["count"].loc[a]/AOI_pd.loc[AOI_pd["next_AOI"]==AOI2].count()["next_AOI"]))

    ind=[a for a in AOI.index]
    col=ind.copy()
    col.append("0")
    pivot=pd.DataFrame(index=col,columns=ind)
    pivot.fillna(0,inplace=True)
    for i in ind:
        for j in col:
            a=i+"=>"+j
            
            if a in transition.index:
                pivot.loc[j,i]=transition["%from"].loc[a]
    pivot=pivot.astype(int)  
    transition.drop(columns=["AOI","timestamp","next_AOI","average_time_aft","prev_AOI","prev_transition"],inplace=True)
    return pivot,transition
            
                
   

def count_AOI(AOI_pd,full_pd):
    AOI=AOI_pd.drop_duplicates(subset="AOI").sort_values("AOI").set_index("AOI")
    AOI["count"]=0
    AOI["average_time"]=0
    AOI["total_time"]=0
    AOI["%_time"]=0
    total_time=full_pd["timestamp"].max()-full_pd["timestamp"].min()
    
    for a in AOI.index:
        AOI["count"].loc[a]=AOI_pd.loc[a==AOI_pd["AOI"]].count()["AOI"]
        AOI["average_time"].loc[a]=AOI_pd["delta"].loc[a==AOI_pd["AOI"]].mean()
        AOI["total_time"].loc[a]=AOI_pd["delta"].loc[a==AOI_pd["AOI"]].sum()
    AOI["%_time"]=(100*AOI["total_time"]/total_time).astype(int)
    return AOI
