# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:48:05 2020

@author: natan
"""

import sys
sys.path.insert(1, 'Preprocessing')
sys.path.insert(2, 'Features')
sys.path.insert(3, 'Graphs')

import AOI_classifier as aoic
import pandas as pd
import Pattern_From_AOI as pfa
import creation_baseMove as cb
import Preprocessing
import TrafficSearch as ts
import Constants as const
import graphs as grh

# Data path
#data_path = "d:/natan/Documents/PIE/Logs/flight_10Dec2019_guilhem"

data_path ="/Users/theo_taupiac/Desktop/PIE_0018/Logs_1012/flight_10Dec2019_guilhem"

#data_path ="d:/Drive/PIE/LOG/10_12_log/Logs/flight_10Dec2019_simon"

#data_path ="d:/Drive/PIE/LOG/10_12_log/Logs/flight_10Dec2019_maxime"

#data_path = "c:/Users/Utilisateur/Desktop/PIE/10-12_log/Logs/flight_10Dec2019_simon"

#data_path="d:/Drive/PIE/LOG/10_12_log/Logs/flight_10Dec2019_guilhem"

# Parse flight data and points of interest
data = pd.read_csv(data_path + "/numData_100ms.csv", sep=';')
poi = pd.read_csv(data_path + "/flightEvent0.csv", sep=';')


# ----------------------------------   DATA PREPROCESSING   ------------------------------- #
#data, poi = Preprocessing.data_preprocessing(data, poi)


# ----------------------------------   TEST THEO ----------------------------------------#

DataMove = cb.plane_and_head_turning(data)
cb.graph_results_turning(DataMove)
cb.temporal_graph(DataMove)
# ----------------------------------   AOI CLASSIFICATION   ------------------------------- #
# Zone computation
zones = aoic.compute_zones(data, poi)
# Classify from flight data
aois = aoic.classify_aois(zones, data)

# ----------------------------------   TRANSITION EXTRACTION   ------------------------------- #
#Sort les différents états : delta= temps resté sur cet AOI
###SEUIL = seuil en ms pour considérer que c'est pas un outlier
clean_aois=pfa.clean_AOI(aois, const.AOI_MIN_TIME)

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


## Listes des chaines trouvées
chain=pfa.chain_AOI(pivot,liste_aoi)
aoi_chain=pd.DataFrame(columns=["count"])
colormaps=["summer","autumn","winter"]



######Graph tps(AOI)
labels=tuple(stats_aoi["%_time"])
stats_aoi["%_time"].plot.pie(legend=True,autopct='%i%%')
grh.time_temps_aoi(clean_aois)
grh.hist_time_aoi(stats_aoi)
grh.hist_count_aoi(stats_aoi)
grh.hist_transitions(chain)


###############GRAPH HIST AOI



### Graphs f