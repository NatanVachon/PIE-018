# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:38:23 2019

@author: natan
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       CLASSES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Zone:
    def __init__(self, xMin, xMax, yMin, yMax):
        self.x = [xMin, xMax]
        self.y = [yMin, yMax]

        self.meshX, self.meshY = np.meshgrid(self.x, self.y)

    def inZone(self, x, y):
        return x >= self.x[0] and x < self.x[1] and y >= self.y[0] and y < self.y[1]


class ZoneGraphics:
    def __init__(self, name, zone, color):
        self.name = name
        # Store zone
        self.zone = zone
        # Create color
        colorMap = LinearSegmentedColormap.from_list(self.name + "_color", [color, color, color], N=1)
        # Create plot
        self.pcolor = plt.pcolor(self.zone.meshX, self.zone.meshY, np.ones((2, 2)), cmap=colorMap, alpha=0.2)

    def set_alpha(self, alpha):
        self.pcolor.set_alpha(alpha)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       CONSTANTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# AOI boundaries
AOI_LEFT   = -90 #[°]
AOI_MIDDLE = 0 #[°]
AOI_RIGHT  = 90 #[°]
AOI_TOP    = 40 #[°]
AOI_FRONT  = -20 #[°]
AOI_BOTTOM = -40 #[°]

# AOI indexes
LEFT = 0
RIGHT = 1
FRONT = 2
ZI1 = 3
ZI2 = 4

# AOI zones
leftZone = Zone(AOI_LEFT, AOI_MIDDLE, AOI_FRONT, AOI_TOP)
rightZone = Zone(AOI_MIDDLE, AOI_RIGHT, AOI_FRONT, AOI_TOP)
zi1Zone = Zone(AOI_LEFT, AOI_MIDDLE, AOI_BOTTOM, AOI_FRONT)
zi2Zone = Zone(AOI_MIDDLE, AOI_RIGHT, AOI_BOTTOM, AOI_FRONT)

AOI_zones = [leftZone, rightZone, zi1Zone, zi2Zone]


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
    zone_left = Zone(headings[1], headings[5], -90, 90)
    zone_front = Zone(headings[5], headings[6], pitches[4], pitches[3])
    zone_right = Zone(headings[6], headings[2], -90, 90)
    zone_i1 = Zone(headings[8], headings[9], pitches[7], pitches[4])
    zone_i2 = Zone(headings[9], headings[10], pitches[7], pitches[4])

    # TODO: supprimer
    print(headings[0], pitches[0])

    return [zone_left, zone_front, zone_right, zone_i1, zone_i2]

def classify_aoi(zones, pitch, heading):
    for i in range(len(zones)):
        if zones[i].inZone(heading, pitch):
            return i

    # If not in any zone
    return None

def classify_aois(zones, pitchs, headings):
    return [classify_aoi(zones, pitch, heading) for (pitch, heading) in (pitchs, headings)]

