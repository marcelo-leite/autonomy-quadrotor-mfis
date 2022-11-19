
import sys
import os
from tkinter import font

import numpy as np
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
fsys = sifuzzy(1,1)   


class ObstacleAvoid:
    def __init__(self, d_min, d_max):

        # Instance FIS Obstacle Avoid to each direction
        self.FIS_OALeft  = sifuzzy(1,1)   
        self.FIS_OARight = sifuzzy(1,1)   
        self.FIS_OAFront = sifuzzy(1,1)   
        self.FIS_OABack  = sifuzzy(1,1)  

        # Domain Input
        xi_d = np.linspace(d_min,d_max, round(((d_max - d_min)/0.01) + 1))
        # print(xi_d)
        # print(xi_d)

        # Domain Output (Consequente)
       
        # xo_r = np.linspace(0,90, 101)
        # xo_l = np.linspace(-90, 0, 101)
        # xo_f = np.linspace(-180,-90,101)
        # xo_b = np.linspace(0,90,101)

        xo_r = np.linspace(-30,90, 101)
        xo_l = np.linspace(-90, 30, 101)
        xo_f = np.linspace(-180,-60,101)
        xo_b = np.linspace(-30,90,101)

        # Set Domain Input
        self.FIS_OALeft.finput.setdm(0, xi_d)
        self.FIS_OARight.finput.setdm(0, xi_d)
        self.FIS_OAFront.finput.setdm(0, xi_d)
        self.FIS_OABack.finput.setdm(0, xi_d)

        # Set Domain Output
        self.FIS_OALeft.foutput.setdm(0, xo_l)
        self.FIS_OARight.foutput.setdm(0, xo_r)
        self.FIS_OAFront.foutput.setdm(0, xo_f)
        self.FIS_OABack.foutput.setdm(0, xo_b)

        # CREAT MEMBERSHIP INPUT
        k = 0.2

        m0 = mb.gaussmf(xi_d, [k, d_min])
        m1 = mb.gaussmf(xi_d, [k, d_min + (d_max - d_min)/4])
        m2 = mb.gaussmf(xi_d, [k, d_min + (d_max - d_min)/2])
        m3 = mb.gaussmf(xi_d, [k, d_min + 3*(d_max - d_min)/4])
        m4 = mb.gaussmf(xi_d, [k, d_max])

        # FIS_AORight
        self.FIS_OARight.finput.addmb(0, m0)
        self.FIS_OARight.finput.addmb(0, m1)
        self.FIS_OARight.finput.addmb(0, m2)
        self.FIS_OARight.finput.addmb(0, m3)
        self.FIS_OARight.finput.addmb(0, m4)

        # FIS_AOLeft
        self.FIS_OALeft.finput.addmb(0, m0)
        self.FIS_OALeft.finput.addmb(0, m1)
        self.FIS_OALeft.finput.addmb(0, m2)
        self.FIS_OALeft.finput.addmb(0, m3)
        self.FIS_OALeft.finput.addmb(0, m4)

        # FIS_AOBack
        self.FIS_OABack.finput.addmb(0, m0)
        self.FIS_OABack.finput.addmb(0, m1)
        self.FIS_OABack.finput.addmb(0, m2)
        self.FIS_OABack.finput.addmb(0, m3)
        self.FIS_OABack.finput.addmb(0, m4)


        # FIS_AOFront
        self.FIS_OAFront.finput.addmb(0, m0)
        self.FIS_OAFront.finput.addmb(0, m1)
        self.FIS_OAFront.finput.addmb(0, m2)
        self.FIS_OAFront.finput.addmb(0, m3)
        self.FIS_OAFront.finput.addmb(0, m4)

        # CREAT MEMBERSHIP OUTPUT
        self.FIS_OARight.foutput.automf(0, 5)
        self.FIS_OALeft.foutput.automf(0, 5)
        self.FIS_OAFront.foutput.automf(0, 5)
        self.FIS_OABack.foutput.automf(0, 5)

        # RULE

        # 0: VL
        # 1: L
        # 2: M
        # 3: H
        # 4: VH


        # IF Do VERY LOW THEN ANGLE VERY HIGH
        # IF Do MEDIUM THEN ANGLE MEDIUM
        # IF Do VERY HIGHT THEN ANGLE VERY LOW   
        rule_r =   [[0,4],
                    [2,2],
                    [4,0]]


        # IF Do VERY LOW THEN ANGLE VERY LOW
        # IF Do MEDIUM THEN ANGLE MEDIUM
        # IF Do VERY HIGHT THEN ANGLE VERY HIGH   
        rule_f =   [[0,0],
                    [2,2],
                    [4,4]]

        # IF Do VERY LOW THEN ANGLE VERY LOW
        # IF Do MEDIUM THEN ANGLE MEDIUM
        # IF Do VERY HIGHT THEN ANGLE VERY HIGH   
        rule_l =   [[0,0],
                    [2,2],
                    [4,4]]

        # IF Do VERY LOW THEN ANGLE VERY LOW
        # IF Do MEDIUM THEN ANGLE MEDIUM
        # IF Do VERY HIGHT THEN ANGLE VERY HIGH   

        rule_b =   [[0,0],
                    [2,2],
                    [4,4]]

        # SET RULE
        self.FIS_OARight.rule.set(rule_r)
        self.FIS_OALeft.rule.set(rule_l)
        self.FIS_OAFront.rule.set(rule_f)
        self.FIS_OABack.rule.set(rule_b)



        pass
        
    def plot(self):
        pass 
    def avoid_left(self, d):
        return self.FIS_OALeft.mamfis([d])
        
    def avoid_right(self, d):
        return self.FIS_OARight.mamfis([d])
        
    def avoid_back(self, d):
        return self.FIS_OABack.mamfis([d])
        
    def avoid_front(self, d):
        return self.FIS_OAFront.mamfis([d])


