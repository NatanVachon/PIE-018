# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:12:29 2019

@author: natan
"""

import AOI_classifier as aoic
from AOI_classifier import ZoneGraphics

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

data_path = "d:/natan/Documents/PIE/Logs/flight_10Dec2019_guilhem"

data = pd.DataFrame()
poi = pd.DataFrame()

fig, ax = plt.subplots()
pt, = plt.plot([], [], "ko")

def init_animation():
    ax.set_xlim(-90, 90)
    ax.set_ylim(-45, 45)

    ax.set_xlabel("Heading angle [°]")
    ax.set_ylabel("Pitch angle [°]")
    ax.grid()
    ax.set_title("Cross calibration")
    return [pt, gZone_left.pcolor, gZone_right.pcolor, gZone_front.pcolor, gZone_zi1.pcolor, gZone_zi2.pcolor]

def update_animation(frame):
    # Plot sight point
    x, y = data.at[frame, "FD_PILOT_HEAD_HEADING"], data.at[frame, "FD_PILOT_HEAD_PITCH"]
    xdata = [x]
    ydata = [y]

    # Update surbrillance
    update_surbrillance(y, x)

    #Update plot
    pt.set_data(xdata, ydata)
    return [pt, gZone_left.pcolor, gZone_right.pcolor, gZone_front.pcolor, gZone_zi1.pcolor, gZone_zi2.pcolor]

def get_poi_timestamps(data, poi):
    timestamps = []

    for k in range(len(poi)):
        timestamps.append(next(i for i in data.index if data.at[i, "FD_TIME_MS"] > poi.at[k, "FD_TIME_MS"]))

    return timestamps

def update_surbrillance(pitch, heading):
    gZone_left.set_alpha(0.2)
    gZone_right.set_alpha(0.2)
    gZone_front.set_alpha(0.2)
    gZone_zi1.set_alpha(0.2)
    gZone_zi2.set_alpha(0.2)

    index = aoic.classify_aoi(zones, pitch, heading)

    if index == 'L':
        gZone_left.set_alpha(0.7)
    elif index == 'R':
        gZone_right.set_alpha(0.7)
    elif index == 'F':
        gZone_front.set_alpha(0.7)
    elif index == 'P':
        gZone_zi1.set_alpha(0.7)
    elif index == 'S':
        gZone_zi2.set_alpha(0.7)
    return

if __name__ == "__main__":
    # Initialization
    data = pd.read_csv(data_path + "/numData_100ms.csv", sep=';')
    poi = pd.read_csv(data_path + "/flightEvent0.csv", sep=';')
    poi_timestamps = get_poi_timestamps(data, poi)

    # Zones definition
    zones = aoic.compute_zones(data, poi)
    gZone_left = ZoneGraphics(zones[0], (1, 0, 0))
    gZone_front = ZoneGraphics(zones[1], (0, 1, 0))
    gZone_right = ZoneGraphics(zones[2], (1, 1, 0))
    gZone_zi1 = ZoneGraphics(zones[3], (0, 0, 1))
    gZone_zi2 = ZoneGraphics(zones[4], (0, 1, 1))

    # Launch animation
    ani = FuncAnimation(fig, update_animation, init_func=init_animation, frames=[i for i in range(len(data))], blit=True, interval = 25)
    plt.show()