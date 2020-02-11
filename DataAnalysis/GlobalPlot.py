# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:07:03 2020

@author: natan
"""

import matplotlib.pyplot as plt
import matplotlib.patches as pcs
import numpy as np

# Global constants
rect_height = 0.

def create_rect(height, begin, end, color, alpha=1., hatch=None):
    rect = pcs.Rectangle((begin, height - 0.5 * rect_height), end - begin, rect_height, linewidth=1, edgecolor='k', facecolor=color, alpha=alpha, hatch=hatch)
    return rect

if __name__ == "__main__":
    fig, ax = plt.subplots(1)

    x = np.linspace(0., 10., 100)
    y = x**2

    ax.plot(x, y, 'r-')

    max_value = max(y)
    rect_height = 0.1 * max_value

    rect = create_rect(0.8 * max_value, 6., 8., 'g', alpha=0.7)

    ax.add_patch(rect)
    plt.show()