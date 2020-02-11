# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 11:42:47 2020

@author: Simon
"""
import matplotlib.pyplot as plt


aoi=[["L","r","Left"],["F","g","Front"],["R","y","Right"],["P","b","Primary"],["S","c","Secondary"]]
L ='r'
F='g'
R='y'
P='b'
S='c'


def time_temps_aoi(clean_aois):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel("Temps de vol ( ms) ")
    ax1.set_ylabel("Temps passé sur chaque AOI sans transition( ms) ")
    
    for a in aoi:
        aoigraph=clean_aois[clean_aois["AOI"]==a[0]]
        aoigraph=aoigraph[["timestamp","delta"]]
        ax1.scatter(aoigraph["timestamp"],aoigraph["delta"],c=a[1],label=a[2])
    plt.legend(loc='upper left');
    plt.show()
    
    

def hist_time_aoi(stats_aoi,aoi):
    fig=plt.figure()
    ax1=fig.add_subplot(111)
    ax1.set_xlabel("Vol Guilhem")
    ax1.set_ylabel("Répartition du temps sur les AOI (%)")
    leg=[]
    a=aoi[0]
    prec=stats_aoi.loc[a[0],"%_time"]
    plt.bar([1],prec,color=a[1],label=a[2])
    leg.append(a[2])
    for a in aoi[1:] :
        ax1.bar([1],stats_aoi.loc[a[0],"%_time"],color=a[1],label=a[2],bottom=prec)
        prec+=stats_aoi.loc[a[0],"%_time"]
        leg.append(a[2])
    plt.legend(loc='upper left');
    plt.show()

def hist_count_aoi(stats_aoi):

    fig=plt.figure()
    ax1=fig.add_subplot(111)
    ax1.set_xlabel("Vol Guilhem")
    ax1.set_ylabel("Répartition passage sur les AOI (#)")
    leg=[]
    a=aoi[0]
    prec=stats_aoi.loc[a[0],"count"]
    plt.bar([1],prec,color=a[1],label=a[2])
    leg.append(a[2])
    for a in aoi[1:] :
        ax1.bar([1],stats_aoi.loc[a[0],"count"],color=a[1],label=a[2],bottom=prec)
        prec+=stats_aoi.loc[a[0],"count"]
        leg.append(a[2])
    plt.legend(loc='upper left');
    plt.show()
    
    
    
def hist_transitions(chain):
    f=0
    h=0
    o=0
    
    for a in chain.index:
        if "L" in a or "R" in a:
            chain.loc[a,"type"]="Horizontale"
            chain.loc[a,"type2"]=1
            h+=1
        elif "FP" in a or "PF" in a:
            chain.loc[a,"type"]="Verticale"
            chain.loc[a,"type2"]=0
            f+=1
        else :
            chain.loc[a,"type"]="Other"
            chain.loc[a,"type2"]=2
            o+=1
    prec=[0,0,0]
    chain["type2"]=chain["type2"].astype(int)
    fig=plt.figure()
    ax1=fig.add_subplot(111)
    patch_handles = []
    
    ax1.set_xlabel("Vol Guilhem")
    ax1.set_ylabel("Répartition transitions sur les AOI (#)")
    for a in chain.index:
        patch_handles.append(ax1.bar(chain.loc[a,"type"],chain.loc[a,"pourcent"],label=chain.loc[a,"type"],bottom=prec[chain.loc[a,"type2"]]))
        prec[chain.loc[a,"type2"]]+=chain.loc[a,"pourcent"]
    for j in range(len(patch_handles)):
            for i, patch in enumerate(patch_handles[j].get_children()):
                bl = patch.get_xy()
                x = 0.5*patch.get_width() + bl[0]
                y = 0.5*patch.get_height() + bl[1]
                ax1.text(x,y, chain.index[j], ha='center')
    
    
    plt.show()    