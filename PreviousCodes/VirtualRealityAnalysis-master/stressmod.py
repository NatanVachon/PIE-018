# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:20:46 2019
Class Features for  :
    imports CSV
    performs feature extraction on windows
    display de analysis
V1

@author: Sylvain Zorman
"""

import tsfresh as ts
import pandas as pd
from matplotlib import pyplot
from scipy.signal import butter, filtfilt
import scipy as spy
import numpy as np
import pickle#inutil
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def butter_HLBpass(fcut, ftype, fs, order=1):
    """"coeficient Hihg Low, band pass filters

        fcut in a vector [Low,High]
        ftype is the type : low, high or band
        for low and high fctu is a single value, 2 for band
        fs is sampkling freq
        order is the order of the applied filter
    """
    nyq = 0.5 * fs
    b_fil, a_fil = butter(order, np.array(fcut) / nyq, btype=ftype)
    return b_fil, a_fil


def butter_HLB_Filt(data, fcut, ftype, fs, order=1):
    """perform both ways filtering

        Data is a vector
        fcut is an int for low or high pass filter an array of 2 for bandpass
        fs is sampling freq
        order is the order of filter
        Y is the filtered data
        """
    b_fil, a_fil = butter_HLBpass(fcut, ftype, fs, order=order)
    data_filt = filtfilt(b_fil, a_fil, data)
    return data_filt


def global_filt(feat_in):
    """perform adjusted global filt of the phy data

        input is a class Feature instance
        PZT(resp):0.1-2 Hz
        EDA: 0.05 1 Hz
        *to be implemented*BPM :  perform the extraction of rate from InterBeatMes no filter
    """
    if feat_in.type == 'phy':
        feat_in.filt_val[:, 0] = butter_HLB_Filt(feat_in.val[:, 0], [0.1, 2], 
                        'band', feat_in.fs, order=1)
        feat_in.filt_val[:, 2] = butter_HLB_Filt(feat_in.val[:, 2], [0.2, 0.8], 
                        'band', feat_in.fs, order=1)#PZT
        feat_in.filt_val[:, 3] = butter_HLB_Filt(feat_in.val[:, 3], [0.05, 1], 
                        'band', feat_in.fs, order=1)
    if feat_in.type == 'comp':
        for col in range(feat_in.val.shape[1]):
            feat_in.filt_val[:, col] = feat_in.val[:, col]# butter_HLB_Filt(feat_in.val[:, col], 1,'high', feat_in.fs, order=1)
    return

##############
# feat extract

def WdW_mn_crossing_up(X,fs):
    """will be implemented for PZT. Currently the signal is too poor for an ananylis
    """
    try:
        global_ENGY = np.mean(X**2)
        RMS = np.sqrt(np.mean(X**2))
        #1:mapping the signal with correct ENGY with a 1sec window
        RMS_map=np.zeros(len(X))
        loc_RMS=np.zeros(len(X)-int(20*fs))
        Xing_map=np.zeros(len(X), dtype=bool)
        k=0
        for i in  range(int(fs*10),len(X)-int(fs*10)):#implementation of rule 2
            loc_RMS[k]=np.mean(X[i-int(fs*10):i+int(fs*10)])
            RMS_map[i] = True#(loc_RMSY>0.25*global_RMS) & (loc_ENGY<0.75*global_ENGY)
            k=k+1
    
        for j in  range(int(fs*10),len(X)-int(fs*10)):#checking rule1
            #print(j)
            if True:#RMS_map[j]:#rule2
                if (X[j-1]-loc_RMS[j-int(fs*10)]) < 0 and (X[j]-
                   loc_RMS[j-int(fs*10)]) > 0:#both side of the RMS line
                   Xing_map[j]=True
        return Xing_map
    
    except:
        return np.zeros(len(X), dtype=bool)

def inter_beat_mes(data,fs):
    """compute the front montant et descendant
    
    generate time series with inter ups, downs or average of both values"""

    interval_up = 0
    interval_down = 0
    last_up = 0
    last_down = 0
    inter_beat_up = np.zeros(len(data))
    inter_beat_down = np.zeros(len(data))
    i = 0
    mn = np.mean(data)
    for val in data[1:]:
        if (data[i + 1] > mn) & (data[i] < mn):  # front montant
            interval_up = i - last_up
            last_up = i
        elif (data[i] > mn) & (data[i + 1] < mn):  # front descendant
            interval_down = i - last_down
            last_down = i
        inter_beat_up[i] = interval_up
        inter_beat_down[i] = interval_down
        i = i + 1
    return fs/np.mean(inter_beat_down[inter_beat_down!=0])*60


def add_end(vec, val):
    """add val at the end of a vector"""
    if np.size(vec) == 0:
        return val  # np.array([val])
    else:
        return np.vstack((vec, val))  # np.array([val])))


def add_line(vec, line):
    """add a line at the end of a np array"""
    if np.size(vec) == 0:
        return line  # np.array([val])
    else:
        return np.hstack((vec, line))  # np.array([val])))


def feat_extr_1D(data, fs, WdW):
    """this function  compute features by moving the window by halph the windows size each steps for a vector

    data is a timeseries
    fs: sampling rate
    WdW : the number of point of the analysis window"""
    if WdW % 2 != 0:
        print('Error: the windows size should be even')
        return
    # Init
    col_name = ['index', 'WdW Position', 'Ej', 'ABS', 'AutoCorr', 'ApproxEnt', 'Entrop', 'Complexity', 'countAboveMn',
                'countBelowMn', 'fft_agg', 'event/min']
    feats_info = np.arange(0, len(data), np.int(WdW / 2))
    feats_info = np.vstack((np.arange(0, feats_info.size), feats_info))
    feat_current = np.array([])
    feats = []
    for i in feats_info[1, :]:
        feat_current = np.array([])
        WdW_data = data[i:i + WdW]
        # looking at energy
        feat_current = add_end(feat_current,
                               ts.feature_extraction.feature_calculators.
                               abs_energy(WdW_data))    
        feat_current = add_end(feat_current, ts.feature_extraction.feature_calculators.
                               absolute_sum_of_changes(WdW_data))
        feat_current = add_end(feat_current, ts.feature_extraction.feature_calculators.
                               agg_autocorrelation(WdW_data, [{'f_agg': 'median', 'maxlag': np.int(WdW / 2)}])[0][1])
        # looking at entropy
        feat_current = add_end(feat_current, ts.feature_extraction.feature_calculators.
                               approximate_entropy(WdW_data, 2, 3))  # should optimize r it is someteing NaN

        feat_current = add_end(feat_current, ts.feature_extraction.feature_calculators.
                               sample_entropy(WdW_data))

        feat_current = add_end(feat_current, ts.feature_extraction.feature_calculators.
                               cid_ce(WdW_data, True))
        feat_current = add_end(feat_current, ts.feature_extraction.feature_calculators.
                               count_above_mean(WdW_data))
        feat_current = add_end(feat_current, ts.feature_extraction.feature_calculators.
                               count_below_mean(WdW_data))
        feat_current = add_end(feat_current,
                               list(ts.feature_extraction.feature_calculators.fft_aggregated(WdW_data, [
                                   {'aggtype': 'centroid'}]))[0][1])
        # should optimize r
        feat_current = add_end(feat_current, inter_beat_mes(WdW_data, fs))
        feats = add_line(feats, feat_current)

    data = np.transpose(np.vstack((feats_info, feats)))
    df_out = pd.DataFrame(data, columns=col_name)
    num_of_feat = data.shape[1]
    return df_out, num_of_feat, col_name
    # return np.transpose(feats), col_name


def feat_extr_array(data, fs, WdW):
    """produce features from data

    data is a nd array of ts
    fs is sampling rate
    WdW is the windows for features extraction in number of points
    """
    feats = []
    for col in range(data.shape[1]):
        print(col)
        feat_1D, num_of_feat, feat_name = feat_extr_1D(data[:, col], fs, WdW)
        feats = add_line(feats, feat_1D.values)
    return feats, num_of_feat, feat_name


def feat_viz_sub(l, r, data, ylabel, title, axes, optional_time=[]):
    """perform subplot display with synchronized x axis"""
    if optional_time == []:
        if len(axes.shape) == 1:
            axes[l].set_title(title)
            axes[l].plot(data, color='C0')
            axes[l].set_ylabel(ylabel)   
            axes[l].grid()
        else :
            axes[l, r].set_title(title)
            axes[l, r].plot(data, color='C0')
            axes[l, r].set_ylabel(ylabel)
            axes[l, r].grid()
            if l == np.max(axes.shape) - 1:
                axes[l, r].set_xlabel('time[msec]')#the lowest as the label on x

    else :
        if len(axes.shape) == 1:
            axes[l].set_title(title)
            axes[l].plot(optional_time, data, color='C0')
            axes[l].set_ylabel(ylabel)
            axes[l].grid()        
            if l == np.max(axes.shape)- 1:#the lowest as the label on x
                axes[l].set_xlabel('time[msec]')
        else :
            axes[l, r].set_title(title)
            axes[l, r].plot(optional_time, data, color='C0')
            axes[l, r].set_ylabel(ylabel)
            axes[l, r].grid()
            if l == np.max(axes.shape) - 1:
                axes[l, r].set_xlabel('time[msec]')#the lowest as the label on x


def feat_viz(data, feat_mat, axes, first_label, feat_time, feat_names):
    """Plots TS.

    Time is the time,
    Data is a one dim array,
    Filt is [Flow, FHigh],
    first_label is name of the initial ts,
    feat_time : is the time array for the features display
    subset 
    """

    feat_viz_sub(0, 0, data, "Amplitude", first_label, axes)
    feat_viz_sub(0, 1, data, "Amplitude", first_label, axes)
    ln = 1

    for col in range(0, 5):
        feat_viz_sub(ln, 0, feat_mat[:, col], "Amplitude", 
                     feat_names[col], axes, feat_time)
        ln = ln + 1
    ln = 1
    for col in range(5, 10):
        feat_viz_sub(ln, 1, feat_mat[:, col], "Amplitude", 
                     feat_names[col], axes, feat_time)
        ln = ln + 1



def feat_import(filename):
    """import a Feature instance"""
    with open(filename, 'rb') as input:
        instance_name = pickle.load(input)
    return instance_name

       ################
       #### class #####
       ################
class Features:
    def __init__(self, file_name, data_type):
        self.df = pd.read_csv(file_name, delimiter=';', 
                              engine='python')
        self.val = pd.read_csv(file_name, delimiter=';', 
                               engine='python').values
        self.type = data_type
        self.Wdw = []
        self.sub_samp = []
        self.fs = []
        self.filt_val = pd.read_csv(file_name, delimiter=';', 
                                    engine='python').values
        self.feat_names = []
        
    def feat_compute(self, WdW, fs, sub_samp = 1):
        """compute the features
        
            WdW is the analysis window. Carefull : this unit is in point after subsampling ie: if one wants a windows of 1sec for fs= 1000Hz
                and sub_samp = 10 then WdW should be set to 100 (and not 1000)
            fs is sampling freq
            sub_samp : is for subsampling it peaks one point every sub_samp point (no extrapolation)
        """
        self.Wdw = WdW
        self.sub_samp = sub_samp
        self.fs = fs
        # filtering
        global_filt(self)
        # compute features
        self.features_mat, self.number_of_features,self.feat_names = feat_extr_array(self.filt_val[::sub_samp, :], 
                                          self.fs / self.sub_samp, self.Wdw)
        
    def display_ts(self,ts2call = []):
        """to display a subset of time series"""
        pyplot.close()
        if ts2call == []:#plots all figures
            ts2call = list(range(1,self.filt_val.shape[1]))
        nrows = np.min([len(ts2call),5]) #number of row and cols in subplot
        ncols = (len(ts2call)-1) // 5  + 1
        fig, axes = pyplot.subplots(nrows, ncols, figsize=(7, 7), sharex=True)
        for ts in ts2call:
            i = 0
            for ts in ts2call:
                feat_viz_sub(i%(nrows), i//(nrows),self.filt_val[:, ts],
                             "Amplitude", self.df.columns[ts], axes)
                i = i+1
                
    def display_ft(self,ft2call):
        """display a subset of fetaures
        
        ft2call is a list of list : ((ts1,ft1),(ts2,ft2),...)
        """
        pyplot.close()
        nrows = np.min([len(ft2call),9]) #number of row and cols in subplot
        ncols = (len(ft2call)-1) // 9 + 1
        fig, axes = pyplot.subplots(nrows, ncols, figsize=(7, 7), sharex=True)
        i = 0
        for ft in ft2call:
            feat_viz_sub(i%(nrows) , i//(nrows), self.features_mat[:, ft[1] +  ft[0] * self.number_of_features],
                         "Amplitude", self.feat_names[ft[1]] + "; " + self.df.columns[ft[0]], 
                         axes, self.features_mat[:, 1]*self.sub_samp)
            i = i+1
        
    def display(self, ts2call = [], feat2call = []):
        """display timesies along with features

        subset_ts : is optional, it's a list of integer corresponding to the time series to be displayed
        subset_ts:t|ecg|pzt|eda|bpm|evt
        subset_feat: 'index', 'WdW Position', 'Ej', 'Pow', 'AutoCorr', 'ApproxEnt', 'Entrop', 'Complexity', 'countAboveMn',
                'countBelowMn', 'fft_agg', 'interbeat']
        """
        """# cleaning data for display
        self.features_mat[np.isnan(self.features_mat)] = -1
        self.features_mat[np.isinf(self.features_mat)] = 10
        # removing outliers (to facilitate ploting)

        for col in range(2, self.features_mat.shape[1]):  # remove outliers
            feat_col = self.features_mat[:, col]
            col_mean = np.mean(feat_col)
            col_var = np.var(feat_col)
            feat_col[(feat_col - col_mean) ** 2 > 4 * col_var] = 10  # set the outlier to 10 to help displaying
            #print("change in mean:", col_mean - np.mean(feat_col))
            #print("change in var:", col_var - np.var(feat_col))"""

        ########
        # plot #
        ########
        pyplot.close()
        if ts2call == []:#plots all figures
            ts2call = list(range(0,self.filt_val.shape[1]))

        if feat2call == []:#plots all figures
            feat2call = list(range(2,self.number_of_features))

        nrows = np.min([len(feat2call)+1,6]) # number of row and cols in subplot
        ncols = (len(feat2call)-1) // 6 +1

        for ts in ts2call:
            fig, axes = pyplot.subplots(nrows, ncols, figsize=(7, 7), sharex=True)
            for col in range(ncols):
                feat_viz_sub(0, col, self.filt_val[:,ts], "Amplitude", self.df.columns[ts], axes)
            i = 0
            for ft in feat2call:
                print('ft',ft)
                print('i',i)
                print('%',i%(nrows-1))
                print('//', i//(nrows-1))
                print('ft + 2 + ts * self.number_of_features',ft +  ts * self.number_of_features)
                print('ts',ts)
                feat_viz_sub(i%(nrows-1) + 1, i//(nrows-1), self.features_mat[:, ft +  ts * self.number_of_features],
                             "Amplitude", self.feat_names[ft], axes, self.features_mat[:, 1]*self.sub_samp)
                i = i+1
        return 
    
    
    def feat_exract(self,ft2extr):
        """extract a selected subset of features 
        
        ft2extr is a  2D list with ((timeserie #1, feature#1),(ts#2,ft#2)...)
        features_mat is structured as |all features from timeserie #1 = self.number_of_features columns | all features from timeserie #2 = self.number_of_features columns| ...
        """
        feat_extr =  self.features_mat[:, ft2extr[0][1] +  ft2extr[0][0] * self.number_of_features]
        for ft_e in ft2extr[1:]:
            feat_extr = np.vstack((feat_extr, self.features_mat[:, ft_e[1] +  ft_e[0] * self.number_of_features]))
        return feat_extr.T
    
    
    def identify_kmeans_states(ref_states,test_states):
        """corr table [n] is the test_state corresponding to ref_state n
        
        the assignation is by distance minimisation
        """
        corr_table = []
        temp_test_states = test_states.copy()
        ln = 0
        for rs in ref_states:
            dist  =[(x[0]-rs[0])**2+(x[1]-rs[0])**2 for x in temp_test_states]
            corr_table = np.append(corr_table, [dist.index(np.min(dist))])
            temp_test_states[dist.index(np.min(dist))] = [np.inf, np.inf] #so that we can't get two test_states closest to one ref state
            ln += 1
        return corr_table
    

        
            
    def feat_pca(self, input_feat, ref_centers = [], ref_pca = []):
        input_feat[np.isnan(input_feat)] = 0
        input_feat[np.isinf(input_feat)] = 1
        X = StandardScaler().fit_transform(input_feat)  
        if ref_pca == []:
            pca = PCA(n_components=2)
            pca.fit(X)
        else:
            pca = ref_pca
        feat_reduced_pca = pca.transform(X) #projection sur les axes PCa=> reduction dim
        feat_reduced = pca.inverse_transform(feat_reduced_pca) #on se remet dans les coordonnées initales
        #pyplot.scatter(X[:, 0], X[:, 1], alpha=0.2)
        #pyplot.scatter(feat_reduced[:, 0], feat_reduced[:, 1], alpha=0.8)
        #pyplot.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.8)
        #pyplot.plot(np.transpose(pca.components_))
        pyplot.show()
        print(pca.components_)
        print(pca.singular_values_)
        print(pca.explained_variance_ratio_)
        
        ########KMEAN
        X = feat_reduced_pca
        kmeans = KMeans(n_clusters = 4)
        kmeans.fit(X)
        y_kmeans = kmeans.predict(X)
        pyplot.figure()
        pyplot.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

        centers = kmeans.cluster_centers_
        pyplot.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);
        pyplot.figure()
        pyplot.plot(X[:,0])
        #pyplot.plot(spy.signal.savgol_filter(y_kmeans,21,1))
        pyplot.plot(y_kmeans)
        if ref_centers != []:
            return self.identify_kmeans_states(centers,centers)
        
    def save(self, file_name):
        with open(file_name, 'wb') as output:
             pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        return 


#    feat.display_ft(data2show_comp)

