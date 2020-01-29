# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:15:43 2020

@author: natan
"""

############################################ PARAMETERS ############################################
TS_DURATION = 20 #[s]
TS_MIN_HEADING_AMPLITUDE = 180 #[°]

############################################ FUNCTIONS ############################################

# function name: traffic_search
# Inputs:
#   data [DataFrame]: Onboard measurements with AOI column attached
#   date [float]: Moment at which we check if a traffic search happened (in seconds)
# Output:
#   [bool] Is the traffic search done

def traffic_search(data, date):
    # Get closest index
    index = next((i for i in range(len(data)) if data.at[i, "FD_TIME_MS"] > date), None)
    if index is None:
        print("Given date out of bounds")

    # Look for heading min and max at +/- TS_DURATION / 2
    dindex = int(TS_DURATION / 0.1 / 2) # Convertion from time to indexes
    sub_list = data.loc[index - dindex: index + dindex, "FD_PILOT_HEAD_HEADING"]
    min_heading, max_heading = min(sub_list), max(sub_list)
    amplitude_check = max_heading - min_heading >= TS_MIN_HEADING_AMPLITUDE

    # Check that every AOI has been checked
    sub_list = data.loc[index - dindex: index + dindex, "AOI"].tolist()
    aoi_check = 'L' in sub_list and 'F' in sub_list and 'R' in sub_list

    return amplitude_check and aoi_check