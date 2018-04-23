import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np
import random
from math import sqrt
import seaborn as sns

from BC import noisy_bc
from functions import set_random_opinions


def set_random_gauss_opinions(network, mu, sigma):
    num_of_agents = nx.number_of_nodes(network)
    opinions = {}
    agent = 0
    while agent < num_of_agents:
        opinion = random.gauss(mu, sigma)
        if 0 <= opinion <= 1:
            opinions[agent] = opinion
            agent += 1
    nx.set_node_attributes(network, name='opinion', values=opinions)


def main():
    n = 100
    network = nx.complete_graph(n)
    # set_random_gauss_opinions(network, mu=0.5, sigma=sqrt(1/40))
    set_random_opinions(network)
    R = 0.1
    sigma = 0.05
    time_step = 0.01
    time_limit = 100
    t0 = time.time()
    opinions_evolution = noisy_bc(network, R, sigma, time_limit=time_limit, time_step=time_step)
    t1 = time.time()
    print(t1-t0)
    opinions_list = list(opinions_evolution.values())
    plt.figure()
    for opinion_profile in opinions_list:
        plt.plot(np.arange(0, time_limit+time_step, time_step), opinion_profile, '-')
    plt.show()


def plot_profiles(opinions_list, time_step, num_of_agents):
    num_of_points = len(opinions_list[0])
    time_indexes = range(0, num_of_points, num_of_points//5)
    plt.figure()
    sns.set_style('whitegrid')
    for index in time_indexes:
        print(index)
        opinions = [agent_opinions[index] for agent_opinions in opinions_list]
        # sns.kdeplot(np.array(opinions), bw=0.5)
        plt.plot(opinions, '.')
    plt.show()


def main1():
    n = 50
    network = nx.complete_graph(n)
    set_random_gauss_opinions(network, mu=0.5, sigma=sqrt(1/40))
    R = 0.2
    sigma = 0.1
    time_step = 0.1
    time_limit = 50
    t0 = time.time()
    opinions_evolution = noisy_bc(network, R, sigma, time_limit=time_limit, time_step=time_step)
    t1 = time.time()
    print(t1 - t0)
    opinions_list = list(opinions_evolution.values())
    plot_profiles(opinions_list, time_step, n)


if __name__ == "__main__":
    main()
