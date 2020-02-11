# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:13:36 2020

@author: Simon
"""


import scipy.signal
import matplotlib.pyplot as plt 
def energy(data):
    energy=data[["FD_TIME_MS","FD_GYRO_X","FD_GYRO_Y","FD_GYRO_Z"]]
    energy["E"]=energy["FD_GYRO_X"].pow(2)+energy["FD_GYRO_Y"].pow(2)+energy["FD_GYRO_Z"].pow(2)
    energy["e_mean"]=energy.E.rolling(20).mean()
    energy["e_mean"].plot()
    peak=scipy.signal.find_peaks(energy["E"],height=0.05*max(energy["E"]),distance=100)
    plt.scatter(x=peak[0],y=peak[1]['peak_heights'])
    return energy["e_mean"],peak