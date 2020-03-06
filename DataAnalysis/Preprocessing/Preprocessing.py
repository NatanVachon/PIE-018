
"""
This file contains functions used to prepare data before feature computations.
"""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                                       FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def data_preprocessing(data, poi):
    """
    Function used to format raw flight data

    Parameters
    ----------
    data : DataFrame
        Raw flight data.
    poi : DataFrame
        Points of interest.

    Returns
    -------
    data : DataFrame
        Formated flight data.
    poi : DataFrame
        Formated points of interest.

    """
    # Used to remove freezes at the begining of the logs
    data = data.drop_duplicates(subset = "FD_PILOT_HEAD_PITCH")
    data = data.reset_index(drop = True)

    # Sets the begin timestamp to 0s and convert milliseconds to seconds
    t0 = data.at[0, "FD_TIME_MS"]

    data["FD_TIME_MS"].astype("float")
    data["FD_TIME_MS"] -= t0
    data["FD_TIME_MS"] *= 0.001
    data = data.rename(columns={"FD_TIME_MS": "FD_TIME_S"})

    poi["FD_TIME_MS"].astype("float")
    poi["FD_TIME_MS"] -= t0
    poi["FD_TIME_MS"] *= 0.001
    poi = poi.rename(columns={"FD_TIME_MS": "FD_TIME_S"})

    return data, poi