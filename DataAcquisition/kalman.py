# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 10:30:53 2019

@author: Simon
"""
import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.kalman import ExtendedKalmanFilter as EKF

from math import ceil
from datetime import timedelta
import datetime
import matplotlib as mp
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pyquaternion import Quaternion
from scipy.fftpack import fft, fftfreq, fftshift
from skimage import util
import math
data=pd.read_csv('vol1_2909.csv',';')
calibdebut=0
calibfin=5000
imin=150000
imax=200000
N=imax-imin


XSENSE_ACC=data.loc[:,["FD_ACCX2","FD_ACCY2","FD_ACCZ2"]]/9.81
ACC0=XSENSE_ACC.iloc[calibdebut:calibfin].mean().to_numpy()
XSENSE_ACC=XSENSE_ACC.iloc[imin:imax].reset_index().drop("index",1)
ACC0=np.array([0,0,1])
XSENSE_GYRO_=data.loc[:,["FD_GYRO_X2","FD_GYRO_Y2","FD_GYRO_Z2"]]*math.pi/180
GYR0=XSENSE_GYRO_.iloc[calibdebut:calibfin].mean().to_numpy()
XSENSE_GYRO_=XSENSE_GYRO_.iloc[imin:imax].reset_index().drop("index",1)

XSENSE_MAGNETOMETER_=data.loc[:,["FD_MAGNETOMETER_X2","FD_MAGNETOMETER_Y2","FD_MAGNETOMETER_Z2"]]
MAG0=XSENSE_MAGNETOMETER_.iloc[calibdebut:calibfin].mean().to_numpy()
XSENSE_MAGNETOMETER_=XSENSE_MAGNETOMETER_.iloc[imin:imax].reset_index().drop("index",1)

XSENSE_QUAT=data.loc[:,["FD_ORIENTATION_QUATERNION2_0","FD_ORIENTATION_QUATERNION2_1","FD_ORIENTATION_QUATERNION2_2","FD_ORIENTATION_QUATERNION2_3"]]
XSENSE_QUAT=XSENSE_QUAT.iloc[imin:imax].reset_index().drop("index",1)




def q2euler(q):
    q0=q[0]
    q1=q[1]
    q2=q[2]
    q3=q[3]
    phi = np.arctan2(2*(q0*q2+q1*q3), 1-2*(q0*q0+q1*q1))
    theta = np.arcsin(2*(q3*q1 - q0*q2))
    theta=max(min(theta,1),-1)
    psi =np.arctan2(2*(q2*q3 + q1*q0), 1-2*(q2*q2 + q3*q3))
    return np.array([phi, theta, psi])


def q2euler_pd(pandas,a):
    q0=pandas.iloc[:,0]
    q1=pandas.iloc[:,1]
    q2=pandas.iloc[:,2]
    q3=pandas.iloc[:,3]
    pandas["phi"+a] = np.arctan2(2*(q0*q1+q2*q3), 1-2*(q1*q1+q2*q2))
    pandas["theta"+a]= np.arcsin(2*(q3*q1 - q0*q2))
    pandas["psi"+a] = np.unwrap(np.arctan2(2*(q0*q3 + q1*q2), 1-2*(q2*q2 + q3*q3)))
    return pandas
    
def q2euler_pdbis(pandas,a):
    q0=pandas.iloc[:,0]
    q1=pandas.iloc[:,1]
    q2=pandas.iloc[:,2]
    q3=pandas.iloc[:,3]
    pandas["phi"+a] = np.unwrap(np.arctan(2*(q0*q1+q2*q3), 2*(q1*q1+q2*q2)-1))
    pandas["theta"+a]= np.unwrap(np.arcsin(2*(q3*q1 - q0*q2)))
    pandas["psi"+a] = np.arctan2(2*(q1*q2 + q0*q3), 2*(q0*q0 + q1*q1)-1)
    return pandas



class EKF_cust(EKF):
    def __init__(self, dt):
        EKF.__init__(self,4,6,6)
        self.dt = dt
        
    def predict(self,u):
        
        [p,q,r]=u
        DQ=np.array([[0,-p,-q,-r],[p,0,r,-q],[q,-r,0,p],[r,q,-p,0]]);
        A=np.eye(4)+0.5*dt*DQ
        self.x=A.dot(self.x)
        self.P=np.eye(4).dot(self.P).dot(np.eye(4))+self.Q




def sensor_reading(i):
    accx=XSENSE_ACC["FD_ACCX2"][i]
    accy=XSENSE_ACC["FD_ACCY2"][i]
    accz=XSENSE_ACC["FD_ACCZ2"][i]
    magx=XSENSE_MAGNETOMETER_["FD_MAGNETOMETER_X2"][i]
    magy=XSENSE_MAGNETOMETER_["FD_MAGNETOMETER_Y2"][i]
    magz=XSENSE_MAGNETOMETER_["FD_MAGNETOMETER_Z2"][i]
    return np.array([accx,accy,accz,magx,magy,magz])


def gyro_measure(i):
    x=XSENSE_GYRO_["FD_GYRO_X2"][i]
    y=XSENSE_GYRO_["FD_GYRO_Y2"][i]
    z=XSENSE_GYRO_["FD_GYRO_Z2"][i]
    
    return np.array([x,y,z])


def q2R(q):
    q0=q[0]
    q1=q[1]
    q2=q[2]
    q3=q[3]
    return np.array([[q0**2+q1**2-q2**2-q3**2,   2*(q1*q2-q0*q3),        2*(q0*q2+q1*q3)],
                  [2*(q1*q2+q0*q3),        q0**2-q1**2+q2**2-q3**2,    2*(q2*q3-q0*q1)],
                  [2*(q1*q3-q0*q2),        2*(q0*q1+q2*q3),        q0**2-q1**2-q2**2+q3**2]])
    
    
def quat2M(q):
    q0=q[0];
    q1=q[1];
    q2=q[2];
    q3=q[3];
    M = np.array([[q0**2+q1**2-q2**2-q3**2,2*(q1*q2-q0*q3),2*(q0*q2+q1*q3)],[2*(q1*q2+q0*q3),q0**2-q1**2+q2**2-q3**2,2*(q2*q3-q0*q1)],[2*(q1*q3-q0*q2),2*(q0*q1+q2*q3),q0**2-q1**2-q2**2+q3**2]])
    return M

#Measurment Matrix
def Hx(x):
    [q0,q1,q2,q3]=x
    M=np.transpose(quat2M(x))
    Y =np.concatenate((M.dot(ACC0),M.dot(MAG0)))
    return Y

#Jacobian Matrix of the measurment
def Hjacobian(x):
    [q0,q1,q2,q3]=x
    J1=2*np.array([[q0,q1,-q2,-q3],[-q3,q2,q1,-q0],[q2,q3,q0,q1]])
    J2=2*np.array([[q3,q2,q1,q0],[q0,-q1,q2,-q3],[-q1,-q0,q3,q2]])
    J3=np.array([[-q2,q3,-q0,q1],[q1,q0,q3,q2],[q0,-q1,-q2,q3]])
    Hacc=(J1*ACC0[0]+J2*ACC0[1]+J3*ACC0[2])
    Hmag=(J1*MAG0[0]+J2*MAG0[1]+J3*MAG0[2])
    
    H=np.concatenate((Hacc,Hmag))
    return H



dt=0.1
###INIT
kf = EKF_cust(dt=dt)
kf.x=np.array([1.,0.,0.,0.])
kf.P=100.*np.eye(4)
qa=1
kf.Q=np.diag([qa,qa,qa,qa])
kf.F=np.eye(4)
ra=10.
rm=10**5.
kf.R=np.diag([ra,ra,ra,rm,rm,rm])

index=N
track=[]
##KALMAN LOOP
for i in range(index) :
    gyro=gyro_measure(i)
    [p,q,r]=gyro
    kf.predict(u=gyro)
    z=sensor_reading(i)
    kf.update(z,HJacobian=Hjacobian,Hx=Hx)
    kf.x=kf.x/np.linalg.norm(kf.x)
    track.append(kf.x)
  
    
##PLOT
XSENSE_QUAT=q2euler_pd(XSENSE_QUAT,"2")
result=pd.DataFrame(track)
result=q2euler_pd(result,"1")


fig_3 = plt.figure()
(XSENSE_QUAT["theta2"][0:index]).plot(label="XSENSE")
result["theta1"][0:index].plot(label="BNO")
plt.legend()


(result["psi1"][0:index]*math.pi/180).plot()
XSENSE_QUAT["psi2"][0:index].plot(legend=True)

fig_3 = plt.figure()
result["phi1"][0:index].plot()
(XSENSE_QUAT["phi2"][0:index]).plot()



fig_3 = plt.figure()
result.iloc[0:index,0].plot()
XSENSE_QUAT.iloc[0:index,0].plot()

fig_3 = plt.figure()
result.iloc[0:index,1].plot()
XSENSE_QUAT.iloc[0:index,1].plot()

fig_3 = plt.figure()
result.iloc[0:10000,2].plot()
XSENSE_QUAT.iloc[0:10000,2].plot()

fig_3 = plt.figure()
result.iloc[0:index,3].plot()
XSENSE_QUAT.iloc[0:index,3].plot()
