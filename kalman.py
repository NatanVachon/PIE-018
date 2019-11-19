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
data=pd.read_csv('vol2_2909.csv',';')

imin=000
imax=248000
N=imax-imin
XSENSE_ACC=data.loc[:,["FD_ACCX2","FD_ACCY2","FD_ACCZ2"]]
XSENSE_GYRO_=data.loc[:,["FD_GYRO_X2","FD_GYRO_Y2","FD_GYRO_Z2"]]
XSENSE_MAGNETOMETER_=data.loc[:,["FD_MAGNETOMETER_X2","FD_MAGNETOMETER_Y2","FD_MAGNETOMETER_Z2"]]

MAG0=XSENSE_MAGNETOMETER_.mean().to_numpy()
ACC0=XSENSE_ACC.mean().to_numpy()
GYR0=XSENSE_GYRO_.mean().to_numpy()


class EKF_cust(EKF):
    def __init__(self, dt):
        EKF.__init__(self,4,6,6)
        self.dt = dt
        
    def predict(self, u=gyro):
        
        [p,q,r]=gyro
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
    x=XSENSE_GYRO_["FD_GYRO_X2"][i]*math.pi/180
    y=XSENSE_GYRO_["FD_GYRO_Y2"][i]*math.pi/180
    z=XSENSE_GYRO_["FD_GYRO_Z2"][i]*math.pi/180
    
    return np.array([x,y,z])

def quat2M(q):
    q0=q[0];
    q1=q[1];
    q2=q[2];
    q3=q[3];
    M = np.array([[q0**2+q1**2-q2**2-q3**2,2*(q1*q2-q0*q3),2*(q0*q2+q1*q3)],[2*(q1*q2+q0*q3),q0**2-q1**2+q2**2-q3**2,2*(q2*q3-q0*q1)],[2*(q1*q3-q0*q2),2*(q0*q1+q2*q3),q0**2-q1**2-q2**2+q3**2]])
    return M

#Measurment Matric
def Hx(x):
    [qo,q1,q2,q3]=x
    M=np.transpose(quat2M(kf.x))
    Yhat =np.concatenate((M.dot(ACC0),M.dot(MAG0)))
    return Yhat

#Jacobian Matrix
def Hjacobian(x):
    [qo,q1,q2,q3]=x
    J1=2*np.array([[q0,q1,-q2,-q3],[-q3,q2,q1,-q0],[q2,q3,q0,q1]])
    J2=2*np.array([[q3,q2,q1,q0],[q0,-q1,q2,-q3],[-q1,-q0,q3,q2]])
    J3=np.array([[-q2,q3,-q0,q1],[q1,q0,q3,q2],[q0,q1,q2,q3]])
    Hacc=(J1*ACC0[0]+J2*ACC0[1]+J3*ACC0[2])
    Hmag=(J1*MAG0[0]+J2*MAG0[1]+J3*MAG0[2])
    H=np.concatenate((Hacc,Hmag))
    return H




###INIT
kf = EKF_cust(dt=dt)
kf.x=np.array([1.,0.,0.,0.])
kf.P=1000.*np.eye(4)
qa=0.01*0.01
kf.Q=np.diag([qa,qa,qa,qa])
kf.F=np.eye(4)
ra=10.
rm=1.
kf.R=np.diag([ra,ra,ra,rm,rm,rm])
dt=0.1

track=[]
##KALMAN LOOP
for i in range(20):
    gyro=gyro_measure(i)
    [p,q,r]=gyro
    kf.predict(u=gyro)
    z=sensor_reading(i)
    kf.update(z,HJacobian=Hjacobian,Hx=Hx)
    kf.x=kf.x/np.linalg.norm(kf.x)
    track.append(kf.x)
    

