# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:12:29 2019

@author: natan
"""
import PlanePhysics as pp

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

data_path = "d:/natan/Documents/PIE/Logs/1211_test_protocole/1211_Guilhem_gauche"

data = pd.DataFrame()
poi = pd.DataFrame()

fig, ax = plt.subplots()
red, = plt.plot([], [], "ro")
green, = plt.plot([], [], "go")
xred, yred = [], []
xgreen, ygreen = [], []

def init_animation():
    ax.set_xlim(-180, 180)
    ax.set_ylim(-7.5, 1.5)

    ax.set_xlabel("Heading angle [°]")
    ax.set_ylabel("Pitch projection [m]")
    return [red, green]

def update_animation(frame):
    # Check if we have to draw
    if frame > poi_timestamps[1] and frame < poi_timestamps[2]:
        return [red, green]

    if frame <= poi_timestamps[1]:
        ln = red
        xdata, ydata = xred, yred

    else:
        ln = green
        xdata, ydata = xgreen, ygreen

    # Get point on cockpit glass
    x, y = data.at[frame, "FD_PILOT_HEAD_HEADING"], pp.project_pitch(data.at[frame, "FD_PILOT_HEAD_PITCH"])
    xdata.append(x)
    ydata.append(y)

    #Update plot
    ln.set_data(xdata, ydata)
    return [red, green]

def get_poi_timestamps(data, poi):
    timestamps = []

    for k in range(len(poi)):
        timestamps.append(next(i for i in data.index if data.at[i, "FD_TIME_MS"] > poi.at[k, "FD_TIME_MS"]))

    return timestamps


if __name__ == "__main__":
    # Initialization
    data = pd.read_csv(data_path + "/numData_10ms.csv", sep=';')
    poi = pd.read_csv(data_path + "/flightEvent.csv", sep=';')
    poi_timestamps = get_poi_timestamps(data, poi)

    # Launch animation
    ani = FuncAnimation(fig, update_animation, init_func=init_animation, frames=[i for i in range(poi_timestamps[0], poi_timestamps[3])], blit=True, interval = 5)
    plt.grid()
    plt.show()