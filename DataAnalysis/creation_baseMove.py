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

head_turn_value = 10 ### A PARAMETRER EN FONCTION DE LA CROIX
plane_turn_value = 15 ### IDEM
derive_cap = 2
###############################################################################
#########################       CODE PRELIM       #############################
###############################################################################

exec(open("/Users/theo_taupiac/Desktop/PIE_0018/creation_features.py").read()) 

DataMove = pd.DataFrame( columns = ['turning_plane','turning_head'])


###############################################################################
############################     FONCTIONS     ################################
###############################################################################

### AVEC LE LACET POUR LINSTANT (FD_AHRS_HEADING)!! PROCHAINE MESURE BIEN CHOISIR LES DATA DANS 100ms
# Donne la direction du virage a chaque instant du vol.

"""
S'applique aux data de XPlane. Donne la direction du virage a chaque instant du vol. parametres a choisir ci-dessus (next update)
"""



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

        if (moyenne_roulis <= - plane_turn_value) & (moyenne_deriv_cap >= derive_cap) :
            DataMove.loc[t,'turning_plane'] = -1
            #"<<<------"
            
        elif (moyenne_roulis >= plane_turn_value) & (moyenne_deriv_cap >= derive_cap) :
            DataMove.loc[t,'turning_plane'] = 1
            #"------>>>"
        else:
            DataMove.loc[t,'turning_plane'] = 0
            #"^^^"
    return(DataMove)


"""
S'applique aux data de XPlane. Donne les instants ou la tête tourne a droite ou a gauche. head_turn_value reglee avec la croix (next update)
"""
def head_turning(df):
    cap_head = df.loc[:,["FD_PILOT_HEAD_HEADING"]]
    #cap_head_time = df.loc[:,["FD_TIME_MS"]]
    
    for t in range(len(df)):
           
           if (cap_head.iloc[t].values <= -head_turn_value) :
                DataMove.loc[t,'turning_head'] = -1
                #"<<<------"
            
           elif (cap_head.iloc[t].values >= head_turn_value) :
                DataMove.loc[t,'turning_head'] =  1
                #"------>>>"
                
           else:
                DataMove.loc[t,'turning_head'] = 0
                #"^^^"
    return(DataMove)
    
  
    
"""
S'applique directement à Datamove. grce aux data crees par les deux fonctions precedentes.
Donne la frequence de tournee de tete pendant le virage.

PAS D'ORIENTATION POUR L'INSTANT
"""    
def freq_head_turning(dm):
    nb_virage = 0
    nb_turn = 0
    
    turning_plane = []
    turning_head = []
    
    turn_plane = dm.loc[:,["turning_plane"]]
    turn_head = dm.loc[:,["turning_head"]]
    
    
    for t in range(len(dm)-1):
        
        # NOUVEAU VIRAGE
        if abs(turn_plane.iloc[t+1].values) == 1 and turn_plane.iloc[t].values == 0:
            turning_plane.append(1)
            
            if abs(turn_head.iloc[t+1].values) == 1 :
                turning_head.append([1])
            else :
                turning_head.append([0])
                
        # VIRAGE QUI CONTINUE
        if abs(turn_plane.iloc[t+1].values) == 1 and turn_plane.iloc[t].values == 1:
            turning_plane[nb_virage] += 1
            
            # LISTE DANS LA LISTE CONCERNANT LE VIRAGE EN COURS
            if abs(turn_head.iloc[t+1].values) == 1 and turn_head.iloc[t].values == 1:
                turning_head[nb_virage][nb_turn] += 1
            if abs(turn_head.iloc[t+1].values) == 1 and turn_head.iloc[t].values == 0:
                nb_turn += 1
                turning_head[nb_virage].append(1)
                
        # FIN DE VIRAGE
        if turn_plane.iloc[t+1].values == 0 and abs(turn_plane.iloc[t].values) == 1 : 
            nb_virage += 1

    Frequence_tete = []
    
    #une valeur toutes les 0.1sec dans le tableau
    
    for k in range(len(turning_head)):
        Frequence_tete.append(100*len(turning_head[k])/turning_plane[k])


    print("La premiere valeur est le nombre de virages, le premier tableau correspond a chacune de leur duree, le dernier au temps ou la tete est tournee. La derniere valeur correspond au ratio des deux dernieres")
    return(nb_virage,turning_plane,turning_head,Frequence_tete) 
    
#turning_plane,turning_head)    
    
    
    
###############################################################################
######################          TEST FONCTION          ########################  
###############################################################################
    
plane_turning(threshold_turn, dataFlight)
head_turning(dataFlight)
freq_head_turning(DataMove)


### A CODER changement dinclinaison precede d'un regard (DEBUT ET FIN VIRAGE)