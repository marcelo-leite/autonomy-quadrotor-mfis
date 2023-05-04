from cProfile import label
from matplotlib import markers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os



# SIMU A) s1   20 17
# SIMU B) s18  -2 80
cwd = os.path.realpath(os.path.dirname(__file__))
path_d = str(cwd) + "/../database/test/trot"

dfl = []
# dfl.append(pd.read_csv(f'{path_d}/datapose-s10-{0}-{0}-fa1-fr0.5.csv', delimiter=','))
dfl.append(pd.read_csv(f'{path_d}/datapose-s3-{21}-{18}-fa0.5-fr0.5.csv', delimiter=','))
# dfl.append(pd.read_csv(f'{path_d}/datapose-s3-{21}-{18}-fa1-fr0.5.csv', delimiter=','))
# dfl.append(pd.read_csv(f'datapose-s1-{21}-{18}-fa1-fr1.csv', delimiter=','))
# dfl.append(pd.read_csv(f'datapose-s1-{21}-{18}-fa1-fr1.csv', delimiter=','))

alfa = []
beta = []
t = []

for df in dfl:
    alfa.append(df['alfa'].to_numpy())
    beta.append(df['beta'].to_numpy())
    t.append(df['t'].to_numpy())


fig, ax = plt.subplots()




# PLOT

# plt.xticks(np.arange(-5, 22, 5))
# plt.yticks(np.arange(-5, 25, 5))
# plt.grid()
lw = 2
k = 0.7

plt.xlim([177, 240])
plt.ylim([40, 51])


# s_size = 5
plt.plot(t[0], np.rad2deg(alfa[0]), label=f"rotação")
plt.plot(t[0], np.rad2deg(beta[0]), label=f"setpoint")
plt.legend()
plt.ylabel("Ângulo (Graus)")
plt.xlabel("Tempo (s)")



plt.rcParams["figure.figsize"] = (6,6)
plt.subplots_adjust(left=0.1, right=0.9, top=0.98, bottom=0.1)
# plt.savefig(f'simu({pose[1][0]}:{pose[1][1]}).png', format='png')
plt.show()
plt.gcf().autofmt_xdate()


