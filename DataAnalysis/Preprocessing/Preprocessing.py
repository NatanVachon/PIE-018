#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:19:00 2020

@author: theo_taupiac
"""

"""
Theo Taupiac

Reminder :
    Ce fichier se lance en lançant creation_baseMove
    lancer data_reconstruction en amont

"""
###############################################################################
#########################        IMPORTS          #############################
###############################################################################


###############################################################################
#########################       PARAMETRES       ##############################
###############################################################################

#threshold = 2

###############################################################################
#########################       FUNCTION       ################################
###############################################################################

def data_preprocessing(data, poi):
    # Cette étape permet d'enlever le freeze des premieres donnees de chaque log
    data = data.drop_duplicates(subset = "FD_PILOT_HEAD_PITCH")
    data = data.reset_index(drop = True)

    # On recale le timestamp à 0s
    t0 = data.at[0, "FD_TIME_MS"]

    data["FD_TIME_MS"].astype("float")
    data["FD_TIME_MS"] -= t0
    data["FD_TIME_MS"] *= 0.001
    data = data.rename(columns={"FD_TIME_MS": "FD_TIME_S"})

    poi["FD_TIME_MS"].astype("float")
    poi["FD_TIME_MS"] -= t0
    poi["FD_TIME_MS"] *= 0.001
    poi = poi.rename(columns={"FD_TIME_MS": "FD_TIME_S"})

    ####### Columns names
    """
    ### POSITION
    Position_name = ["FD_PILOT_HEAD_HEADING","FD_PILOT_HEAD_ROLL_X","FD_PILOT_HEAD_PITCH"]

    ### TIME
    Speed_name = ["FD_PILOT_speed_HEAD_HEADING","FD_PILOT_speed_HEAD_ROLL_X","FD_PILOT_speed_HEAD_PITCH"]
    Acc_name = ["FD_PILOT_acc_HEAD_HEADING","FD_PILOT_acc_HEAD_ROLL_X","FD_PILOT_acc_HEAD_PITCH"]
    Jerk_name = ["FD_PILOT_jerk_HEAD_HEADING","FD_PILOT_jerk_HEAD_ROLL_X","FD_PILOT_jerk_HEAD_PITCH"]

    ### FFT
    FFT_Speed_name = ["FD_PILOT_FFT_speed_HEAD_HEADING","FD_PILOT_FFT_speed_HEAD_ROLL_X","FD_PILOT_FFT_speed_HEAD_PITCH"]
    FFT_Acc_name = ["FD_PILOT_FFT_acc_HEAD_HEADING","FD_PILOT_FFT_acc_HEAD_ROLL_X","FD_PILOT_FFT_acc_HEAD_PITCH"]
    FFT_Jerk_name = ["FD_PILOT_FFT_jerk_HEAD_HEADING","FD_PILOT_FFT_jerk_HEAD_ROLL_X","FD_PILOT_FFT_jerk_HEAD_PITCH"]

    ####### Changement du format

    temp_col = data["FD_TIME_MS"]
    #data = data.stack().str.replace(',','.').unstack()
    data[Position_name[0]] = data[Position_name[0]].astype(float)
    data[Position_name[1]] = data[Position_name[1]].astype(float)
    data[Position_name[2]] = data[Position_name[2]].astype(float)
    data["FD_TIME_MS"] = temp_col

    ###############################################################################
    ###################       VARIABLES OF HEAD PILOT       #######################
    ###############################################################################

    #########    TIME
    ### SPEED
    for i in range(3) :
        data[Speed_name[i]]=0
        for k in range (threshold, len(data)-threshold):
            data.loc[k,Speed_name[i]] = (data.loc[k+threshold,Position_name[i]]- data.loc[k-threshold,Position_name[i]])/((data.loc[k+threshold,"FD_TIME_MS"]- data.loc[k-threshold,"FD_TIME_MS"])*0.001)

    ### ACCELERATION
    for i in range(3) :
        data[Acc_name[i]]=0
        for k in range (threshold, len(data)-threshold):
            data.loc[k,Acc_name[i]] = (data.loc[k+threshold,Speed_name[i]]- data.loc[k-threshold,Speed_name[i]])/((data.loc[k+threshold,"FD_TIME_MS"]- data.loc[k-threshold,"FD_TIME_MS"])*0.001)

    ### JERK
    for i in range(3) :
        data[Jerk_name[i]]=0
        for k in range (threshold, len(data)-threshold):
            data.loc[k,Jerk_name[i]] = (data.loc[k+threshold,Acc_name[i]]- data.loc[k-threshold,Acc_name[i]])/((data.loc[k+threshold,"FD_TIME_MS"]- data.loc[k-threshold,"FD_TIME_MS"])*0.001)
    """
    return data, poi