
import sys
import os
from tkinter import font

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D

import time

if __name__ == '__main__':

    from fis.sifuzz import sifuzzy
    from fis.sifuzz import membership

else:
    from .fis.sifuzz import sifuzzy
    from .fis.sifuzz import membership

mb = membership()
 


class ObstacleAvoid:
    def __init__(self, d_min, d_max):

        # Instance FIS Obstacle Avoid to each direction
        self.FIS_OALeft  = sifuzzy(2,1)   
        self.FIS_OARight = sifuzzy(2,1)   
        self.FIS_OAFront = sifuzzy(2,1)   
        self.FIS_OABack  = sifuzzy(2,1)  

        # Domain Input
        xi_d = np.linspace(d_min,d_max, round(((d_max - d_min)/0.01) + 1))
        xi_a = np.linspace(-180,180, round(((360)/1) + 1))
        # Domain Output (Consequente)
        xo = np.linspace(-180,180, round(((360)/1) + 1))

        # Set Domain Input
        self.FIS_OALeft.finput.setdm(0, xi_d)
        self.FIS_OARight.finput.setdm(0, xi_d)
        self.FIS_OAFront.finput.setdm(0, xi_d)
        self.FIS_OABack.finput.setdm(0, xi_d)

        self.FIS_OALeft.finput.setdm(1, xi_a)
        self.FIS_OARight.finput.setdm(1, xi_a)
        self.FIS_OAFront.finput.setdm(1, xi_a)
        self.FIS_OABack.finput.setdm(1, xi_a)


        # Set Domain Output
        self.FIS_OALeft.foutput.setdm(0, xo)
        self.FIS_OARight.foutput.setdm(0, xo)
        self.FIS_OAFront.foutput.setdm(0, xo)
        self.FIS_OABack.foutput.setdm(0, xo)

        # CREAT MEMBERSHIP INPUT
        k = (d_max - d_min)/6

        m0 = mb.gaussmf(xi_d, [k, d_min])
        m1 = mb.gaussmf(xi_d, [k, d_min + (d_max - d_min)/2])
        m2 = mb.gaussmf(xi_d, [k, d_max])

        # FIS_AORight
        self.FIS_OARight.finput.addmb(0, m0)
        self.FIS_OARight.finput.addmb(0, m1)
        self.FIS_OARight.finput.addmb(0, m2)


        # FIS_AOLeft
        self.FIS_OALeft.finput.addmb(0, m0)
        self.FIS_OALeft.finput.addmb(0, m1)
        self.FIS_OALeft.finput.addmb(0, m2)


        # FIS_AOBack
        self.FIS_OABack.finput.addmb(0, m0)
        self.FIS_OABack.finput.addmb(0, m1)
        self.FIS_OABack.finput.addmb(0, m2)


        # FIS_AOFront
        self.FIS_OAFront.finput.addmb(0, m0)
        self.FIS_OAFront.finput.addmb(0, m1)
        self.FIS_OAFront.finput.addmb(0, m2)

        # CREAT MEMBERSHIP YAW DIRECTION
        k_sb = xo[0]/2
        yS = mb.trimf(xo,[xo[0], xo[0], xo[0] - k_sb]) +  mb.trimf(xo,[xo[0] - 3*k_sb, xo[0] - 4*k_sb, xo[0] - 4*k_sb])
        yL = mb.trimf(xo,[xo[0], xo[0] - k_sb, xo[0] - 2*k_sb])
        yN = mb.trimf(xo,[xo[0] - k_sb, xo[0] - 2*k_sb, xo[0] - 3*k_sb])
        yO = mb.trimf(xo,[xo[0] - 2*k_sb, xo[0] - 3*k_sb, xo[0] - 4*k_sb])

        # 
        self.FIS_OAFront.finput.addmb(1, yS)
        self.FIS_OAFront.finput.addmb(1, yL)
        self.FIS_OAFront.finput.addmb(1, yN)
        self.FIS_OAFront.finput.addmb(1, yO)

        self.FIS_OABack.finput.addmb(1, yS)
        self.FIS_OABack.finput.addmb(1, yL)
        self.FIS_OABack.finput.addmb(1, yN)
        self.FIS_OABack.finput.addmb(1, yO)

        self.FIS_OALeft.finput.addmb(1, yS)
        self.FIS_OALeft.finput.addmb(1, yL)
        self.FIS_OALeft.finput.addmb(1, yN)
        self.FIS_OALeft.finput.addmb(1, yO)

        self.FIS_OARight.finput.addmb(1, yS)
        self.FIS_OARight.finput.addmb(1, yL)
        self.FIS_OARight.finput.addmb(1, yN)
        self.FIS_OARight.finput.addmb(1, yO)



        

        self.FIS_OAFront.foutput.addmb(0, yS)
        self.FIS_OAFront.foutput.addmb(0, yL)
        self.FIS_OAFront.foutput.addmb(0, yN)
        self.FIS_OAFront.foutput.addmb(0, yO)

        self.FIS_OABack.foutput.addmb(0, yS)
        self.FIS_OABack.foutput.addmb(0, yL)
        self.FIS_OABack.foutput.addmb(0, yN)
        self.FIS_OABack.foutput.addmb(0, yO)

        self.FIS_OALeft.foutput.addmb(0, yS)
        self.FIS_OALeft.foutput.addmb(0, yL)
        self.FIS_OALeft.foutput.addmb(0, yN)
        self.FIS_OALeft.foutput.addmb(0, yO)

        self.FIS_OARight.foutput.addmb(0, yS)
        self.FIS_OARight.foutput.addmb(0, yL)
        self.FIS_OARight.foutput.addmb(0, yN)
        self.FIS_OARight.foutput.addmb(0, yO)


        # self.FIS_OALeft.foutput.plot()
        # self.FIS_OAFront.finput.addmb(0, m1)
        # self.FIS_OAFront.finput.addmb(0, m2)
        # self.FIS_OARight.foutput.automf(0, 5)
        # self.FIS_OALeft.foutput.automf(0, 5)
        # self.FIS_OAFront.foutput.automf(0, 5)
        # self.FIS_OABack.foutput.automf(0, 5)

        # RULE


        
        # for i in range(3):
        #     plt.plot(self.FIS_OABack.finput.v[0].x,self.FIS_OABack.finput.v[0].f[i])
        # plt.show()
        # self.FIS_OAFront.finput.plot()
        # print(self.FIS_OABack.finput.v[0].x)

        path_d = "/home/marc/ros-ws/theconstructcore-ws/quadrotor-ws/src/hector_control/src/system"
        datarule_b = pd.read_csv(path_d + str("/datarule/datarule_rback.csv"), delimiter=',')
        datarule_f = pd.read_csv(path_d +  str("/datarule/datarule_rfront.csv"))
        datarule_r = pd.read_csv(path_d + str("/datarule/datarule_rright.csv"))
        datarule_l = pd.read_csv(path_d + str("/datarule/datarule_rleft.csv"))

        # datarule_b["D_BACK"].iloc
        # print(datarule_b.values)
        # REPLACE BACK
        datarule_b = datarule_b.replace("S",0)
        datarule_b = datarule_b.replace("L",1)
        datarule_b = datarule_b.replace("N",2)
        datarule_b = datarule_b.replace("O",3)

        datarule_b = datarule_b.replace("P",0)
        datarule_b = datarule_b.replace("M",1)
        datarule_b = datarule_b.replace("G",2)

        # REPLACE FRONT
        datarule_f = datarule_f.replace("S",0)
        datarule_f = datarule_f.replace("L",1)
        datarule_f = datarule_f.replace("N",2)
        datarule_f = datarule_f.replace("O",3)

        datarule_f = datarule_f.replace("P",0)
        datarule_f = datarule_f.replace("M",1)
        datarule_f = datarule_f.replace("G",2)

        # REPLACE RIGHT
        datarule_r = datarule_r.replace("S",0)
        datarule_r = datarule_r.replace("L",1)
        datarule_r = datarule_r.replace("N",2)
        datarule_r = datarule_r.replace("O",3)

        datarule_r = datarule_r.replace("P",0)
        datarule_r = datarule_r.replace("M",1)
        datarule_r = datarule_r.replace("G",2)

        # REPLACE LEFT
        datarule_l = datarule_l.replace("S",0)
        datarule_l = datarule_l.replace("L",1)
        datarule_l = datarule_l.replace("N",2)
        datarule_l = datarule_l.replace("O",3)

        datarule_l = datarule_l.replace("P",0)
        datarule_l = datarule_l.replace("M",1)
        datarule_l = datarule_l.replace("G",2)

        # PANDAS DATAFRAME TO ARRAY
        rule_b = list(datarule_b.values)
        rule_l = list(datarule_l.values)
        rule_r = list(datarule_r.values)
        rule_f = list(datarule_f.values)

        # SET RULE
        self.FIS_OARight.rule.set(rule_r)
        self.FIS_OALeft.rule.set(rule_l)
        self.FIS_OAFront.rule.set(rule_f)
        self.FIS_OABack.rule.set(rule_b)
        pass
        
    def plot(self):
        pass 
    def avoid_left(self, d, theta):
        return self.FIS_OALeft.mamfis([d, theta], 1)
        
    def avoid_right(self, d, theta):
        return self.FIS_OARight.mamfis([d, theta], 1)
        
    def avoid_back(self, d, theta):
        return self.FIS_OABack.mamfis([d, theta], 1)
        
    def avoid_front(self, d, theta):
        return self.FIS_OAFront.mamfis([d, theta], 1)


