#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains the functions to analyse turning situations

"""


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       IMPORTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Constants as const

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def plane_and_head_turning(df):
    """
    Function that create a dateframe with all the direction of the plane's turns'

    Parameters
    ----------
    df : panda Dataframe
        dataframe with all the data collected about a flight, every 100ms.

    Returns
    -------
    None.

    """


    DataMove = pd.DataFrame(columns = ['turning_plane'])

    ######### CODE PLANE_TURNING

    roulis = df.loc[:,["FD_AHRS_ROLL"]]
    cap = df.loc[:,["FD_AHRS_HEADING"]]
    #cap = df.loc[:,["FD_GPS_COURSE"]]       #  CHANGE ALL THE HEADING TO COURSE IF COURSE AVAILABLE
    cap_time = df.loc[:,["FD_TIME_S"]]


    for t in range(const.DT_SW_TURN, len(df)-const.DT_SW_TURN):

        roulis_current = roulis.iloc[t-const.DT_SW_TURN:t+const.DT_SW_TURN]
        cap_current = cap.iloc[t-const.DT_SW_TURN:t+const.DT_SW_TURN]
        cap_current_time = cap_time.iloc[t-const.DT_SW_TURN:t+const.DT_SW_TURN]

        moyenne_roulis = roulis_current.mean().FD_AHRS_ROLL

        vect = cap_current.FD_AHRS_HEADING.values
        #vect = cap_current.FD_GPS_COURSE.values
        vect_time = cap_current_time.FD_TIME_S.values


        deriv=[]
        for k in range(len(vect)-1):
            u=(vect[k+1]-vect[k])*1000/(vect_time[k+1]-vect_time[k])
            deriv.append(abs(u))

        moyenne_deriv_cap = np.mean(deriv)

        if (moyenne_roulis <= - const.PLANE_TURN_VALUE) & (moyenne_deriv_cap >= const.DERIVE_CAP) :
            DataMove.loc[t,'turning_plane'] = -1
            #"<<<------"

        elif (moyenne_roulis >= const.PLANE_TURN_VALUE) & (moyenne_deriv_cap >= const.DERIVE_CAP) :
            DataMove.loc[t,'turning_plane'] = 1
            #"------>>>"
        else:
            DataMove.loc[t,'turning_plane'] = 0
            #"^^^"


    return(DataMove)



def temporal_graph(dm):
    """
    Create the temporal graph about the dynamic of head turns and plane turns

    Parameters
    ----------
    dm: panda Dataframe
        dataframe with all the plane's turns and heads position about a flight, every 100ms.

    Returns
    -------
    None.

    """
    plt.figure()
    plt.plot(dm.loc[:,["turning_plane"]])
    plt.plot(dm.loc[:,["turning_head"]]*0.5)   #.replace(0, np.nan))
    plt.show()




def graph_results_turning(dm):
    """

    Applied directly on Datamove, thanks to data created by the two previous functions.
    Give informations/graphs about turning situations (symetry during turns, security checks, explanations of non secure turns)

    Parameters
    ----------
    dm: panda Dataframe
        dataframe with all the plane's turns and heads position about a flight, every 100ms.

    Returns
    -------
    time_begin_turn : list
        list of the timestamp of the beginning of the turn
    
    time_end_turn : list
        list of the timestamp of the end of the turn
    
    duree_virage : list
        list of the duration, all turns
        
    turn_side : list
        list of the sides, all turns
    
    -- all these returns are used in the global plot --

    """
    nb_virage = 0
    turn_side = []
    nb_turn = 0

    turning_plane = []
    turning_head = []
    
    time_begin_turn = []
    time_end_turn = []

    last_look_before_turning = []
    last_look_before_end = []

    turn_plane = dm.loc[:,["turning_plane"]]
    turn_head = dm.loc[:,["AOI"]]


    for t in range(len(dm)-1):

        # NOUVEAU VIRAGE
        if abs(turn_plane.iloc[t+1].values) == 1 and turn_plane.iloc[t].values == 0:

            turning_plane.append(1)
            
            time_begin_turn.append(round(dm.loc[t+1,"FD_TIME_S"],1))
            
            if turn_head.iloc[t+1].values == 'R':
                turning_head.append([1])
            if turn_head.iloc[t+1].values == 'L':
                turning_head.append([-1])
            else:
                turning_head.append([0])

            # Regards avant le virage
            p = t
            while (p > t - const.LAST_T_TO_CHECK) & (turn_head.iloc[p].values !='R') & (turn_head.iloc[p].values !='L') :
                p-=1
            temp_time = p
            if turn_head.iloc[p].values == 'R' :
                last_look_before_turning.append(["Right",1,round(dm.loc[t,"FD_TIME_S"]-dm.loc[p,"FD_TIME_S"],1)]) ### indique le cote de la tete en premier, le nb de secondes en second, et cb de secondes cetait avant le virage en 3eme variable
            elif turn_head.iloc[p].values == 'L' :
                last_look_before_turning.append(["Left",1,round(dm.loc[t,"FD_TIME_S"]-dm.loc[p,"FD_TIME_S"],1)])
            else:
                last_look_before_turning.append(["NONE",0,0])
            p-=1
            while (p > t - const.LAST_T_TO_CHECK) & (turn_head.iloc[p].values == turn_head.iloc[temp_time].values):
                p-=1

                #last_look_before_turning[nb_virage][1] += 1

            last_look_before_turning[nb_virage][1] = round(dm.loc[temp_time,"FD_TIME_S"]-dm.loc[p,"FD_TIME_S"],1)


        # VIRAGE QUI CONTINUE
        if abs(turn_plane.iloc[t+1].values) == 1 and abs(turn_plane.iloc[t].values) == 1:
            turning_plane[nb_virage] += 1

            # TETE A DROITE
            if turn_head.iloc[t+1].values == 'R' and turn_head.iloc[t].values == 'R':
                turning_head[nb_virage][nb_turn] += 1
            if turn_head.iloc[t+1].values == 'R' and turn_head.iloc[t].values != 'R' :
                nb_turn += 1
                turning_head[nb_virage].append(1)


             # TETE A GAUCHE
            if turn_head.iloc[t+1].values == 'L' and turn_head.iloc[t].values == 'L':
                turning_head[nb_virage][nb_turn] -= 1
            if turn_head.iloc[t+1].values == 'L' and turn_head.iloc[t].values != 'L' :
                nb_turn += 1
                turning_head[nb_virage].append(-1)



        # FIN DE VIRAGE
        if turn_plane.iloc[t+1].values == 0 and abs(turn_plane.iloc[t].values) == 1 :
            nb_virage += 1
            nb_turn = 0
            
            time_end_turn.append(round(dm.loc[t+1,"FD_TIME_S"],1))
            
            if turn_plane.iloc[t].values == 1 :
                turn_side.append("Right")
            if turn_plane.iloc[t].values == -1 :
                turn_side.append("Left")

            # Regards avant de sortir du virage
            p = t
            while (p > t - const.LAST_T_TO_CHECK) & (turn_head.iloc[p].values !='R') & (turn_head.iloc[p].values !='L') :
                p-=1
            temp_time = p
            if turn_head.iloc[p].values == 'R' :
                last_look_before_end.append(["Right",1,round(dm.loc[t,"FD_TIME_S"]-dm.loc[p,"FD_TIME_S"],1)]) ### indique le cote de la tete en premier, le nb de secondes en second, et cb de secondes cetait avant le virage en 3eme variable
            elif turn_head.iloc[p].values == 'L' :
                last_look_before_end.append(["Left",1,round(dm.loc[t,"FD_TIME_S"]-dm.loc[p,"FD_TIME_S"],1)])
            else :
                last_look_before_end.append(["NONE",0,0])
            p-=1
            while (p > t - const.LAST_T_TO_CHECK) & (turn_head.iloc[p].values == turn_head.iloc[temp_time].values):
                p-=1

                #last_look_before_end[nb_virage-1][1] += 1
            last_look_before_end[nb_virage-1][1] = round(dm.loc[temp_time,"FD_TIME_S"]-dm.loc[p,"FD_TIME_S"],1)

    #une valeur toutes les 0.1sec dans le tableau environ
    #Frequence_tete = []
    #for k in range(len(turning_head)):
        #Frequence_tete.append(round(0.1*turning_plane[k]/len(turning_head[k]),1))



##############      LES SORTIES AFFICHEES

    print("Nombre de virages : ", nb_virage)
    print()
    print("Coté de chaque virage : ", turn_side)
    print()
    duree_virage = [round(time_end_turn[i] - time_begin_turn[i],1) for i in range(len(time_end_turn))]
    print("Duree de chaque virage : ",duree_virage, " s")
    print()
    for k in range(len(turning_head)):
        turning_head[k] = [round(float(i)*0.1,1) for i in turning_head[k]]
    print("Temps regard à l'exterieur pendant chaque virage",turning_head, " s")
    print()
    nb_regards = []
    for i in range (len(turning_head)):
        nb_regards += [len(turning_head[i])]
    print("Nombre de regards a l'exterieur pour chaque virage :", nb_regards)
    print()
    print("Cote dernier regard avant de tourner/duree/il ya cb de secondes",last_look_before_turning)
    print()
    print("Cote dernier regard avant de revenir droit/duree/il ya cb de secondes",last_look_before_end)
    print("Timestamp des débuts de virage",time_begin_turn)
    print()
    print("Timestamp des fins de virage",time_end_turn)


    #print("Temps moyen entre deux regards a l'exterieur pour chaque virage",Frequence_tete, " s")

####    PIE CHART AGREGE DES VIRAGES DROITE & GAUCHE

    sum_total_LT_front = 0
    sum_total_LT_left = 0
    sum_total_LT_right = 0
    sum_total_RT_front = 0
    sum_total_RT_left = 0
    sum_total_RT_right = 0

    virage_secure = 0
    virage_unsecure = []

    for k in range(len(turn_side)):

# LEFT
        if turn_side[k] == "Left" :
            sum_total_LT_front += duree_virage[k]
            for value in turning_head[k]:
                if value <0:
                    sum_total_LT_left -= value
                    sum_total_LT_front += value
                else:
                    sum_total_LT_right += value
                    sum_total_LT_front -= value
# RIGHT
        else :
            sum_total_RT_front += duree_virage[k]
            for value in turning_head[k]:
                if value <0:
                    sum_total_RT_left -= value
                    sum_total_RT_front += value
                else:
                    sum_total_RT_right += value
                    sum_total_RT_front -= value

# Turn starts security
        # TEST #  last_look_before_turning[0][0]="Left"

        virage_unsecure.append([])
        if turn_side[k] != last_look_before_turning[k][0]: # dernier regard du cote du virage
            virage_unsecure[-1].append("Last look before turning was to the "+last_look_before_turning[k][0]+", turn was to the "+turn_side[k]+" -" )
        if last_look_before_turning[k][1] < 0.4:    # 0.4 secondes mini a regarder le cote ou l'on tourne
            virage_unsecure[-1].append("Last look before turning was not long enough (< 0.4 seconds) - ")
        if last_look_before_turning[k][2] > 5:  # dernier regard il ya moins de 5 secondes
            virage_unsecure[-1].append("Last look before turning was too far from the turn (> 5 seconds) - ")

        if last_look_before_turning[k][0] == "NONE":  # pas de regard !
            virage_unsecure[-1].append("NO look outside before turning ! - ")
# Turn end security

        if turn_side[k] == last_look_before_end[k][0]: # dernier regard du cote du virage
            virage_unsecure[-1].append("The last check before the end of the turn was to the "+last_look_before_end[k][0]+", turn was to the "+turn_side[k]+" -" )
        if last_look_before_end[k][1] < 0.4:    # 0.4 secondes mini a regarder le cote ou l'on tourne
            virage_unsecure[-1].append("Last look before the end of the turn was not long enough (< 0.4 seconds) - ")
        if last_look_before_end[k][2] > 5:  # dernier regard il ya moins de 5 secondes
            virage_unsecure[-1].append("Last look before the end of the turn was too far from the turn (> 5 seconds) - ")

        if last_look_before_end[k][0] == "NONE":
            virage_unsecure[-1].append("NO look outside before quitting the turn ! - ")


        if  virage_unsecure[-1] == []:
            virage_secure +=1
            virage_unsecure.remove(virage_unsecure[-1]) # si tout est bon, on vire la liste vide

###### LEFT TURNS

    # defining labels
    activities = ['Front', 'Left', 'Right']
    #portion covered by each label
    slices = [sum_total_LT_front,sum_total_LT_left,sum_total_LT_right]
    # color for each label
    colors = ['g', 'b', 'r']
    # plotting the pie chart
    plt.pie(slices, labels = activities, colors=colors,
            startangle=90, shadow = True,
            radius = 1.2, autopct = '%1.1f%%')
    # title the pie
    plt.title("Looks during Left turns", pad = 20)
    # plotting legend
    plt.legend()
    # showing the plot
    plt.show()


###### RIGHT TURNS

    # defining labels
    activities = ['Front', 'Left', 'Right']
    #portion covered by each label
    slices = [sum_total_RT_front,sum_total_RT_left,sum_total_RT_right]
    # color for each label
    colors = ['g', 'b', 'r']
    # plotting the pie chart
    plt.pie(slices, labels = activities, colors=colors,
            startangle=90, shadow = True,
            radius = 1.2, autopct = '%1.1f%%')
    # title the pie
    plt.title("Looks during Right turns", pad = 20)
    # plotting legend
    plt.legend()
    # showing the plot
    plt.show()

###### PLOT SECURITY TURNS

    # defining labels
    activities = ['Securised turn', 'Non secure']
    #portion covered by each label
    slices = [virage_secure,len(virage_unsecure)]
    # color for each label
    colors = ['g', 'r']
    # plotting the pie chart
    plt.bar(height = slices, x = activities)
    # title the pie
    plt.title("Security before turns", pad = 20)
    # showing the plot
    plt.show()
    if virage_unsecure != []:
        print ("Details of the unsecure turning situation :")
        print(virage_unsecure)

    return(time_begin_turn, time_end_turn, duree_virage, turn_side)

"""
Optional graph, not used right now

####    PIE CHART DE TOUS LES VIRAGES

    for k in range(len(turn_side)):
        sum_left = 0
        sum_right = 0
        for value in turning_head[k]:
            if value <0:
                sum_left -= value
            else:
                sum_right += value

        # defining labels
        activities = ['Front', 'Left', 'Right']
        #portion covered by each label
        slices = [duree_virage[k]-sum_left-sum_right,sum_left,sum_right]
        # color for each label
        colors = ['g', 'b', 'r']
        # plotting the pie chart
        plt.pie(slices, labels = activities, colors=colors,
                startangle=90, shadow = True,
                radius = 1.2, autopct = '%1.1f%%')
        # title the pie
        plt.title(turn_side[k] + " turn", pad = 20)

        # plotting legend
        plt.legend()
        # showing the plot
        plt.show()
"""