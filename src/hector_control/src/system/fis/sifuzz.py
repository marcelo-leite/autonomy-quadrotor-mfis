
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# from membership.membership import membership

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

class funiverse:
    def __init__(self):
        self.f = []
        self.x = []
        pass

    def add_mb(self, f_mb):
        self.f.append(f_mb)
        
    def set_dm(self, x):
        self.x = x

class fset():
    def __init__(self, n, name):
        self.name = name
        self.mb = membership()
        self.v = []
        for i in range(n):
            self.v.append(funiverse())
        pass
    def addmb(self, i, f):
        self.v[i].add_mb(f)
    
    # AUTO GENERATE FUNCTION MEMBERSHIPS
    def automf(self, i, n):
        x = self.v[i].x
        dx = (x[len(x) - 1] - x[0])/(n - 1)
        f = []
        
        f.append(self.mb.trimf(x, [x[0], x[0], x[0] + dx]))
        
        temp = x[0]
        for j in range(1, n - 1):
            f.append(self.mb.trimf(x, [temp, temp + dx, temp + 2*dx]))
            temp = temp + dx
        
        f.append(self.mb.trimf(x, [x[len(x) - 1] - dx, x[len(x) - 1], x[len(x) - 1]]))
        
        for y in f:
            self.v[i].add_mb(y)
    
    def setdm(self,i, x):
        self.v[i].set_dm(x)
    
   


    # PLOT MEMBERSHIP
    def plot(self):
        len_v = len(self.v)

        if(len_v > 1):
            fig, axs = plt.subplots(int(len(self.v)))
            fig.suptitle(self.name + str(" Fuzzy"))

            for j in range(len(self.v)):
                for i in range(len(self.v[j].f)):


                    # plt.xticks(range(self.x[0], self.x[len(self.x) - 1]))

                    # plt.xlim([self.x[0], self.x[len(self.x) - 1]])
                    # axs[j].ylim([0, 5])

                    
                    axs[j].plot(self.v[j].x, self.v[j].f[i], label=i)
                    axs[j].set_title(self.name + " " + str(j))
                    axs[j].legend()
                    
                    
        else:
            for j in range(len(self.v)):
                for i in range(len(self.v[j].f)):
                    plt.plot(self.v[j].x, self.v[j].f[i], label=i)
                    plt.title(self.name + " " + str(j))
                    plt.legend()   
                    
                    plt.xticks(np.linspace(self.v[j].x[0], self.v[j].x[len(self.v[j].x) - 1], 9))
                    plt.xlim([self.v[j].x[0], self.v[j].x[len(self.v[j].x) - 1]])  
                    plt.ylim([0, 1])    

         
        plt.show()


class finput(fset):
    def __init__(self, n, name):
        super().__init__(n, name)


    def intersect(self, i, x0):
        pos = "inf"
        array = []
        for k in range(len(self.v[i].x)):
            if(abs(x0 - self.v[i].x[k]) <= 10**-7):
                pos = k
                break

        if( pos != "inf"):
            for j in range(len(self.v[i].f)):
                array.append(self.v[i].f[j][pos])
        else:
            print(x0)
            print("Não Encontrado")
            # print(x0)
        return array

class rule:
    def __init__(self):
        self.ruleset = []
        self.ruleop = None
        pass

    def set(self, dataset):
        self.ruleset = dataset
class defuzz:
    def __init__(self) -> None:
        pass
    # Center of Gravity (COG)
    def cog(self, x, u):
        aux_n = 0
        aux_d = 0
        for i in  range(len(x)):
            aux_n = x[i]*u[i] + aux_n
            aux_d = u[i] + aux_d

        z = aux_n/aux_d
        return z
        # pass
    # Bisector of Area Methods (BOA)
    def boa(self, u):
        pass
    # Weight Average Method
    def wam(self, u):
        pass
    # First of Maxima Method (FOM)
    def fom(self, x, u):
        index = np.argmax(u)
        z = x[index]
        return z
    # Last of Maxima Method (LOM)
    def lom(self, u):
        pass
    # Mean and Maxima Method (MOM)
    def mom(self, u):
        pass

class sifuzzy(defuzz):
    def __init__(self, n_in, n_out):
        
        self.finput = finput(n_in, "Input")
        self.foutput = fset(n_out, "Output")
        self.rule = rule()
        
    
    def mamfis(self, p, op):
        
        # INTERSECTION
        f_ativ = []
        for i in range(len(p)):
            f_ativ.append(self.finput.intersect(i, p[i]))

            
        # print(f_ativ)
        # ATIVATION REGRA
        aggr = []
        for r in self.rule.ruleset:
            # print(r)

            # RULE PREPOSITION INPUT AGGREGATION FMAX OR FMIN
            if( op == 0):
                aggr_p = 0
            elif( op == 1):
                aggr_p = 1
            
            for j in range(len(r) - 1):
                if(r[j] != "inf"):
                    if( op == 0):
                        aggr_p  = np.fmax(aggr_p, f_ativ[j][int(r[j])])
                    elif( op == 1):
                        aggr_p  = np.fmin(aggr_p, f_ativ[j][int(r[j])])
            # RULE PREPOSITION INPUT WITH OUTPUT AGGREGATION FMIN
            aux = len(r) - 1
            aggr.append(np.fmin(aggr_p, self.foutput.v[0].f[int(r[aux])]))
        
        # UNIAO SETS FUZZY
        aggr_t = 0
        for j in range(len(aggr)):
            # print(np.round(np.array(aggr[j]), 2))
            aggr_t  = np.fmax(aggr_t, aggr[j])
        # DEFUZZ CENTROID
        # plt.plot(self.foutput.v[0].x, aggr_t)
        # plt.show()

        x = self.foutput.v[0].x
        u = aggr_t
        

        z = self.fom(x, u)
        return z
        
    def sugfis(self):
        pass


