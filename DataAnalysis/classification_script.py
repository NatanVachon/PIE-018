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
import Preprocessing
import TrafficSearch as ts

# Data path
data_path = "d:/natan/Documents/PIE/Logs/flight_10Dec2019_guilhem"

# Parse flight data and points of interest
data = pd.read_csv(data_path + "/numData_100ms.csv", sep=';')
poi = pd.read_csv(data_path + "/flightEvent0.csv", sep=';')

# ----------------------------------   DATA PREPROCESSING   ------------------------------- #
data, poi = Preprocessing.data_preprocessing(data, poi)

# ----------------------------------   AOI CLASSIFICATION   ------------------------------- #
# Zone computation
zones = aoic.compute_zones(data, poi)
# Classify from flight data
aois = aoic.classify_aois(zones, data)

# ----------------------------------   TRANSITION EXTRACTION   ------------------------------- #
seuil = 10
#Sort les différents états : delta= temps resté sur cet AOI
###SEUIL = seuil en ms pour considérer que c'est pas un outlier
clean_aois = pfa.clean_AOI(aois,seuil)

#LISTE DES ETATS
liste_aoi = clean_aois["AOI"].tolist()

pivot, transition = pfa.count_transitions(clean_aois)

print(pivot) #pivot = table de passage des transition
print(transition) #transition = tableau des transitions


#Sort une compilation des difféerents AOI ( temps passé sur chaque, % du total...)
stats_aoi = pfa.count_AOI(clean_aois,aois)
print(stats_aoi)

###############################################################################
#########################        FEATURES          ############################
###############################################################################

# Check if a traffic search happened around 100s
#print("Check for traffic check around 100s:", ts.traffic_search(data, 100))

