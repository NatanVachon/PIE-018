# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:07:03 2020

@author: natan
"""

import matplotlib.pyplot as plt
import matplotlib.patches as pcs
import numpy as np

# Constants
circle_radius = .1
box_height = .1

# Global variable
xx, yy = 1., 1.

def create_rect(height, begin, end, color, alpha=1., hatch=None):
    rect = pcs.Rectangle((begin, height - 0.5 * rect_height), end - begin, rect_height, linewidth=0, edgecolor=None, facecolor=color, alpha=alpha, hatch=hatch)
    return rect

def create_circle(xy, radius, color, alpha=1., hatch=None):
    circle = pcs.Ellipse(xy, circle_radius * xx , circle_radius * yy , color=color, alpha=alpha, hatch=hatch)
    return circle

def globalPlot(energy, tete_fixe, tete_fixe_aoi, traffic_search, turn):
    fig, ax = plt.subplots(1)

    x = np.linspace(0., 10., 100)
    y = x ** 2

    ax.plot(x, y, 'r-')

    xx, yy = max(x), max(y)
    rect_height = box_height * yy

    rect = create_rect(0.8 * yy, 6., 8., 'g', alpha=0.8)
    circle = create_circle((5, 5), 0.1 * yy, 'r', alpha=0.8, hatch='/')

    ax.add_patch(rect)
    ax.add_patch(circle)
    plt.show()
