from matplotlib import markers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def path_square(x,y):
    lx, ly = 1, 1
    xr = x - lx/2
    yr = y - ly/2
    p = patches.Rectangle((xr, yr), lx, ly, linewidth=0, edgecolor="black", facecolor="black")
    return p

df = pd.read_csv('datapose.csv', delimiter=',')
x = df['x'].to_numpy()
y = df['y'].to_numpy()
# print(x)


fig, ax = plt.subplots()

# plt.scatter(6.5,6.5, marker='s', s=1000, c="black")

# CONFIG

plt.xlim([0,10])
plt.ylim([0,10])

plt.xticks(np.arange(-1,13, 1))
plt.yticks(np.arange(-2,12, 1))

# ADD OBSTACLE PLOT
pilar = [path_square(2.48639, 2.52913), path_square(4.49723,-0.544255), path_square(7.54201, 2.47525), path_square(1.55461, 7.46992), path_square(5.46835, 7.49662), path_square(10.9623, 5.51946)]

for p in pilar:
    ax.add_patch(p)

plt.scatter(0,0, c="green")
plt.scatter(10,10, c="red")
# PLOT
plt.ylabel("Eixo Y")
plt.xlabel("Eixo X")
# plt.grid()
plt.plot(x,y)
plt.savefig('destination_path.eps', format='eps')
plt.show()
# plt.gcf().autofmt_xdate()


