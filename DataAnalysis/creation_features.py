# -*- coding: utf-8 -*-
"""
Theo Taupiac

Reminder :
    
    lancer data_reconstruction en amont
    Ajouter le GPS POUR IS_TURNING
        
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

threshold = 2

address_folder = "/Users/theo_taupiac/Desktop/PIE_0018/1211_test_protocole"
pilot_names = ["/1211_Guilhem_gauche","/1211_maxime_droite","/1211_simon_droite","/1211_natan_gauche"]

# voir si on code pour utiliser les 100ms
choix_pilote = 1

###############################################################################
#########################       FUNCTIONS        ##############################
###############################################################################

def my_read_csv(filename):
    return pd.read_csv(filename, sep = ';')

###############################################################################
#################      OPENING CSV AND COLUMNS NAMES       ####################
###############################################################################

#   BUG
filename = address_folder + pilot_names[choix_pilote] + "/numData_10ms_"
#dataFlight = my_read_csv("/Users/theo_taupiac/Desktop/PIE_0018" + filename)
    
####### Opening CSV

dataFlight = my_read_csv(filename)
#dataFlight = my_read_csv(address_folder + "/numData_10ms_.csv")

# Cette étape fait office de passage a 100ms pour le moment
dataFlight = dataFlight.drop_duplicates(subset = "FD_PILOT_HEAD_HEADING" )
dataFlight = dataFlight.reset_index(drop = True)

#Verification avec les time\
"""
liste_des_ecarts_temporels = []
for k in range(len(dataFlight)-1):
    liste_des_ecarts_temporels += [(dataFlight.loc[k+1,'FD_TIME_MS']-dataFlight.loc[k,'FD_TIME_MS'])]
max(liste_des_ecarts_temporels)
min(liste_des_ecarts_temporels)
np.mean(liste_des_ecarts_temporels)
plt.boxplot(liste_des_ecarts_temporels)
Plt.grid()
"""
####### Columns names

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

temp_col = dataFlight["FD_TIME_MS"]
#dataFlight = dataFlight.stack().str.replace(',','.').unstack()
dataFlight[Position_name[0]] = dataFlight[Position_name[0]].astype(float)
dataFlight[Position_name[1]] = dataFlight[Position_name[1]].astype(float)
dataFlight[Position_name[2]] = dataFlight[Position_name[2]].astype(float)
dataFlight["FD_TIME_MS"] = temp_col

###############################################################################
###################       VARIABLES OF HEAD PILOT       #######################
###############################################################################

#########    TIME
### SPEED
for i in range(3) :
    dataFlight[Speed_name[i]]=0
    for k in range (threshold, len(dataFlight)-threshold):
        dataFlight.loc[k,Speed_name[i]] = (dataFlight.loc[k+threshold,Position_name[i]]- dataFlight.loc[k-threshold,Position_name[i]])/((dataFlight.loc[k+threshold,"FD_TIME_MS"]- dataFlight.loc[k-threshold,"FD_TIME_MS"])*0.001)
        
### ACCELERATION
for i in range(3) :
    dataFlight[Acc_name[i]]=0
    for k in range (threshold, len(dataFlight)-threshold):
        dataFlight.loc[k,Acc_name[i]] = (dataFlight.loc[k+threshold,Speed_name[i]]- dataFlight.loc[k-threshold,Speed_name[i]])/((dataFlight.loc[k+threshold,"FD_TIME_MS"]- dataFlight.loc[k-threshold,"FD_TIME_MS"])*0.001)

### JERK       
for i in range(3) :
    dataFlight[Jerk_name[i]]=0
    for k in range (threshold, len(dataFlight)-threshold):
        dataFlight.loc[k,Jerk_name[i]] = (dataFlight.loc[k+threshold,Acc_name[i]]- dataFlight.loc[k-threshold,Acc_name[i]])/((dataFlight.loc[k+threshold,"FD_TIME_MS"]- dataFlight.loc[k-threshold,"FD_TIME_MS"])*0.001)
"""
#########    FFT
### SPEED
for i in range(3) :
    dataFlight[Speed_name[i]]=0
    for k in range (threshold, len(dataFlight)-threshold):
        dataFlight.loc[k,Speed_name[i]] = 
        
### ACCELERATION
for i in range(3) :
    dataFlight[Acc_name[i]]=0
    for k in range (threshold, len(dataFlight)-threshold):
        dataFlight.loc[k,Acc_name[i]] = 

### JERK       
for i in range(3) :
    dataFlight[Jerk_name[i]]=0
    for k in range (threshold, len(dataFlight)-threshold):
        dataFlight.loc[k,Jerk_name[i]] = 

"""

"""
D'apres le travail de  "Anguita et al. (2013)", voici les datas et procedes appliques pour obtenir 561 variables.

Datas

tBodyAcc-XYZ
tGravityAcc-XYZ
tBodyAccJerk-XYZ
tBodyGyro-XYZ
tBodyGyroJerk-XYZ
tBodyAccMag
tGravityAccMag
tBodyAccJerkMag
tBodyGyroMag
tBodyGyroJerkMag
fBodyAcc-XYZ
fBodyAccJerk-XYZ
fBodyGyro-XYZ
fBodyAccMag
fBodyAccJerkMag
fBodyGyroMag
fBodyGyroJerkMag
"""

"""
mean(): Mean value
std(): Standard deviation
mad(): Median absolute deviation 
max(): Largest value in array
min(): Smallest value in array
sma(): Signal magnitude area
energy(): Energy measure. Sum of the squares divided by the number of values. 
iqr(): Interquartile range 
entropy(): Signal entropy
arCoeff(): Autorregresion coefficients with Burg order equal to 4
correlation(): correlation coefficient between two signals
maxInds(): index of the frequency component with largest magnitude
meanFreq(): Weighted average of the frequency components to obtain a mean frequency
skewness(): skewness of the frequency domain signal 
kurtosis(): kurtosis of the frequency domain signal 
bandsEnergy(): Energy of a frequency interval within the 64 bins of the FFT of each window.
angle(): Angle between to vectors.

gravityMean
tBodyAccMean
tBodyAccJerkMean
tBodyGyroMean
tBodyGyroJerkMean


"""