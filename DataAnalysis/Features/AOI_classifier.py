# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:38:23 2019

@author: natan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       CLASSES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Zone:
    def __init__(self, name, xMin, xMax, yMin, yMax):
        self.name = name
        self.x = [xMin, xMax]
        self.y = [yMin, yMax]

        self.meshX, self.meshY = np.meshgrid(self.x, self.y)

    def inZone(self, x, y):
        return x >= self.x[0] and x < self.x[1] and y >= self.y[0] and y < self.y[1]


class ZoneGraphics:
    def __init__(self, zone, color):
        self.name = zone.name
        # Store zone
        self.zone = zone
        # Create color
        colorMap = LinearSegmentedColormap.from_list(self.name + "_color", [color, color, color], N=1)
        # Create plot
        self.pcolor = plt.pcolor(self.zone.meshX, self.zone.meshY, np.ones((2, 2)), cmap=colorMap, alpha=0.2)

    def set_alpha(self, alpha):
        self.pcolor.set_alpha(alpha)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def compute_zones(data, poi):
    timestamps = []
    # Get index for each poi
    for k in range(len(poi)):
        timestamps.append(next(i for i in data.index if data.at[i, "FD_TIME_MS"] > poi.at[k, "FD_TIME_MS"]))

    # Get point for each poi
    pitches, headings = [data.at[i, "FD_PILOT_HEAD_PITCH"] for i in timestamps], [data.at[i, "FD_PILOT_HEAD_HEADING"] for i in timestamps]

    # Define zones
    zone_left = Zone('L', -180, headings[5], -180, 180)
    zone_front = Zone('F', headings[5], headings[6], pitches[4], pitches[3])
    zone_right = Zone('R', headings[6], 180, -180, 180)
    zone_i1 = Zone('P', headings[5], headings[9], pitches[7], pitches[4])
    zone_i2 = Zone('S', headings[9], headings[6], pitches[7], pitches[4])

    return [zone_left, zone_front, zone_right, zone_i1, zone_i2]

def classify_aoi(zones, pitch, heading):
    for i in range(len(zones)):
        if zones[i].inZone(heading, pitch):
            return zones[i].name

    # If not in any zone
    return 'N'

def classify_aois(zones, data):
    aois = [classify_aoi(zones, data.at[i, "FD_PILOT_HEAD_PITCH"], data.at[i, "FD_PILOT_HEAD_HEADING"]) for i in range(len(data))]
    df = pd.DataFrame()
    df["timestamp"] = data["FD_TIME_MS"]
    df["AOI"] = aois

    # Save aois in data
    data["AOI"] = aois
    return df

