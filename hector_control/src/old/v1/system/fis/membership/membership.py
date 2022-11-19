# import membership as fmb
import numpy as np


class membership:
    # Membership
    def __init__(self):
        pass
    
    
    def gaussmf(self, x, p):
        self.x = np.array(x)
        self.f = np.zeros(len(self.x))
        
        # Gaussian Membership Function   
        
        for i in  range(len(x)):
            a = ((-1)*(x[i] - p[1])**2)/(2*p[0]**2)
            self.f[i] = np.exp(a)
        return self.f
        pass
    
    def trapmf(self, x, p):

        f = np.zeros(len(x))

        for i in  range(len(x)):

            if((p[1] - p[0]) != 0):
                t1 = (x[i] - p[0])/(p[1] - p[0])
            else:
                t1 = 1
            t2 = 1

            if((p[3] - p[2]) != 0):
                t3 = (p[3] - x[i])/(p[3] - p[2])
            else:
                t3 = 1
            

            k1 = np.min([t1, t2, t3])
            k2 = 0
            f[i] = np.max([k1, k2])
        
        return f
        
    
    def trimf(self, x, p):
        self.x = np.array(x)
        self.f = np.zeros(len(x))
        
        # Triangular Membership Function    
        
        for i in  range(len(self.x)):
            
            if(self.x[i] < p[0]):
                self.f[i] = 0
                
            elif(p[0] <= self.x[i] and self.x[i] < p[1]):
                if((p[1] - p[0]) != 0):
                    self.f[i] = (1/(p[1] - p[0]))*(self.x[i] - p[0])
                else:
                    self.f[i] = 1
                
            elif(p[1] <= self.x[i] and self.x[i] <= p[2]):
                if((p[2] - p[1]) != 0):
                    self.f[i] = 1 - (1/(p[2] - p[1]))*(self.x[i] - p[1])
                else:
                    self.f[i] = 1
                
            elif(x[i] > p[2]):
                self.f[i] = 0
        return self.f


# mb = membership()

# x_food = np.linspace(0,10,100)

# a = mb.trimf(x_food, [1,5,8])

# print(a)