# PLOT 
if __name__ == '__main__':
    def PLOT_FOUTPUT(SOA):

        yf = SOA.FIS_OAFront.foutput.v[0].f
        xf = SOA.FIS_OAFront.foutput.v[0].x

        yb = SOA.FIS_OABack.foutput.v[0].f
        xb = SOA.FIS_OABack.foutput.v[0].x

        yl = SOA.FIS_OALeft.foutput.v[0].f
        xl = SOA.FIS_OALeft.foutput.v[0].x

        yr = SOA.FIS_OARight.foutput.v[0].f
        xr = SOA.FIS_OARight.foutput.v[0].x

        fig, axs = plt.subplots(2, 2)
        fig.suptitle('Fuzzy Output', y=1)
        

        fs = 10
        
        axs[0, 0].set_title('FRONT', fontsize=fs, fontweight="bold")
        axs[0, 1].set_title('BACK', fontsize=fs, fontweight="bold")
        axs[1, 0].set_title('LEFT', fontsize=fs, fontweight="bold")
        axs[1, 1].set_title('RIGHT', fontsize=fs, fontweight="bold")

        ls = 9
        # CONFIGURE TICK
        axs[0,0].tick_params(labelsize=ls)
        axs[0,1].tick_params(labelsize=ls)
        axs[1,0].tick_params(labelsize=ls)
        axs[1,1].tick_params(labelsize=ls)

        axs[0,0].set_xticks(np.linspace(xf[0], xf[-1], 5))
        axs[0,1].set_xticks(np.linspace(xb[0], xb[-1], 5))
        axs[1,0].set_xticks(np.linspace(xl[0], xl[-1], 5))
        axs[1,1].set_xticks(np.linspace(xr[0], xr[-1], 5))


        axs[0,0].set_ylim([0, 1])
        axs[0,0].set_xlim([xf[0], xf[-1]])

        axs[0,1].set_ylim([0, 1])
        axs[0,1].set_xlim([xb[0], xb[-1]])

        axs[1,0].set_ylim([0, 1])
        axs[1,0].set_xlim([xl[0], xl[-1]])

        axs[1,1].set_ylim([0, 1])
        axs[1,1].set_xlim([xr[0], xr[-1]])
     
        # PLOT
        for i in range(len(yf)):
            axs[0, 0].plot(xf, yf[i], label=i)
            axs[0, 1].plot(xb, yb[i], label=i)
            axs[1, 0].plot(xl, yl[i], label=i)
            axs[1, 1].plot(xr, yr[i], label=i)
        axs[0, 0].legend(loc="upper right")
        axs[0, 1].legend(loc="upper right")
        axs[1, 0].legend(loc="upper right")
        axs[1, 1].legend(loc="upper right")

        for ax in axs.flat:
            ax.set(xlabel='Ângulo', ylabel='Pertinência')
            
        # # Hide x labels and tick labels for top plots and y ticks for right plots.
        axs[0,0].set(xlabel='', ylabel='Pertinência')   
        axs[0,1].set(xlabel='', ylabel='') 
        axs[1,1].set(xlabel='Ângulo', ylabel='')  
        
        
        fig.tight_layout()
        plt.show()

        pass
    def PLOT_FINPUT(SOA):
        # DATA
        yd = SOA.FIS_OAFront.finput.v[0].f
        xd = SOA.FIS_OAFront.finput.v[0].x

         # PLOT ANTECEDENTS
        for i in range(len(yd)):
            plt.plot(xd, yd[i], label=i)
        plt.title("Fuzzy Input")
        plt.xlabel("Distância")
        plt.ylabel("Pertinência")
        plt.ylim(0,1)
        plt.xlim(xd[0], xd[-1]) 
        plt.xticks(np.linspace(xd[0], xd[-1], 5))
        plt.tick_params(labelsize=10)
        plt.legend(loc="right")
        plt.show()
        pass
    def PLOT_OUTPUT(self):
        xr = []
        yr = []

        xf = []
        yf = []

        xb = []
        yb = []

        xl = []
        yl = []

        # PLOT SAIDA

        for i in np.arange(0.4, 3 + 0.01, 0.01):
            
            xl.append(i)
            yl.append(SOA.FIS_OALeft.mamfis([i]))

            xr.append(i)
            yr.append(SOA.FIS_OARight.mamfis([i]))

            xf.append(i)
            yf.append(SOA.FIS_OAFront.mamfis([i]))

            xb.append(i)
            yb.append(SOA.FIS_OABack.mamfis([i]))

        xl = np.array(xl)
        xb = np.array(xb)
        xf = np.array(xf)
        xr = np.array(xr)
    
        fig, axs = plt.subplots(2, 2)
        # fig.suptitle('Fuzzy Output', y=1)
        

        fs = 10
        
        axs[0, 0].set_title('FRONT', fontsize=fs, fontweight="bold")
        axs[0, 1].set_title('BACK', fontsize=fs, fontweight="bold")
        axs[1, 0].set_title('LEFT', fontsize=fs, fontweight="bold")
        axs[1, 1].set_title('RIGHT', fontsize=fs, fontweight="bold")

        ls = 9
        # CONFIGURE TICK
        axs[0,0].tick_params(labelsize=ls)
        axs[0,1].tick_params(labelsize=ls)
        axs[1,0].tick_params(labelsize=ls)
        axs[1,1].tick_params(labelsize=ls)

        axs[0,0].set_xticks(np.linspace(xf[0], xf[-1], 5))
        axs[0,1].set_xticks(np.linspace(xb[0], xb[-1], 5))
        axs[1,0].set_xticks(np.linspace(xl[0], xl[-1], 5))
        axs[1,1].set_xticks(np.linspace(xr[0], xr[-1], 5))

        axs[0,0].set_yticks(np.linspace(yf[0], yf[-1], 6))
        axs[0,1].set_yticks(np.linspace(yb[0], yb[-1], 6))
        axs[1,0].set_yticks(np.linspace(yl[0], yl[-1], 6))
        axs[1,1].set_yticks(np.linspace(yr[-1], yr[0], 6))


        axs[0,0].set_ylim([yf[0], yf[-1]])
        axs[0,0].set_xlim([xf[0], xf[-1]])

        axs[0,1].set_ylim([yb[0], yb[-1]])
        axs[0,1].set_xlim([xb[0], xb[-1]])

        axs[1,0].set_ylim([yl[0], yl[-1]])
        axs[1,0].set_xlim([xl[0], xl[-1]])

        axs[1,1].set_ylim([yr[-1], yr[0]])
        axs[1,1].set_xlim([xr[0], xr[-1]])
     
        # PLOT
        
        axs[0, 0].plot(xf, yf)
        axs[0, 1].plot(xb, yb)
        axs[1, 0].plot(xl, yl)
        axs[1, 1].plot(xr, yr)
        

        for ax in axs.flat:
            ax.set(xlabel='Distância', ylabel='Ângulo')
            
        # # Hide x labels and tick labels for top plots and y ticks for right plots.
        axs[0,0].set(xlabel='', ylabel='Ângulo')   
        axs[0,1].set(xlabel='', ylabel='') 
        axs[1,1].set(xlabel='Distância', ylabel='')  
        
        
        fig.tight_layout()
        plt.show()
        

    SOA = ObstacleAvoid(0.4,3)

    # PLOT_FINPUT(SOA)
    # PLOT_FOUTPUT(SOA)
    PLOT_OUTPUT(SOA)
    
    

    






        
        

    


    
