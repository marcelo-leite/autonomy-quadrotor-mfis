from cProfile import label
from pickle import APPEND
from matplotlib import markers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def path_square(x,y):
    lx, ly = 1, 1
    xr = float(x) - lx/2
    yr = float(y) - ly/2
    p = patches.Rectangle((xr, yr), lx, ly, linewidth=0, edgecolor="black", facecolor="black")
    return p
def distance_to_cicle(p, q):
    x = np.zeros(len(q[0]))
    y = np.zeros(len(q[0]))
    for i in range(len(q[0])):
        for j in range(len(p[0])):
            d = np.sqrt((p[0][j] - q[0][i])**2 + (p[1][j] - q[1][i])**2)
            if(d <= 2):
                x[i] = q[0][i]
                y[i] = q[1][i]
                break
    return x, y

# df0 = pd.read_csv('datapose.csv', delimiter=',')
# df1 = pd.read_csv('datapose1.csv', delimiter=',')
# df2 = pd.read_csv('datapose2.csv', delimiter=',')

df = pd.read_csv('datapose-s13-17-20.csv', delimiter=',')
x = df['x'].to_numpy()
y = df['y'].to_numpy()
s = df['s'].to_numpy()
# x0 = df0['x'].to_numpy()
# y0 = df0['y'].to_numpy()



# x1 = df1['x'].to_numpy()
# y1 = df1['y'].to_numpy()

# x2 = df2['x'].to_numpy()
# y2 = df2['y'].to_numpy()
# s2 = df2['s'].to_numpy()

y_fis = y[s == 1]
x_fis = x[s == 1]

y_fpa = y[s == 0]
x_fpa = x[s == 0]

fig, ax = plt.subplots()

xo = ['2.48639', '4.49723', '7.54201', '1.55461', '5.46835', '10.9623', '15.1737', '17.872', '18.816', '11.0321', '8.25934', '11.6691', '8.91221', '2.94851', '7.19557', '13.0949', '12.4967']
yo = ['2.52913', '-0.544255', '2.47525', '7.46992', '7.49662', '5.51946', '6.91589', '4.03057', '11.4136', '8.92808', '10.5307', '2.13023', '-2.90968', '12.3713', '14.9949', '12.2376', '16.9632']
xo = np.float_(xo)
yo = np.float_(yo)

pilar = []
for i in range(len(xo)):
    pilar.append(path_square(float(xo[i]), float(yo[i])))

for p in pilar:
    ax.add_patch(p)

plt.scatter(0,0, c="green")
plt.scatter(17,20, c="red")
# PLOT

# CONFIG

plt.xlim([-2,22])
plt.ylim([-2,22])

plt.ylabel("Eixo Y")
plt.xlabel("Eixo X")
plt.xticks(np.arange(-2, 26, 2))
plt.yticks(np.arange(-2, 26, 2))
lw = 2
k = 0.7

# va = distance_to_cicle([xo, yo], [x0, y0])


# plt.scatter(x0,y0, linewidth=lw, alpha=k, label="APF")
# plt.scatter(va[0],va[1], linewidth=lw, alpha=k, label="FIS")


s_size = 4
# plt.plot(x,y)
plt.scatter(x_fis, y_fis, s=s_size, label="FIS", linewidths=1)
plt.scatter(x_fpa, y_fpa, s=s_size, label="FPA")

# plt.plot(x2,y2,c="black" ,linewidth=lw, alpha=k, label="NEW")
# plt.plot(x0,y0,linewidth=lw, alpha=k, label="OLD")

# plt.plot(x1,y1, linewidth=lw, alpha=k, label="Simulação 2")
# plt.plot(x2,y2, linewidth=lw, alpha=k, label="Simulação 3")

plt.legend()
plt.grid()
# plt.savefig('simu_path.eps', format='eps')
plt.show()
plt.gcf().autofmt_xdate()


