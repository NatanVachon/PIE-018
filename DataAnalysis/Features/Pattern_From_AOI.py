# -*- coding: utf-8 -*-
"""
This file deals with AOI pattern recognition for an interpretation purpose.
"""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       IMPORTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import Constants as const
import pandas as pd
import numpy as np

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def clean_AOI(full_pd, seuil):
    """
    This function will compress all the data to keep only the first row for each AOI, allowing to detect patterns after

    Parameters
    ----------
    full_pd : TYPE
        DESCRIPTION.
    seuil : TYPE
        DESCRIPTION.

    Returns
    -------
    clean : TYPE
        DESCRIPTION.

    """
    full_pd=full_pd.copy(deep=True)
    clean = full_pd.loc[(full_pd.loc[:,"AOI"].shift() != full_pd.loc[:,"AOI"])].copy(deep=True)
    clean.loc[:,"delta"]=(-clean["FD_TIME_S"]+clean["FD_TIME_S"].shift(-1)).fillna(0)
    clean=clean.loc[(clean["delta"]>seuil)]

    clean.reset_index(drop=True,inplace=True)
    return clean




def count_transitions(AOI_pd):
    """


    Parameters
    ----------
    AOI_pd : TYPE
        DESCRIPTION.

    Returns
    -------
    pivot : TYPE
        DESCRIPTION.
    transition : TYPE
        DESCRIPTION.

    """
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
    transition.drop(columns=["AOI","FD_TIME_S","next_AOI","average_time_aft","prev_AOI","prev_transition"],inplace=True)
    return pivot,transition




def tete_fixe_tunnel(aois,t1,t2):
    """


    Parameters
    ----------
    aois : TYPE
        DESCRIPTION.
    t1 : TYPE
        DESCRIPTION.
    t2 : TYPE
        DESCRIPTION.

    Returns
    -------
    fixe : TYPE
        DESCRIPTION.

    """
    ref=aois.loc[t1,"AOI"]
    fixe=(aois.loc[aois.loc[:, "FD_TIME_S"]<t2].loc[aois.loc[:, "FD_TIME_S"]>t1,"AOI"]==ref).all()
    return fixe


def tete_fixe(data,t1,t2,seuil=const.SEUIL_TETE_FIXE):
    """


    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    t1 : TYPE
        DESCRIPTION.
    t2 : TYPE
        DESCRIPTION.
    seuil : TYPE, optional
        DESCRIPTION. The default is const.SEUIL_TETE_FIXE.

    Returns
    -------
    fixe : TYPE
        DESCRIPTION.

    """
    local=data.loc[data["FD_TIME_S"]<t2].loc[data["FD_TIME_S"]>t1,["FD_PILOT_HEAD_HEADING","FD_PILOT_HEAD_PITCH"]]
    mean=local.mean()
    fixe=((abs(local-mean)>seuil).all()).all()
    return fixe

def count_AOI(AOI_pd,full_pd):
    """


    Parameters
    ----------
    AOI_pd : TYPE
        DESCRIPTION.
    full_pd : TYPE
        DESCRIPTION.

    Returns
    -------
    AOI : TYPE
        DESCRIPTION.

    """
    AOI=AOI_pd.drop_duplicates(subset="AOI").sort_values("AOI").set_index("AOI")
    AOI["count"]=0
    AOI["average_time"]=0
    AOI["total_time"]=0
    AOI["%_time"]=0
    total_time=full_pd["FD_TIME_S"].max()-full_pd["FD_TIME_S"].min()

    for a in AOI.index:
        AOI.loc[a,"count"]=AOI_pd.loc[a==AOI_pd["AOI"]].count()["AOI"]
        AOI.loc[a,"average_time"]=AOI_pd.loc[a==AOI_pd["AOI"],"delta"].mean()
        AOI.loc[a,"total_time"]=AOI_pd.loc[a==AOI_pd["AOI"],"delta"].sum()
    AOI.loc[:,"%_time"]=(100*AOI["total_time"]/total_time).astype(int)
    return AOI




def chain_AOI(pivot,liste_aoi):
    """


    Parameters
    ----------
    pivot : TYPE
        DESCRIPTION.
    liste_aoi : TYPE
        DESCRIPTION.

    Returns
    -------
    aoi_chain : TYPE
        DESCRIPTION.

    """
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