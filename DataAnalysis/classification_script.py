# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:48:05 2020

@author: natan
"""

import AOI_classifier as aoic
import pandas as pd
import Pattern_From_AOI as pfa
# Data path
data_path = "d:/natan/Documents/PIE/Logs/flight_10Dec2019_guilhem"
data_path="D:/Drive/PIE/LOG/10_12_log/Logs/flight_10Dec2019_guilhem"
# Parse flight data and points of interest
data = pd.read_csv(data_path + "/numData_10ms.csv", sep=';')
poi = pd.read_csv(data_path + "/flightEvent0.csv", sep=';')

# Compute AOIs
zones = aoic.compute_zones(data, poi)
# Classify from flight data
aois = aoic.classify_aois(zones, data)



#Sort les différents états : delta= temps resté sur cet AOI
###SEUIL = seuil en ms pour considérer que c'est pas un outlier
clean_aois=pfa.clean_AOI(aois,seuil) 

#LISTE DES ETATS
clean_aois["AOI"].tolist()

#pivot = table de passage des transition
#transition = tableau des transitions
pivot,transition=pfa.(clean_aois)

print(pivot)
print(transition)


#Sort une compilation des difféerents AOI ( temps passé sur chaque, % du total...)
pfa.count_AOI(clean_aois,aois)




