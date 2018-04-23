import matplotlib.pyplot as plt
import networkx as nx
import matplotlib as mp

from functions import set_random_opinions
from BC import bounded_confidence, select_all


mp.rcParams['font.size'] = 13


e = [0.05, 0.15, 0.25, 0.35]
f, axarr = plt.subplots(2, 2)

for index in range(4):
    eps = e[index]
    network = nx.watts_strogatz_graph(50, 10, 0.3)
    set_random_opinions(network)
    opinions_dynamics = bounded_confidence(network, eps, eps, select_all)
    opinions_list = list(opinions_dynamics.values())
    number_of_time_steps = len(opinions_list[0])
    for opinion_profile in opinions_list:
        axarr[index//2, index % 2].plot(range(number_of_time_steps), opinion_profile, '.-')
        axarr[index//2, index % 2].set_title('confidence level: {}'.format(eps))
for ax in axarr.flat:
    ax.set(xlabel='time', ylabel='opinions')
for ax in axarr.flat:
    ax.label_outer()
plt.savefig('plots/single_ws_50_10_0,3.pdf')
plt.show()