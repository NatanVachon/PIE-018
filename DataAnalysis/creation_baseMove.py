#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:21:11 2019

@author: theo_taupiac

Reminder :
    
    plane_turning :
        
    s'adapter par rapport a la croix pour head turn
    preciser les virages pas bien engagés
    aller voir avant et apres virage av ion, si la tete tourne
    
    !!!!! difference de time stamp pour duree virage
    
    
    Calculer les frequences de tourner la tete
"""

###############################################################################
#########################        IMPORTS          #############################
###############################################################################

import pandas as pd
import numpy as np
#%matplotlib inline

###############################################################################
#########################       PARAMETRES       ##############################
###############################################################################

threshold_turn = 4
head_turn_value = 10 ### A PARAMETRER EN FONCTION DE LA CROIX
plane_turn_value = 15
derive_cap = 1

###############################################################################
#########################       CODE PRELIM       #############################
###############################################################################

#DataMove = pd.DataFrame(columns = ['turning_plane','turning_head'])

###############################################################################
############################     FONCTIONS     ################################
###############################################################################


# Donne la direction du virage a chaque instant du vol.

"""
S'applique aux data de XPlane. Donne la direction du virage a chaque instant du vol. parametres a choisir ci-dessus (next update)
+++
Donne les instants ou la tête tourne a droite ou a gauche. head_turn_value reglee avec la croix (next update)
"""

def plane_and_head_turning(df):
    
    DataMove = pd.DataFrame(columns = ['turning_plane','turning_head'])
    
    ######### CODE PLANE_TURNING      
    
    roulis = df.loc[:,["FD_AHRS_ROLL"]]
    #cap = df.loc[:,["FD_AHRS_HEADING"]]
    cap = df.loc[:,["FD_GPS_COURSE"]]
    cap_time = df.loc[:,["FD_TIME_MS"]]
    cap_head = df.loc[:,["FD_PILOT_HEAD_HEADING"]]
    #cap_head_time = df.loc[:,["FD_TIME_MS"]]
    
    
    for t in range(threshold_turn, len(df)-threshold_turn):
        
        roulis_current = roulis.iloc[t-threshold_turn:t+threshold_turn]
        cap_current = cap.iloc[t-threshold_turn:t+threshold_turn]
        cap_current_time = cap_time.iloc[t-threshold_turn:t+threshold_turn]
        
        moyenne_roulis = roulis_current.mean().FD_AHRS_ROLL
        
        #vect = cap_current.FD_AHRS_HEADING.values
        vect = cap_current.FD_GPS_COURSE.values
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
              
    ######### CODE HEAD_TURNING             
    
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
    turn_side = []
    nb_turn = 0
    
    turning_plane = []
    turning_head = []
    
    turn_plane = dm.loc[:,["turning_plane"]]
    turn_head = dm.loc[:,["turning_head"]]
    
    
    for t in range(len(dm)-1):
        
        # NOUVEAU VIRAGE
        if abs(turn_plane.iloc[t+1].values) == 1 and turn_plane.iloc[t].values == 0:
            turning_plane.append(1)
            
            if turn_head.iloc[t+1].values == 1 :
                turning_head.append([1])
                
            if turn_head.iloc[t+1].values == -1 :
                turning_head.append([-1])  
                
            if turn_head.iloc[t+1].values == 0 :
                turning_head.append([0])
                
        # VIRAGE QUI CONTINUE
        if abs(turn_plane.iloc[t+1].values) == 1 and abs(turn_plane.iloc[t].values) == 1:
            turning_plane[nb_virage] += 1
            
            # TETE A DROITE
            if turn_head.iloc[t+1].values == 1 and turn_head.iloc[t].values == 1:
                turning_head[nb_virage][nb_turn] += 1
            if turn_head.iloc[t+1].values == 1 and turn_head.iloc[t].values != 1 :
                nb_turn += 1
                turning_head[nb_virage].append(1)

                
             # TETE A GAUCHE
            if turn_head.iloc[t+1].values == -1 and turn_head.iloc[t].values == -1:
                turning_head[nb_virage][nb_turn] -= 1
            if turn_head.iloc[t+1].values == -1 and turn_head.iloc[t].values != -1 :
                nb_turn += 1
                turning_head[nb_virage].append(-1)   
                
                
                
        # FIN DE VIRAGE
        if turn_plane.iloc[t+1].values == 0 and abs(turn_plane.iloc[t].values) == 1 : 
            nb_virage += 1
            nb_turn = 0
            if turn_plane.iloc[t].values == 1 :
                turn_side.append("droite")
            if turn_plane.iloc[t].values == -1 :
                turn_side.append("gauche")


    Frequence_tete = []
    
    #une valeur toutes les 0.1sec dans le tableau environ
    
    for k in range(len(turning_head)):
        Frequence_tete.append(round(0.1*turning_plane[k]/len(turning_head[k]),1))



##############      LES SORTIES AFFICHEES 

    print("Nombre de virages : ", nb_virage)
    print("Coté de chaque virage : ", turn_side)
    print("Duree de chaque virage : ",[round(float(i)*0.1,1) for i in turning_plane], " s")
    
    #for k in range(len(turning_head)):
        #turning_head[k] = [round(float(i)*0.1,1) for i in turning_head[k]]
    #print("Temps regard à l'exterieur pendant chaque virage",turning_head, " s")
    
    nb_regards = []
    for i in range (len(turning_head)): 
        nb_regards += [len(turning_head[i])]
    print("Nombre de regards a l'exterieur pour chaque virage :", nb_regards)
    
    print("Temps moyen entre deux regards a l'exterieur pour chaque virage",Frequence_tete, " s")





"""
data_path ="/Users/theo_taupiac/Desktop/PIE_0018/Logs_1012/flight_10Dec2019_guilhem"

# Parse flight data and points of interest
data = pd.read_csv(data_path + "/numData_100ms.csv", sep=';')
      
freq_head_turning(plane_and_head_turning(data))   
#turning_plane,turning_head)    
"""
"""   
    
    
###############################################################################
######################          TEST FONCTION          ########################  
###############################################################################
    
plane_turning(dataFlight)
head_turning(dataFlight)
freq_head_turning(DataMove)

"""
### A CODER changement dinclinaison precede d'un regard (DEBUT ET FIN VIRAGE)