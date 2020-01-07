# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:48:05 2020

@author: natan
"""

import AOI_classifier as aoic
import pandas as pd

# Data path
data_path = "d:/natan/Documents/PIE/Logs/flight_10Dec2019_guilhem"

# Parse flight data and points of interest
data = pd.read_csv(data_path + "/numData_10ms.csv", sep=';')
poi = pd.read_csv(data_path + "/flightEvent0.csv", sep=';')

# Compute AOIs
zones = aoic.compute_zones(data, poi)
# Classify from flight data
aois = aoic.classify_aois(zones, data)