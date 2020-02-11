# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:54:16 2020

@author: natan
"""


AOI_MIN_TIME = 0.01 #[s]
TRAFFIC_SEARCH_WINDOW = 0.02 #[s]
TRAFFIC_SEARCH_MIN_HEADING_AMPLITUDE = 130. #[°]
SEUIL_TETE_FIXE=2. #[s]
ROLLING_MEAN=10 # nombre de sample sur lequel faire un rolling mean de l'energie

# Pour creation_baseMove

dt_sw_turn = 4 # nombre de valeurs pour prendre la moyenne du roulis, et derivee instantanee du defilement de cap
head_turn_value = 10 # A PARAMETRER EN FONCTION DE LA CROIX <----- !!!
plane_turn_value = 15 # inclinaison des ailes minimale pour considerer un virage
derive_cap = 1 # on considere un virage lorsque la derive de cap est > a 1'/s
last_t_to_check = 100 # on regarde 10 sec avant debut virage, et 10 sec avant la fin pour le dernier regard
