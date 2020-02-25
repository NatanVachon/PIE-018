# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:07:03 2020

@author: natan
"""

import matplotlib.pyplot as plt
import matplotlib.patches as pcs
import numpy as np

# Constants
circle_radius = .08
box_height = .1

tete_fixe_height = .8
tete_fixe_color = 'r'
tete_fixe_aoi_height = .6
tete_fixe_aoi_color = (1., 0.27, 0)
traffic_search_height = .4
traffic_search_color = 'b'
turn_height = .2
turn_color = 'g'

# Global variable
xx, yy = 1., 1.
rect_height = .1

def create_rect(height, begin, end, color, alpha=1., hatch=None):
    rect = pcs.Rectangle((begin, height - 0.5 * rect_height), end - begin, rect_height, linewidth=0, edgecolor=None, facecolor=color, alpha=alpha, hatch=hatch)
    return rect

def create_circle(xy, radius, color, alpha=1., hatch=None):
    circle = pcs.Ellipse(xy, circle_radius * xx , circle_radius * yy , color=color, alpha=alpha, hatch=hatch)
    return circle

def globalPlot(energy, tete_fixe=None, tete_fixe_aoi=None, traffic_search=None, turn=None):
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

    ax.plot(x, y, 'k-')

    # Create patches
    if tete_fixe is not None:
        for (begin, end) in tete_fixe:
            rectangle = create_rect(tete_fixe_height * yy, begin, end, tete_fixe_color, alpha=0.8)
            ax.add_patch(rectangle)

    if tete_fixe_aoi is not None:
        for (begin, end) in tete_fixe_aoi:
            rectangle = create_rect(tete_fixe_aoi_height * yy, begin, end, tete_fixe_aoi_color, alpha=0.8)
            ax.add_patch(rectangle)

    if traffic_search is not None:
        for (begin, end) in traffic_search:
            circle = create_circle((0.5 * (begin + end), traffic_search_height * yy), circle_radius * yy, traffic_search_color, alpha=0.8)
            ax.add_patch(circle)

    if turn is not None:
        for (begin, end) in turn:
            rectangle = create_rect(turn_height * yy, begin, end, turn_color, alpha=0.8)
            ax.add_patch(rectangle)

    plt.grid()
    plt.show()
