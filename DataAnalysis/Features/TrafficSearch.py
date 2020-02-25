# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:15:43 2020

@author: natan
"""
############################################ IMPORTS ############################################
import Constants as const

############################################ FUNCTIONS ############################################

# function name: traffic_search
# Inputs:
#   data [DataFrame]: Onboard measurements with AOI column attached
#   date [float]: Moment at which we check if a traffic search happened (in seconds)
# Output:
#   [bool] Is the traffic search done

def traffic_search(data, t1, t2):
    """

    Parameters
    ----------
    data : DataFrame
        Onboard measurements with AOI column attached.
    t1 : float
        Begin date of the search period.
    t2 : float
        End date of the search period.

    Returns
    -------
    bool
        Is the traffic search done ?

    """

    # Get closest index
    index_t1 = next((i for i in range(len(data)) if data.at[i, "FD_TIME_S"] > t1), None)
    index_t2 = next((i for i in range(len(data)) if data.at[i, "FD_TIME_S"] > t2), None)

    if index_t1 is None or index_t2 is None:
        print("Given date out of bounds")
        return None

    # Look for heading min and max between t1 and t2
    sub_list = data.loc[index_t1:index_t2, "FD_PILOT_HEAD_HEADING"]
    min_heading, max_heading = min(sub_list), max(sub_list)
    amplitude_check = max_heading - min_heading >= const.TRAFFIC_SEARCH_MIN_HEADING_AMPLITUDE
    #print("amplitude:", max_heading - min_heading)

    # Check that every AOI has been checked
    sub_list = data.loc[index_t1:index_t2, "AOI"].tolist()
    #print("sublist:", sub_list)
    aoi_check = 'L' in sub_list and 'F' in sub_list and 'R' in sub_list

    return amplitude_check and aoi_check