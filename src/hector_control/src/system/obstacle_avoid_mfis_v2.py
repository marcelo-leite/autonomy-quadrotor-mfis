
from array import array
from cProfile import label
from dataclasses import replace
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
        k = 0.3

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
    
        k_sb = xo[0]/4
        yS = mb.trimf(xo,[xo[0], xo[0], xo[0] - k_sb]) +  mb.trimf(xo,[xo[0] - 7*k_sb, xo[0] - 8*k_sb, xo[0] - 8*k_sb])
        ySE = mb.trimf(xo,[xo[0], xo[0] - k_sb, xo[0] - 2*k_sb])
        yE = mb.trimf(xo,[xo[0] - k_sb, xo[0] - 2*k_sb, xo[0] - 3*k_sb])
        yNE = mb.trimf(xo,[xo[0] - 2*k_sb, xo[0] - 3*k_sb, xo[0] - 4*k_sb])
        yN = mb.trimf(xo,[xo[0] - 3*k_sb, xo[0] - 4*k_sb, xo[0] - 5*k_sb])   
        yNO = mb.trimf(xo,[xo[0] - 4*k_sb, xo[0] - 5*k_sb, xo[0] - 6*k_sb])
        yO = mb.trimf(xo,[xo[0] - 5*k_sb, xo[0] - 6*k_sb, xo[0] - 7*k_sb])
        ySO = mb.trimf(xo,[xo[0] - 6*k_sb, xo[0] - 7*k_sb, xo[0] - 8*k_sb])
        # 
        self.FIS_OAFront.finput.addmb(1, yS)
        self.FIS_OAFront.finput.addmb(1, ySE)
        self.FIS_OAFront.finput.addmb(1, yE)
        self.FIS_OAFront.finput.addmb(1, yNE)
        self.FIS_OAFront.finput.addmb(1, yN)
        self.FIS_OAFront.finput.addmb(1, yNO)
        self.FIS_OAFront.finput.addmb(1, yO)
        self.FIS_OAFront.finput.addmb(1, ySO)

        self.FIS_OABack.finput.addmb(1, yS)
        self.FIS_OABack.finput.addmb(1, ySE)
        self.FIS_OABack.finput.addmb(1, yE)
        self.FIS_OABack.finput.addmb(1, yNE)
        self.FIS_OABack.finput.addmb(1, yN)
        self.FIS_OABack.finput.addmb(1, yNO)
        self.FIS_OABack.finput.addmb(1, yO)
        self.FIS_OABack.finput.addmb(1, ySO)


        self.FIS_OALeft.finput.addmb(1, yS)
        self.FIS_OALeft.finput.addmb(1, ySE)
        self.FIS_OALeft.finput.addmb(1, yE)
        self.FIS_OALeft.finput.addmb(1, yNE)
        self.FIS_OALeft.finput.addmb(1, yN)
        self.FIS_OALeft.finput.addmb(1, yNO)
        self.FIS_OALeft.finput.addmb(1, yO)
        self.FIS_OALeft.finput.addmb(1, ySO)

        self.FIS_OARight.finput.addmb(1, yS)
        self.FIS_OARight.finput.addmb(1, ySE)
        self.FIS_OARight.finput.addmb(1, yE)
        self.FIS_OARight.finput.addmb(1, yNE)
        self.FIS_OARight.finput.addmb(1, yN)
        self.FIS_OARight.finput.addmb(1, yNO)
        self.FIS_OARight.finput.addmb(1, yO)
        self.FIS_OARight.finput.addmb(1, ySO)

        # MEMBERSHIP OUTPUT
        self.FIS_OAFront.foutput.addmb(0, yS)
        self.FIS_OAFront.foutput.addmb(0, ySE)
        self.FIS_OAFront.foutput.addmb(0, yE)
        self.FIS_OAFront.foutput.addmb(0, yNE)
        self.FIS_OAFront.foutput.addmb(0, yN)
        self.FIS_OAFront.foutput.addmb(0, yNO)
        self.FIS_OAFront.foutput.addmb(0, yO)
        self.FIS_OAFront.foutput.addmb(0, ySO)

        self.FIS_OABack.foutput.addmb(0, yS)
        self.FIS_OABack.foutput.addmb(0, ySE)
        self.FIS_OABack.foutput.addmb(0, yE)
        self.FIS_OABack.foutput.addmb(0, yNE)
        self.FIS_OABack.foutput.addmb(0, yN)
        self.FIS_OABack.foutput.addmb(0, yNO)
        self.FIS_OABack.foutput.addmb(0, yO)
        self.FIS_OABack.foutput.addmb(0, ySO)


        self.FIS_OALeft.foutput.addmb(0, yS)
        self.FIS_OALeft.foutput.addmb(0, ySE)
        self.FIS_OALeft.foutput.addmb(0, yE)
        self.FIS_OALeft.foutput.addmb(0, yNE)
        self.FIS_OALeft.foutput.addmb(0, yN)
        self.FIS_OALeft.foutput.addmb(0, yNO)
        self.FIS_OALeft.foutput.addmb(0, yO)
        self.FIS_OALeft.foutput.addmb(0, ySO)

        self.FIS_OARight.foutput.addmb(0, yS)
        self.FIS_OARight.foutput.addmb(0, ySE)
        self.FIS_OARight.foutput.addmb(0, yE)
        self.FIS_OARight.foutput.addmb(0, yNE)
        self.FIS_OARight.foutput.addmb(0, yN)
        self.FIS_OARight.foutput.addmb(0, yNO)
        self.FIS_OARight.foutput.addmb(0, yO)
        self.FIS_OARight.foutput.addmb(0, ySO)

        # self.FIS_OALeft.finput.plot()
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

        path_d = "/home/marc/ros-ws/theconstructcore-ws/quadrotor-ws/src/hector_control/src/system/datarule/v2/"
        datarule_b = pd.read_csv(path_d + str("datarule_rback.csv"), delimiter=',')
        datarule_f = pd.read_csv(path_d +  str("datarule_rfront.csv"))
        datarule_r = pd.read_csv(path_d + str("datarule_rright.csv"))
        datarule_l = pd.read_csv(path_d + str("datarule_rleft.csv"))

        # datarule_b["D_BACK"].iloc
        # print(datarule_b.values)
        def replace_label(data):
            data = data.replace("S",0)
            data = data.replace("SE",1)
            data = data.replace("E",2)
            data = data.replace("NE",3)
            data = data.replace("N",4)
            data = data.replace("NO",5)
            data = data.replace("O",6)
            data = data.replace("SO",7)

            data = data.replace("P",0)
            data = data.replace("M",1)
            data = data.replace("G",2)

            return data


        # REPLACE BACK
        datarule_b = replace_label(datarule_b)

        # REPLACE FRONT
        datarule_f = replace_label(datarule_f)

        # REPLACE RIGHT
        datarule_r = replace_label(datarule_r)

        # REPLACE LEFT
        datarule_l = replace_label(datarule_l)

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


