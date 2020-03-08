# -*- coding: utf-8 -*-
"""
This file contains utility functions for final plots
"""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       IMPORTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import matplotlib.pyplot as plt
import matplotlib.patches as pcs

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       CONSTANTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Constants
circle_radius = .05
box_height = .1

energy_color = 'k'
tete_fixe_height = .8
tete_fixe_color = 'r'
tete_fixe_aoi_height = .6
tete_fixe_aoi_color = (1., 0.27, 0)
traffic_search_height = .4
traffic_search_color = 'b'
turn_height = .2
turn_color = 'g'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       GLOBAL VARIABLES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Global variable
xx, yy = 1., 1.
rect_height = .1

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def create_rect(height, begin, end, color, alpha=1., hatch=None):
    """
    Clearer function to plot a rectangle on a plot.

    Parameters
    ----------
    height : float Range([0, 1])
        Height of the rectangle.
    begin : float
        Time at which the rectangle begins.
    end : float
        Time at which the rectangle ends.
    color : Color
        Color of the rectangle.
    alpha : float Range([0, 1]), optional
        Rectangle opacity. The default is 1..
    hatch : char, optional
        Rectangle hatch. The default is None.

    Returns
    -------
    rect : Rectangle
        Created rectangle.

    """
    rect = pcs.Rectangle((begin, height * yy - 0.5 * rect_height), end - begin, rect_height, linewidth=0, edgecolor=None, facecolor=color, alpha=alpha, hatch=hatch)
    return rect

def create_circle(xy, radius, color, alpha=1., hatch=None):
    """
    Create an ellipse shaped that looks like a circle with the axis scale stretch.

    Parameters
    ----------
    xy : tuple
        Center of the circle.
    radius : float
        Circle radius.
    color : Color
        Circle color.
    alpha : float Range([0, 1]), optional
        Circle opacity. The default is 1..
    hatch : char, optional
        Circle hatch. The default is None.

    Returns
    -------
    circle : Ellipse
        Created circle.

    """
    circle = pcs.Ellipse(xy, circle_radius * xx , circle_radius * yy , color=color, alpha=alpha, hatch=hatch)
    return circle

def globalPlot(energy, tete_fixe=None, tete_fixe_aoi=None, traffic_search=None, turn=None):
    """
    Create the global plot containing:
        - Energy
        - Fix head intervals
        - Fix head AOI intervals
        - Traffic search intervals
        - Turn intervals

    Parameters
    ----------
    energy : DataFrame
        Energy data.
    tete_fixe : DataFrame, optional
        Fix head data. The default is None.
    tete_fixe_aoi : DataFrame, optional
        Fix head AOI data. The default is None.
    traffic_search : DataFrame, optional
        Traffic search data. The default is None.
    turn : DataFrame, optional
        Turn data. The default is None.

    Output
    -------
    Global plot.

    """
    fig, ax = plt.subplots(1)

    # Energy plot
    x = energy["FD_TIME_S"]
    y = energy["e_mean"]
    # Scale
    global xx
    global yy
    global rect_height
    xx, yy = max(x), max(y)
    rect_height = box_height * yy

    energy_line, = ax.plot(x, y, energy_color + '-')

    # Create patches
    if tete_fixe is not None:
        for (begin, end) in tete_fixe:
            rectangle = create_rect(tete_fixe_height, begin, end, tete_fixe_color, alpha=0.8)
            ax.add_patch(rectangle)

    if tete_fixe_aoi is not None:
        for (begin, end) in tete_fixe_aoi:
            rectangle = create_rect(tete_fixe_aoi_height, begin, end, tete_fixe_aoi_color, alpha=0.8)
            ax.add_patch(rectangle)

    if traffic_search is not None:
        for (begin, end) in traffic_search:
            circle = create_circle((0.5 * (begin + end), traffic_search_height * yy), circle_radius * yy, traffic_search_color, alpha=0.8)
            ax.add_patch(circle)

    if turn is not None:
        for (begin, end) in turn:
            rectangle = create_rect(turn_height, begin, end, turn_color, alpha=0.8)
            ax.add_patch(rectangle)

    # Legend
    energy_patch = pcs.Patch(color=energy_color, label='Energy')
    tete_fixe_patch = pcs.Patch(color=tete_fixe_color, label='Fix head')
    traffic_search_patch = pcs.Patch(color=traffic_search_color, label='Traffic search')
    turn_patch = pcs.Patch(color=turn_color, label='Turns')
    ax.legend(handles=[energy_patch, tete_fixe_patch, traffic_search_patch, turn_patch])

    ax.set_title("Energy / turns / fix heads")

    ax.grid()
    plt.show()
