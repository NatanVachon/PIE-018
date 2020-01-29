# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:48:05 2020

@author: natan
"""

import sys
sys.path.insert(1, 'Preprocessing')
sys.path.insert(2, 'Features')

import AOI_classifier as aoic
import pandas as pd
import Pattern_From_AOI as pfa
import creation_baseMove as cb
import Preprocessing
import TrafficSearch as ts

import numpy as np
# Data path
#data_path = "d:/natan/Documents/PIE/Logs/flight_10Dec2019_guilhem"

#data_path ="/Users/theo_taupiac/Desktop/PIE_0018/Logs_1012/flight_10Dec2019_guilhem"

data_path ="d:/Drive/PIE/LOG/10_12_log/Logs/flight_10Dec2019_simon"

#data_path = "c:/Users/Utilisateur/Desktop/PIE/10-12_log/Logs/flight_10Dec2019_simon"
#data_path="d:/Drive/PIE/LOG/10_12_log/Logs/flight_10Dec2019_guilhem"

# Parse flight data and points of interest
data = pd.read_csv(data_path + "/numData_100ms.csv", sep=';')
poi = pd.read_csv(data_path + "/flightEvent0.csv", sep=';')


# ----------------------------------   DATA PREPROCESSING   ------------------------------- #
data, poi = Preprocessing.data_preprocessing(data, poi)


# ----------------------------------   TEST THEO ----------------------------------------#

DataMove = cb.plane_and_head_turning(data)
cb.freq_head_turning(DataMove)

# ----------------------------------   AOI CLASSIFICATION   ------------------------------- #
# Zone computation
zones = aoic.compute_zones(data, poi)
# Classify from flight data
aois = aoic.classify_aois(zones, data)

# ----------------------------------   TRANSITION EXTRACTION   ------------------------------- #
seuil = 10
#Sort les différents états : delta= temps resté sur cet AOI
###SEUIL = seuil en ms pour considérer que c'est pas un outlier
clean_aois=pfa.clean_AOI(aois, seuil)

#LISTE DES ETATS
liste_aoi=clean_aois["AOI"].tolist()
print("AOI nettoyés")
pivot,transition=pfa.count_transitions(clean_aois)
print("Transitions comptées")

print(pivot) #pivot = table de passage des transition
print(transition) #transition = tableau des transitions

###############################################################################
#########################        FEATURES          ############################
###############################################################################

# Check if a traffic search happened around 100s
print("Check for traffic check around 100s:", ts.traffic_search(data, 100))

#Sort une compilation des difféerents AOI ( temps passé sur chaque, % du total...)
stats_aoi=pfa.count_AOI(clean_aois ,aois)
print(stats_aoi)

tbp=clean_aois[["delta","timestamp","AOI"]]

aoi=[["L","r","Left"],["F","g","Front"],["R","y","Right"],["P","b","Primary"],["S","c","Secondary"]]
L ='r'
F='g'
R='y'
P='b'
S='c'
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("Temps de vol ( ms) ")
ax1.set_ylabel("Temps passé sur chaque AOI sans transition( ms) ")

for a in aoi:
    aoigraph=clean_aois[clean_aois["AOI"]==a[0]]
    aoigraph=aoigraph[["timestamp","delta"]]
    ax1.scatter(aoigraph["timestamp"],aoigraph["delta"],c=a[1],label=a[2])
plt.legend(loc='upper left');
plt.show()

chain=pfa.chain_AOI(pivot,liste_aoi)
print(chain)