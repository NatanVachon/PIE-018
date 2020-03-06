# -*- coding: utf-8 -*-
"""
This file contains feature function for energy.
"""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       IMPORTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from scipy.signal import find_peaks
import numpy as np

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def energy(data, rolling_mean):
    """
    Computes the gyroscope signal energy.

    Parameters
    ----------
    data : DataFrame
        Flight data.
    rolling_mean : int
        Length of the rolling mean window length.

    Returns
    -------
    energy : DataFrame
        DataFrame containing timestamps and energy values.
    peak : float
        Value of the highest energy spike.
    mean_energy : float
        Mean energy on dataset.

    """
    energy = data[["FD_TIME_S","FD_GYRO_X","FD_GYRO_Y","FD_GYRO_Z"]]

    # Energy is the squared norm of the angular velocity vector
    energy["E"] = (energy.loc[:, "FD_GYRO_X"].pow(2)+energy.loc[:, "FD_GYRO_Y"].pow(2)+energy.loc[:, "FD_GYRO_Z"].pow(2)).apply(np.sqrt)

    # Computing mean and peaks
    energy["e_mean"] = energy.E.rolling(rolling_mean).mean()
    energy = energy.fillna(0.)
    mean_energy = energy["E"].sum()/(data["FD_TIME_S"].max())
    peak = find_peaks(energy["E"], height=0.05*max(energy["E"]), distance=100)

    return energy[["FD_TIME_S", "e_mean"]], peak, mean_energy