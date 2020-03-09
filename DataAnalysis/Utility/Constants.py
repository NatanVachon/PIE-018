# -*- coding: utf-8 -*-
"""
Constants file, used to centralize each important constant.
"""

AOI_MIN_TIME = 0.01 #[s]

TRAFFIC_SEARCH_WINDOW = 0.02 #[s]

TRAFFIC_SEARCH_MIN_HEADING_AMPLITUDE = 130. #[°]

SEUIL_TETE_FIXE = 2. #[s]

ROLLING_MEAN = 10 # Length of the rolling mean window for energy computation

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                Constants creation_baseMove
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

DT_SW_TURN = 4 # nombre de valeurs pour prendre la moyenne du roulis, et derivee instantanee du defilement de cap

PLANE_TURN_VALUE = 15 # inclinaison des ailes minimale pour considerer un virage

DERIVE_CAP = 1 # on considere un virage lorsque la derive de cap est > a 1'/s

LAST_T_TO_CHECK = 100 # on regarde 10 sec avant debut virage, et 10 sec avant la fin pour le dernier regard
