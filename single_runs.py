import matplotlib.pyplot as plt
import networkx as nx
import matplotlib as mp
import pickle

from functions import set_random_opinions
from BC import bounded_confidence, select_all


mp.rcParams['font.size'] = 13


def simulations(network, res_f):
    e = [0.05, 0.15, 0.25, 0.35]
    for index in range(4):
        eps = e[index]
        set_random_opinions(network)
        opinions_dynamics = bounded_confidence(network, eps, eps, select_all)
        with open('results/eps_{}'.format(eps) + res_f, "bw") as fh:
            pickle.dump(opinions_dynamics, fh)


def plots(filename, res_f):
    e = [0.05, 0.15, 0.25, 0.35]
    f, axarr = plt.subplots(2, 2)
    for index in range(4):
        eps = e[index]
        with open('results/eps_{}'.format(eps) + res_f, "rb") as f:
            opinions_dynamics = pickle.load(f)
        opinions_list = list(opinions_dynamics.values())
        number_of_time_steps = len(opinions_list[0])
        for opinion_profile in opinions_list:
            axarr[index//2, index % 2].plot(range(number_of_time_steps), opinion_profile, '.-')
            axarr[index//2, index % 2].set_title(r'$\epsilon={}$'.format(eps))
    for ax in axarr.flat:
        ax.set(xlabel='time', ylabel='opinions')
    for ax in axarr.flat:
        ax.label_outer()
    plt.savefig(filename)


nets_and_files = [
    (nx.watts_strogatz_graph(50, 10, 0.3), 'plots/single_ws_50_10_0,3.pdf', 'single_ws_50_10_0,3.pkl'),
    (nx.complete_graph(50), 'plots/single_cg_50.pdf', 'single_cg_50.pkl'),
    (nx.barabasi_albert_graph(50, 4), 'plots/single_ba_50_4.pdf', 'single_ba_50_4.pkl')
]
for net, file, res_f in nets_and_files:
    # simulations(net, res_f)
    plots(file, res_f)
