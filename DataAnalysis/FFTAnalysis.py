# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:45:12 2020

@author: natan
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import fft
from scipy.signal import find_peaks

name = "simon"
data_path = "d:/natan/Documents/PIE/Logs/flight_10Dec2019_" + name
data = pd.read_csv(data_path + "/numData_100ms.csv", sep=';')

print("Frequency analysis for " + name)

fs = 10. #Hz
x = data["FD_PILOT_HEAD_PITCH"]
#x = data["FD_GYRO_Y"]
f = np.linspace(-0.5 * fs, 0.5 * fs, len(x))
N = len(x)

# FFT
xFFT = fft.fftshift(fft.fft(x))
xFFT, f = xFFT[N//2:], f[N//2:] # Keep half of the fft
xFFT = abs(xFFT) # Take modulus
xFFT = xFFT / float(len(x)) #Normalization

# Peak finder
peak_threshold = 0.8 * max(xFFT[1:])
peakIndexes = find_peaks(xFFT[1:], height=peak_threshold)
peakFrequencies, peakValues = [f[i] for i in peakIndexes[0]], [xFFT[i] for i in peakIndexes[0]]
print("Peaks:", peakFrequencies)

plt.figure()
plt.plot(f[1:N//10], xFFT[1:N//10])
plt.title(name)
plt.xlabel("Frequency [Hz]")
plt.ylabel("FFT modulus")
plt.grid()
plt.show()