#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:21:11 2019

@author: theo_taupiac

Reminder :
    lancer data_reconstruction ET creation features en amont
    -> travaille sur le fichier 10ms, données avec duplicate.drop
    
    Ajouter le GPS POUR plane_TURNING, au lieu de AHRS_HEADING (pour cela, prochaine data, bonnes features)
    
    Calculer les frequences de tourner la tete
"""

###############################################################################
#########################        IMPORTS          #############################
###############################################################################

import pandas as pd
import numpy as np
#%matplotlib inline
import matplotlib.pyplot as plt
import time

###############################################################################
#########################       PARAMETRES       ##############################
###############################################################################
threshold_turn = 4
threshold_turn_head = 3

###############################################################################
#########################       CODE PRELIM       #############################
###############################################################################

exec(open("/Users/theo_taupiac/Desktop/PIE_0018/creation_features.py").read()) 

DataMove = pd.DataFrame( columns = ['turning_plane','turning_head'])


###############################################################################
############################     FONCTIONS     ################################
###############################################################################

### AVEC LE LACET POUR LINSTANT !! PROCHAINE MESURE BIEN CHOISIR LES DATA DANS 100ms
# Donne la direction du virage a chaque instant du vol.

def plane_turning(threshold_turn, df):
    
    roulis = df.loc[:,["FD_AHRS_ROLL"]]
    cap = df.loc[:,["FD_AHRS_HEADING"]]
    cap_time = df.loc[:,["FD_TIME_MS"]]
    
    for t in range(threshold_turn, len(df)-threshold_turn):
        
        roulis_current = roulis.iloc[t-threshold_turn:t+threshold_turn]
        cap_current = cap.iloc[t-threshold_turn:t+threshold_turn]
        cap_current_time = cap_time.iloc[t-threshold_turn:t+threshold_turn]
        
        moyenne_roulis = roulis_current.mean().FD_AHRS_ROLL
        
        vect = cap_current.FD_AHRS_HEADING.values
        vect_time = cap_current_time.FD_TIME_MS.values
        
        deriv=[]
        for k in range(len(vect)-1):
            u=(vect[k+1]-vect[k])*1000/(vect_time[k+1]-vect_time[k])
            deriv.append(abs(u))
    
        moyenne_deriv_cap = np.mean(deriv)

        if (moyenne_roulis <= -15) & (moyenne_deriv_cap >= 2) :
            DataMove.loc[t,'turning_plane'] = "<<<------"
            
        elif (moyenne_roulis >= 15) & (moyenne_deriv_cap >= 2) :
            DataMove.loc[t,'turning_plane'] = "------>>>"
        else:
            DataMove.loc[t,'turning_plane'] = "^^^"
    return(DataMove)



def head_turning(threshold_turn_head, df):
    cap_head = df.loc[:,["FD_PILOT_HEAD_HEADING"]]
    #cap_head_time = df.loc[:,["FD_TIME_MS"]]
    
    for t in range(len(df)):
           
           if (cap_head.iloc[t].values <= -10) :
                DataMove.loc[t,'turning_head'] = "<<<------"
            
           elif (cap_head.iloc[t].values >= 10) :
                DataMove.loc[t,'turning_head'] = "------>>>"
                
           else:
                DataMove.loc[t,'turning_head'] = "^^^"
    return(DataMove)
    
    
plane_turning(threshold_turn, dataFlight)
head_turning(threshold_turn_head, dataFlight)