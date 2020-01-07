# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:48:05 2020

@author: natan
"""

import AOI_classifier as aoic
import pandas as pd
import Pattern_From_AOI as pfa

import sys
sys.path.insert(1, 'Preprocessing')
import Preprocessing

# Data path
data_path = "d:/natan/Documents/PIE/Logs/flight_10Dec2019_guilhem"

# Parse flight data and points of interest
data = pd.read_csv(data_path + "/numData_100ms.csv", sep=';')
poi = pd.read_csv(data_path + "/flightEvent0.csv", sep=';')

# ----------------------------------   DATA CLEANING   ------------------------------- #
data = Preprocessing.data_preprocessing(data)

# ----------------------------------   AOI CLASSIFICATION   ------------------------------- #
# Zone computation
zones = aoic.compute_zones(data, poi)
# Classify from flight data
aois = aoic.classify_aois(zones, data)



# ----------------------------------   TRANSITION EXTRACTION   ------------------------------- #
seuil=10
#Sort les différents états : delta= temps resté sur cet AOI
###SEUIL = seuil en ms pour considérer que c'est pas un outlier
clean_aois=pfa.clean_AOI(aois,seuil)

#LISTE DES ETATS
liste_aoi=clean_aois["AOI"].tolist()

pivot,transition=pfa.count_transitions(clean_aois)

print(pivot) #pivot = table de passage des transition
print(transition) #transition = tableau des transitions


#Sort une compilation des difféerents AOI ( temps passé sur chaque, % du total...)
stats_aoi=pfa.count_AOI(clean_aois,aois)
print(stats_aoi)

tbp=clean_aois[["delta","timestamp","AOI"]]
tbp.plot(kind='scatter',x=1,y=0,c=colors,legend=True)

L ='r'
F='g'
R='y'
P='b'
S='c'
colors=tuple(colors)

colors = np.where(clean_aois["AOI"]=="L",L,np.where(clean_aois["AOI"]=="R",R,np.where(clean_aois["AOI"]=="P",P,np.where(clean_aois["AOI"]=="S",S,np.where(clean_aois["AOI"]=="F",F,F)))))
