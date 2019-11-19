# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 17:54:42 2019

@author: h.corbille
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:53:18 2019

@author: p.verborg
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob 
import os 

#foldername = r"D:\\freshStart\\0.data\\ICM20948_evaluation\\at_rest\\2803_logger_test\\"
#foldername = r"E:\\flight_29mars2019_103042\\"
#foldername = r"D:\\VirtualMachines\\common\\raspLoggerData\\11avr18h\\"
#foldername = r"D:\###HERE###\1. R&D\3. Data\formation_leo\flight_16avril2019_171024"
#foldername = r"E:\flight_24avril2019_163835"
#foldername = r"D:\###HERE###\1. R&D\3. Data\formation_leo\flight_29avril2019_171339"

foldername = "C:\\Users\\h.corbille\\Desktop\\Safetyn\\Data_processing\\Data_test_filtering"

#if not os.path.isdir(foldername + r"\\processed"):
#    os.mkdir(foldername + r"\\processed")

basename1000 = "numData_1000ms_"
basename100 = "numData_100ms_"
basename10 = "numData_10ms_"
basename5 = "numData_5ms_"

#headerImu = ['t_log', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz', 't']

#############
# 5ms files #
#############
fileList = glob.glob(foldername + '\\' + basename5 + '*.csv')
fileList = sorted(fileList, key = lambda filename : int(filename[len(foldername + '\\' + basename5):-4]))
datasetsList = []
if fileList:
    for file in fileList:
        datasetsList.append(pd.read_csv(file, sep =";", skiprows = 1, header = None))
    
    imuData = pd.concat(datasetsList, axis = 0, ignore_index = True)
    imuData.columns = pd.read_csv(fileList[0], nrows = 1, sep = ';').columns
    imuData.to_csv(foldername+ '\\' + basename5, sep = ';', index=False)
    del imuData

##############
# 10ms files #
##############
fileList = glob.glob(foldername + '\\' + basename10 + '*.csv')
fileList = sorted(fileList, key = lambda filename : int(filename[len(foldername + '\\' + basename10):-4]))
datasetsList = []
if fileList:
    for file in fileList:
        datasetsList.append(pd.read_csv(file, sep =";", skiprows = 1, header = None))
    
    imuData = pd.concat(datasetsList, axis = 0, ignore_index = True)
    imuData.columns = pd.read_csv(fileList[0], nrows = 1, sep = ';').columns
    imuData.to_csv(foldername+ '\\' + basename10, sep = ';', index=False)
    del imuData

###############
# 100ms files #
###############
fileList = glob.glob(foldername + '\\' + basename100 + '*.csv')
fileList = sorted(fileList, key = lambda filename : int(filename[len(foldername + '\\' + basename100):-4]))
datasetsList = []
if fileList:
    for file in fileList:
        datasetsList.append(pd.read_csv(file, sep =";", skiprows = 1, header = None))
    
    ahrsData = pd.concat(datasetsList, axis = 0, ignore_index = True)
    ahrsData.columns = pd.read_csv(fileList[0], nrows = 1, sep = ';').columns
    ahrsData.to_csv(foldername+ '\\' + basename100, sep = ';', index=False)
    del ahrsData

#################
## 1000ms files #
#################
fileList = glob.glob(foldername + '\\' + basename1000 + '*.csv')
fileList = sorted(fileList, key = lambda filename : int(filename[len(foldername + '\\' + basename1000):-4]))
datasetsList = []
if fileList:
    for file in fileList:
        datasetsList.append(pd.read_csv(file, sep =";", skiprows = 1, header = None))
    
    gpsData = pd.concat(datasetsList, axis = 0, ignore_index = True)
    gpsData.columns = pd.read_csv(fileList[0], nrows = 1, sep = ';').columns
    gpsData.to_csv(foldername+ '\\' + basename1000, sep = ';', index=False)
    del gpsData