# PLOT 

def plotmesh(x , y):

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    X,Y = np.meshgrid(x,y)


    z = np.array([SOA.avoid_front(x, y) for (x,y) in zip(np.ravel(X), np.ravel(Y))])
    Z = z.reshape(X.shape)

    ax.plot_surface(Y, X, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    plt.show()


if __name__ == '__main__':
    
    pass
    # ax = plt.axes(projection='3d')
    SOA = ObstacleAvoid(0.4,2)
    SOA.FIS_OAFront.finput.plot()
    # print(SOA.avoid_front(1, -20))
    r = [[],[],[]]
    # x = np.round(np.linspace(0.4, 1.5, 1.1/0.01), 2)
    # y = np.round(np.linspace(-180, 180, 360/0.01), 2)

    # x = np.round(np.linspace(0.4, 1.5, int(1.1/0.01)), 2)
    # y = np.linspace(-180, 180, 360 + 1)
    # # z = []
    # # print(x)
    # for d in x:
    #     for yaw in y:
    #         # print("{} {}".format(d, yaw))
    #         r[0].append(d)
    #         r[1].append(yaw)
    #         r[2].append(SOA.avoid_left(d, yaw))

    
    # r = np.array(r)
    # # plotmesh(r[0], r[1])
    # ax.scatter(r[0],r[1], r[2])
    # plt.show()




    






        
        

    


    
