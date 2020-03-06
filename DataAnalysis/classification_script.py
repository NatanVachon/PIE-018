# -*- coding: utf-8 -*-
"""
Global script used to execute everything.
"""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       IMPORTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import sys
sys.path.insert(1, 'Preprocessing')
sys.path.insert(2, 'Features')
sys.path.insert(3, 'Graphs')
import energy as enr
import AOI_classifier as aoic
import pandas as pd
import Pattern_From_AOI as pfa
import creation_baseMove as cb
import Preprocessing
import TrafficSearch as ts
import Constants as const
import graphs as grh
import matplotlib.pyplot as plt
import GlobalPlot as gp
from Lookup import largest_lookup

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       DATA PARSING
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Data path
#data_path = "d:/natan/Documents/PIE/Logs/Log PIE 4 feb/guilhem/flight_04Feb2020_161253_nominal"
#data_path = "d:/natan/Documents/PIE/Logs/Log PIE 4 feb/hugo/flight_04Feb2020_163644_nominal"
#data_path ="/Users/theo_taupiac/Desktop/PIE_0018/Logs_1012/flight_10Dec2019_taupichef"
data_path ="/Users/theo_taupiac/Desktop/PIE_0018/Log_PIE_4_feb/maxime/flight_04Feb2020_nominal"

#data_path ="/Users/theo_taupiac/Desktop/PIE_0018/Logs_1012/flight_10Dec2019_maxime"

#data_path ="d:/Drive/PIE/LOG/04_02_2020/guilhem"

#data_path ="d:/Drive/PIE/Logs/Log PIE 4 feb/leonard/flight_04Feb2020_162341_work"
#data_path = "c:/Users/Utilisateur/Desktop/PIE/10-12_log/Logs/flight_10Dec2019_simon"

#data_path="d:/Drive/PIE/LOG/10_12_log/Logs/flight_10Dec2019_guilhem"

# Parse flight data and points of interest
data = pd.read_csv(data_path + "/numData_100ms.csv", sep=';')
poi = pd.read_csv(data_path + "/flightEvent0.csv", sep=';')

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       EXECUTION
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# ----------------------------------   DATA PREPROCESSING   ------------------------------- #
data, poi = Preprocessing.data_preprocessing(data, poi)


# ----------------------------------   AOI CLASSIFICATION   ------------------------------- #
# Zone computation
zones = aoic.compute_zones(data, poi)
# Classify from flight data
aois = aoic.classify_aois(zones, data)

# ----------------------------------   TRANSITION EXTRACTION   ------------------------------- #
#Sort les différents états : delta= temps resté sur cet AOI
clean_aois=pfa.clean_AOI(aois, const.AOI_MIN_TIME)


# ----------------------------------   TEST VIRAGE    ----------------------------------------#

DataMove = cb.plane_and_head_turning(data)
aois_temp = aois[const.dt_sw_turn: -const.dt_sw_turn]

DataMove = DataMove.join(aois_temp)

del aois_temp

cb.graph_results_turning(DataMove) #pour l'avoir a nouveau, remplacer R par 1 et L par -1 dans datamove
#cb.temporal_graph(DataMove)


# ----------------------------------   ENERGY    ----------------------------------------#

#Energy ( gyro carré intégré)
energy,peak,mean=enr.energy(data,const.ROLLING_MEAN)

energy.plot()
plt.grid()
print('Energie moyenne : '+str(mean))

# ----------------------------------   AOIS ------------------------------- #

#LISTE DES ETATS
liste_aoi=clean_aois["AOI"].tolist()
print("AOI nettoyés")
pivot,transition=pfa.count_transitions(clean_aois)
print("Transitions comptées")

print(pivot) #pivot = table de passage des transition
print(transition) #transition = tableau des transitions

# Check if a traffic search happened around 100s
print("Check for traffic check around 100s:", ts.traffic_search(data, 30, 40))

#Sort une compilation des difféerents AOI ( temps passé sur chaque, % du total...)
stats_aoi=pfa.count_AOI(clean_aois ,aois)
print(stats_aoi)


## Listes des chaines trouvées
chain=pfa.chain_AOI(pivot,liste_aoi)
aoi_chain=pd.DataFrame(columns=["count"])


######Graph tps(AOI)
labels=tuple(stats_aoi["%_time"])
stats_aoi["%_time"].plot.pie(legend=True,autopct='%i%%')
grh.time_temps_aoi(clean_aois)
grh.hist_time_aoi(stats_aoi)
grh.hist_count_aoi(stats_aoi)
grh.hist_transitions(chain)


# ----------------------------------   TRAFFIC SEARCH   ------------------------------- #

traffic_search = largest_lookup(ts.traffic_search,data, 20.)
tete_fixe_tunnel = largest_lookup(pfa.tete_fixe_tunnel, aois, 2.)
tete_fixe = largest_lookup(pfa.tete_fixe, data, 2.)

# ----------------------------------   GLOBAL PLOTS   ------------------------------- #

gp.globalPlot(energy, tete_fixe=tete_fixe, tete_fixe_aoi=tete_fixe_tunnel, traffic_search=traffic_search)