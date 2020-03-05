# -*- coding: utf-8 -*-
"""
This file contains functions and classes about AOI definitions and use.
"""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       IMPORTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       CLASSES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Zone:
    """ Represents an area of interest """
    def __init__(self, name, xMin, xMax, yMin, yMax):
        self.name = name
        self.x = [xMin, xMax]
        self.y = [yMin, yMax]

        self.meshX, self.meshY = np.meshgrid(self.x, self.y)

    def inZone(self, x, y):
        """
        Checks if the tested point (x, y) is in the zone.

        Parameters
        ----------
        x : float
            Heading of tested point.
        y : float
            Pitch of tested point.

        Returns
        -------
        Bool
            Is the tested point in the zone ?
        """
        return x >= self.x[0] and x < self.x[1] and y >= self.y[0] and y < self.y[1]


class ZoneGraphics:
    """ Graphical representation of area of interest for visualization """
    def __init__(self, zone, color):
        self.name = zone.name
        # Store zone
        self.zone = zone
        # Create color
        colorMap = LinearSegmentedColormap.from_list(self.name + "_color", [color, color, color], N=1)
        # Create plot
        self.pcolor = plt.pcolor(self.zone.meshX, self.zone.meshY, np.ones((2, 2)), cmap=colorMap, alpha=0.2)

    def set_alpha(self, alpha):
        """
        Sets the alpha value for visualization.

        Parameters
        ----------
        alpha : float Range([0, 1])
            Alpha value.

        """
        self.pcolor.set_alpha(alpha)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def compute_zones(data, poi):
    """
    Computes calibration zones from flight data and point of interests.

    Parameters
    ----------
    data : DataFrame
        Calibration data.
    poi : DataFrame
        Points of interest timestamps.

    Returns
    -------
    list of Zone
        List containing the five area of interests 'L', 'F', 'R', 'P' and 'S'.

    """
    timestamps = []
    # Get index for each poi
    for k in range(len(poi)):
        timestamps.append(next(i for i in data.index if data.at[i, "FD_TIME_S"] > poi.at[k, "FD_TIME_S"]))

    # Get point for each poi
    pitches, headings = [data.at[i, "FD_PILOT_HEAD_PITCH"] for i in timestamps], [data.at[i, "FD_PILOT_HEAD_HEADING"] for i in timestamps]

    # Define zones
    zone_left = Zone('L', -180., headings[3], -180., 180.)
    zone_front = Zone('F', headings[3], headings[4], pitches[2], pitches[1])
    zone_right = Zone('R', headings[4], 180., -180., 180.)
    zone_i1 = Zone('P', headings[3], headings[7], -90., pitches[2])
    zone_i2 = Zone('S', headings[7], headings[4], -90., pitches[2])

    return [zone_left, zone_front, zone_right, zone_i1, zone_i2]

def classify_aoi(zones, pitch, heading):
    """
    Tests in which zone is the point (heading, pitch).
    Returns 'N' zone if the point is in no zone.

    Parameters
    ----------
    zones : list of Zone
        List of the five AOIs.
    pitch : float
        Tested point pitch.
    heading : float
        Tested point heading.

    Returns
    -------
    char
        Returns the character corresponding to the zone in which the point is
        'L', 'F', 'R', 'P' or 'S'.

    """
    # Check for each zone if we are in
    for i in range(len(zones)):
        if zones[i].inZone(heading, pitch):
            return zones[i].name

    # Else return Null
    return 'N'

def classify_aois(zones, data):
    """
    Same function as classify_aoi but callable on a whole dataframe of flight data.

    Parameters
    ----------
    zones : list of Zone
        List of the five AOIs.
    data : DataFrame
        Flight data.

    Returns
    -------
    df : DataFrame
        A dataframe with two columns .

    """
    aois = [classify_aoi(zones, data.at[i, "FD_PILOT_HEAD_PITCH"], data.at[i, "FD_PILOT_HEAD_HEADING"]) for i in range(len(data))]
    df = pd.DataFrame()
    df["FD_TIME_S"] = data["FD_TIME_S"]
    df["AOI"] = aois

    # Save aois in data
    data["AOI"] = aois
    return df

