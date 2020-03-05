# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:13:24 2020

@author: natan
"""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       IMPORTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#d'une fonction qui marche entre t1 et t2 est appelée pour
#detecter toutes les plages supérieures à threshold surlesquels c'est vrai
def largest_lookup(fonction, data, threshold):
    """
    Used to compute largest intervals on which a function is evaluated to true.

        example :
    Data FD_TIME_S :0-----ta--ta+4-------tb----tb+7-------tc----tc+7-----end
        Ftest      :000000111100000000011111110000000000111111100000000
    largest_lookup(Ftest,data,5) will return [(tb,tb+7),(tc,tc+7)]

    Parameters
    ----------
    fonction : bool function(data, t1, t2)
        function to evaluate.
    data : DataFrame
        Flight data.
    threshold : float
        Time threshold defining a minimum time on which the function
        have to be true to be added to the final interval.

    Returns
    -------
    true2 : TYPE
        DESCRIPTION.

    """

    # Look for intervals on which the function is evaluated to True
    true = []
    threshold_search = threshold / 2.0
    tr = False
    maxt = max(data["FD_TIME_S"]) - threshold_search
    ta = min(data["FD_TIME_S"])
    while ta<=maxt :
        tb = ta + threshold_search

        tr = fonction(data, ta, tb)

        if tr:
            true.append((ta, tb))
        ta = ta + threshold_search

    # Concatenation step
    true2 = []
    i = 0
    while i <= len(true) - 1:
        a = i
        while i <= len(true) - 2 and true[i][1] == true[i+1][0] :
            i += 1
        if true[i][1]-true[a][0] >= threshold :
            true2.append((true[a][0], true[i][1]))
        i += 1
    return true2


def smallest_lookup(function, data, N=10):
    """
    TODO: TERMINER

    Parameters
    ----------
    function : bool function(data, t1, t2)
        Base function callable on an interval [t1, t2].
    data : DataFrame
        Flight data.
    N : int
        Number of subdivisions used in the algorithm.

    Returns
    -------
    disconnected_intervals : list of tuple.
        Each tuple represents an interval in which function(data, time[i], time[j]) is true.

    """
    time = list(data["FD_TIME_S"])
    t_begin, t_end = time[0], time[-1]

    vertices = np.linspace(t_begin, t_end, N)
    candidates = []

    # Look for each couple (i, j) such that f(i, j) is True
    for j in range(1, len(vertices)):
        for i in range(j):
            if function(data, vertices[i], vertices[j]):
                candidates.append((i, j))

    # Check for solution existence
    if len(candidates) == 0:
        return None

    # Sort each couple with distance j - i
    comp = lambda ij: ij[1] - ij[0] # Comparator is the interval length
    candidates = sorted(candidates, key=comp)

    # For each couple in candidates, keep the non intersecting ones
    disconnected_intervals = [candidates[0]]
    for candidate in candidates[1:]:
        intervals_copy = disconnected_intervals.copy()
        is_intersecting = False
        for interval in intervals_copy:
            # Verify that intervals are disjoint
            if not np.sign(candidate[0] - interval[0]) == np.sign(candidate[0] - interval[1])  \
            == np.sign(candidate[1] - interval[0]) == np.sign(candidate[1] - interval[1]):
                is_intersecting = True
                break

        if not is_intersecting:
            disconnected_intervals.append(candidate)

    # At this point, disconnected intervals contains smaller disconnected intervals such that f(i, j) is True