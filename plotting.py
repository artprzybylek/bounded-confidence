import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def plot_avg_freq(file):
    with open(file, "rb") as f:
        avg_freq = pickle.load(f)
    y = np.linspace(0.01, 0.4, len(avg_freq))
    opinions = np.linspace(0, 1, 101)
    X = np.tile(opinions, (40, 1))
    Y = np.tile(y, (101, 1)).T
    Z = np.array(avg_freq)
    Z_max = np.max(Z)
    Z[Z == 0] = np.nan
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, vmin=0, vmax=Z_max, cmap=cm.gist_rainbow, rstride=1, cstride=1,
                    linewidth=.2, edgecolor='k')
    ax.set_xlabel('opinion')
    ax.set_ylabel('confidence level')
    ax.set_zlabel('opinion frequency')


plot_avg_freq("barabasi_albert_graph(625,4)_avg_freq_1.pkl")
plt.show()