# PLOT FUZZY OUTPUT UNIVERSE
def  foutput_universe():

    ax = plt.axes(projection='3d')
    SOA = ObstacleAvoid(0.4,2)
    x = np.linspace(0.4, 2, 30)
    y = np.linspace(-180, 180, 30)
    x = np.around(x, 1)
    y = np.around(y, 0)

    r = [[], [], []]
    for d in x:
        for yaw in y:
            r[0].append(d)
            r[1].append(yaw)
            r[2].append(SOA.avoid_back(d, yaw))

    r[0] = np.around(r[0], decimals=1)
    r = np.array(r)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            for k in range(len(r[0])):
                if(r[0][k] == X[i,j]):
                    if(r[1][k] == Y[i, j]):
                        Z[i,j] = r[2][k]
                        break

    # ax.contour3D(X, Y, Z, 50, cmap='binary')    
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    plt.show()

def finput1_plot():
    SOA = ObstacleAvoid(0.4,2)
    x = SOA.FIS_OAFront.finput.v[0].x
    f = SOA.FIS_OAFront.finput.v[0].f
    vl = ["P", "M", "G"]
    for i in range(len(f)):
        plt.plot(x,f[i], label=vl[i])
    
    # plt.ylim([0,1])
    # plt.xlim([0.4,2])

    plt.xlabel("Distância")
    plt.ylabel("Pertinência")
    plt.legend()
    plt.show()

def finput2_plot():
    SOA = ObstacleAvoid(0.4,2)
    x = SOA.FIS_OAFront.finput.v[1].x
    f = SOA.FIS_OAFront.finput.v[1].f
    vl = ["S", "SE", "E", "NE", "N", "NO", "O", "SO"]
    
    for i in range(len(f)):
        # plt.plot(x,f[i])
        j = np.argmax(f[i])
        # plt.text(x[j] - 5, f[i][j] + 0.01, vl[i])
        plt.plot(x,f[i], label=vl[i])
    plt.xticks(np.arange(-180, 180, 45))
    plt.xlabel("Ângulo")
    plt.xlim([-180,180])
    plt.ylim([0,1])
    plt.ylabel("Pertinência")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()


if __name__ == '__main__':
    # foutput_universe()
    finput1_plot()
    







    






        
        

    


    
