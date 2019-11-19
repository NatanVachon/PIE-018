# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 11:57:23 2019
This is an example
@author: Sylvain Zorman
"""
import sys


"""
flight_folder_in = sys.argv[0] 
flight_folder_out = sys.argv[1]

"""


###################################################
# importing and filtering phy and comp data#####
if __name__ == '__main__':
    filename = 'C:/Users/DELL2/Documents/GitHub/VirtualRealityAnalysis/numData_100ms_2.csv'
    feat = Features(filename, 'comp')

    #feat = feat_import('test.pckl')
    feat.feat_compute(10, 10, 1)
    feat.save('test.pckl')
    #
    #
    #feat.display()
    #feat.display([3],[2,3])#[10],[2,3])#[3],[2])#t|ecg|pzt|eda|bpm|evt
    #feat.display_ts()
#['index', 'WdW Position', 'Ej', 'ABS', 'AutoCorr', 'ApproxEnt', 'Entrop', 'Complexity', 'countAboveMn',
#                'countBelowMn', 'fft_agg', 'event/min']

    data2show_comp=(((10,3),(10,10),(9,3),(9,11),(8,2),(8,3),(7,3),(6,3),(5,3),(5,10),(4,2),(4,10),(3,3),(3,10),(3,7),(2,3),(2,10),(1,2)))
    feat.feat_pca(feat.feat_exract(data2show_comp))




