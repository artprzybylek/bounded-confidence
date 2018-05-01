import pickle
import re
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


mp.rcParams['font.size'] = 11
mp.rcParams['axes.linewidth'] = .1
mp.rcParams['lines.linewidth'] = .1
mp.rcParams['patch.linewidth'] = .1


titles = {
    'results/avg_freq_{}.pkl'.format('cg_200'): 'Network: complete graph, n=200',
    'results/avg_freq_{}.pkl'.format('ba_200_6'): 'Network: Barabasi-Albert, n=200, m=6',
    'results/avg_freq_{}.pkl'.format('ws_200_20_0.3'): 'Network: Watts-Strogatz, n=200, k=20, p=0.3'
    }


def plot_avg_freq(file, output_file):
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
    plt.title(titles[file])
    fig.tight_layout()
    plt.savefig(output_file, dpi=fig.dpi)



files = ['results/avg_freq_{}.pkl'.format(x) for x in [
    'ba_200_6', 'cg_200', 'ws_200_20_0.3'
    ]]
in_out = {
    'results/avg_freq_{}.pkl'.format(x): re.sub('\.', ',', 'plots/avg_freq_{}'.format(x))+'.pdf'
    for x in [
        'ba_200_6', 'cg_200', 'ws_200_20_0.3'
        ]
    }


for f in in_out:
    plot_avg_freq(f, in_out[f])
plt.show()