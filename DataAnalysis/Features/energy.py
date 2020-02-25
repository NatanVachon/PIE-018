# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:13:36 2020

@author: Simon
"""


import scipy.signal
import matplotlib.pyplot as plt
import numpy as np
def energy(data, rolling_mean):
    energy=data[["FD_TIME_S","FD_GYRO_X","FD_GYRO_Y","FD_GYRO_Z"]]
    energy["E"]=(energy.loc[:, "FD_GYRO_X"].pow(2)+energy.loc[:, "FD_GYRO_Y"].pow(2)+energy.loc[:, "FD_GYRO_Z"].pow(2)).apply(np.sqrt)
    energy["e_mean"]=energy.E.rolling(rolling_mean).mean()
    energy = energy.fillna(0.)
    energy["e_mean"].plot()
    mean_energy=energy["E"].sum()/(data["FD_TIME_S"].max())
    peak=scipy.signal.find_peaks(energy["E"],height=0.05*max(energy["E"]),distance=100)
    plt.scatter(x=peak[0],y=peak[1]['peak_heights'])
    return energy[["FD_TIME_S", "e_mean"]],peak,mean_energy