# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:33:41 2019

@author: PIE
"""

import pandas as pd
import numpy as np
#Kalman

# estimation attitude
qa = 1*0.01*0.01  #Bruit d'état
ra = 10 #Buit de mesure accéléro
rm = 1 #bruit de mesure magnéto
Q = np.diag([qa,qa,qa,qa])
R = np.diag([ra,ra,ra,rm,rm,rm])
X=[1,0,0,0]' %Etat : quaternion
P = 1000*np.eye(4)

tp=0
ii=0
obs = np.array([])
xtrue = np.array([])
xhat = np.array([])

while(1):
    ii=ii+1
    

    #d(1)    = Time                (s)
    # d(2:4)  = Gyroscope     X,Y,Z (°/s)
    # d(5:7)  = Accelerometer X,Y,Z (g)
    # d(8:10) = Magnetometer  X,Y,Z (Gauss)
    t=d[1]  
    
    
    # Predict
    p=np.deg2rad(d[2])
    q=np.deg2rad(d[3])
    r=np.deg2rad(d[4])
    DQ=np.matrix([[0,-p,-q,-r],[p,0,r,-q],[q,-r,0,p],[r,q,-p,0]])
    A=np.eye(4)+0.5*DQ*dt
    X = A*X
    P = np.eye(4)*P*np.eye(4)+Q
    
    
    # Update
    
    Y =np.array([d[5],    #accX
            d[6],    #accY
            d[7],    #accZ
            d[8],    #magX
            d[9],    #MagY
            d[10]   #magZ
            ])
        M=quat2M(X(1:4))'
        Yhat = [M*ACC0
            M*MAG0]
        q0=X[1]
        q1=X[2]
        q2=X[3]
        q3=X[4]
        J1=2*np.matrix([[q0,q1,-q2,-q3],
            [-q3,q2,q1,-q0],
            [q2,q3,q0,q1]])
        J2=2*np.matrix([[q3,q2,q1,q0],
            [q0,-q1,q2,-q3],
            [-q1,-q0,q3,q2]
        J3=np.matrix([[-q2,q3,-q0,q1],
            [q1,q0,q3,q2],
            [q0,-q1,-q2,q3]]
        Hacc=J1*ACC0(1)+J2*ACC0(2)+J3*ACC0(3)
        Hmag=J1*MAG0(1)+J2*MAG0(2)+J3*MAG0(3)
     
        H=np.concatenate((Hacc,Hmag))
        G = H*P*H.T+R
        K = P*H.T*np.linalg.inv(G)
        X = X+K*(Y-Yhat)
        X = X/np.linalg.norm(X(1:4))
        P = P - P*K*H
        xhat =np.concatenate((xhat,X),axis=1)
    end
    
    # Update 3D visualization:
    %DCM_k = quat2dcm(X(1:4)')
    DCM_k = quat2dcm([X(1)-X(2:4)]'/norm(X(1:4)))
    update3D
end

