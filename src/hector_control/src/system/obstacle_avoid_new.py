
import sys
import os
from tkinter import font

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D

import time

from regex import F

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
        self.FIS_OA  = sifuzzy(5,1)
           
        # Domain Input
        xi = np.linspace(d_min,d_max, round(((d_max - d_min)/0.01) + 1))
        xa = np.linspace(-180,180, round(((360)/0.01) + 1))
        # Domain Output (Consequente)
        xo = np.linspace(-180,180, round(((360)/0.01) + 1))

        # Set Domain Input
        # 0 - F
        # 1 - R
        # 2 - L
        # 3 - B
        # Set Domain Distance Inputs
        for i in range(4):
            self.FIS_OA.finput.setdm(i, xi)
        
        # Set Domain Angle Input
        self.FIS_OA.finput.setdm(4, xa)
        # Set Domain Output
        self.FIS_OA.foutput.setdm(0, xo)

        # CREAT MEMBERSHIP INPUT
        k = 0.2

        m0 = mb.gaussmf(xi, [k, d_min])
        m1 = mb.gaussmf(xi, [k, d_min + (d_max - d_min)/4])
        m2 = mb.gaussmf(xi, [k, d_min + (d_max - d_min)/2])
        m3 = mb.gaussmf(xi, [k, d_min + 3*(d_max - d_min)/4])
        m4 = mb.gaussmf(xi, [k, d_max])

        # FIS_AO ADD MEMBERSHIP INPUT
        self.FIS_OA.finput.addmb(0, m0)
        self.FIS_OA.finput.addmb(0, m1)
        self.FIS_OA.finput.addmb(0, m2)
        self.FIS_OA.finput.addmb(0, m3)
        self.FIS_OA.finput.addmb(0, m4)
        
        self.FIS_OA.finput.addmb(1, m0)
        self.FIS_OA.finput.addmb(1, m1)
        self.FIS_OA.finput.addmb(1, m2)
        self.FIS_OA.finput.addmb(1, m3)
        self.FIS_OA.finput.addmb(1, m4)

        self.FIS_OA.finput.addmb(2, m0)
        self.FIS_OA.finput.addmb(2, m1)
        self.FIS_OA.finput.addmb(2, m2)
        self.FIS_OA.finput.addmb(2, m3)
        self.FIS_OA.finput.addmb(2, m4)

        self.FIS_OA.finput.addmb(3, m0)
        self.FIS_OA.finput.addmb(3, m1)
        self.FIS_OA.finput.addmb(3, m2)
        self.FIS_OA.finput.addmb(3, m3)
        self.FIS_OA.finput.addmb(3, m4)



        # CREAT MEMBERSHIP OUTPUT
        # mf0 = mb.trimf(xo, [180])

        # FIS_AO ADD MEMBERSHIP INPUT
        self.FIS_OA.finput.addmb(3, m0)
        self.FIS_OA.finput.addmb(3, m1)
        self.FIS_OA.finput.addmb(3, m2)
        self.FIS_OA.finput.addmb(3, m3)
        self.FIS_OA.finput.addmb(3, m4)


        # FUZZY OUTPUT
        # 0 - ANGULO GRANDE DIVISORIO 
        
        # 1 - ANGULO NEGATIVO GRANDE
        # 2 - ANGULO NEGATIVO MEDIO
        # 3 - ANGULO NEGATIVO PEQUENO
        
        # 4 - ANGULO PEQUENO DIVISORIO


        # 5 - ANGULO POSITIVO PEQUENO
        # 6 - ANGULO POSITIVO MEDIO
        # 7 - ANGULO POSITIVO GRANDE

        k_sb = xo[0]/4
        AGD = mb.trimf(xo,[xo[0], xo[0], xo[0] - k_sb]) +  mb.trimf(xo,[xo[0] - 7*k_sb, xo[0] - 8*k_sb, xo[0] - 8*k_sb])

        ANG = mb.trimf(xo,[xo[0], xo[0] - k_sb, xo[0] - 2*k_sb])
        ANM = mb.trimf(xo,[xo[0] - k_sb, xo[0] - 2*k_sb, xo[0] - 3*k_sb])
        ANP = mb.trimf(xo,[xo[0] - 2*k_sb, xo[0] - 3*k_sb, xo[0] - 4*k_sb])
        
        # ANMP = mb.trimf(xo,[xo[0] - 3*k_sb, xo[0] - 4*k_sb, xo[0] - 4*k_sb])   
        # APMP = mb.trimf(xo,[xo[0] - 4*k_sb, xo[0] - 4*k_sb, xo[0] - 5*k_sb])
        
        APD = mb.trimf(xo,[xo[0] - 3*k_sb, xo[0] - 4*k_sb, xo[0] - 5*k_sb])   

        APP = mb.trimf(xo,[xo[0] - 4*k_sb, xo[0] - 5*k_sb, xo[0] - 6*k_sb])
        APM = mb.trimf(xo,[xo[0] - 5*k_sb, xo[0] - 6*k_sb, xo[0] - 7*k_sb])
        APG = mb.trimf(xo,[xo[0] - 6*k_sb, xo[0] - 7*k_sb, xo[0] - 8*k_sb])
        

        self.FIS_OA.foutput.addmb(0, AGD)
        self.FIS_OA.foutput.addmb(0, ANG)
        self.FIS_OA.foutput.addmb(0, ANM)
        self.FIS_OA.foutput.addmb(0, ANP)

        self.FIS_OA.foutput.addmb(0, APD)
        
        self.FIS_OA.foutput.addmb(0, APP)
        self.FIS_OA.foutput.addmb(0, APM)
        self.FIS_OA.foutput.addmb(0, APG)

        # Add Dommain Angle Input

        self.FIS_OA.finput.v[4].f = self.FIS_OA.foutput.v[0].f



        # CREATE RULE
        #            F     R   L   B    THETA
        rule =  [
                    [0,    0,  0, "i",  0],
                    ["i",  0,  0, "i",  5],
                    ["i",  1,  1, "i",  5],
                    [0,    2,  "i", "i",  2],
                    


                ]
        pass
        
    def plotInput(self):
        self.FIS_OA.finput.plot()
        pass 
    def plotOutput(self):
        self.FIS_OA.foutput.plot()

    def avoid(self, d):
        return self.FIS_OA.mamfis([d])

# PLOT 
if __name__ == '__main__':

    SOA = ObstacleAvoid(0.4,3)
    SOA.plotInput()
    # SOA.plotOutput()
    

    






        
        

    


    
