# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:45:12 2020

@author: natan
"""

#from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

name = "guilhem"
data_path = "d:/natan/Documents/PIE/Logs/flight_10Dec2019_" + name
data = pd.read_csv(data_path + "/numData_100ms.csv", sep=';')

fs = 10 #Hz
#x = data["FD_GYRO_Y"]
x = data["FD_PILOT_HEAD_PITCH"]

# f, t, Sxx = signal.spectrogram(x, fs)
# plt.pcolormesh(t, f, Sxx)
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()

# FFT
xFFT = np.fft.fftshift(np.fft.fft(x))
xFFT = xFFT[len(xFFT)//2:]

# First peak comparison


f = np.linspace(0., 5., len(xFFT))
plt.figure()
plt.plot(f[1:len(f)//5], abs(xFFT[1:len(xFFT)//5]))
plt.title(name)
plt.xlabel("Frequency [Hz]")
plt.ylabel("FFT modulus")
plt.grid()
plt.show()