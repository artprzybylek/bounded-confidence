import networkx as nx
import numpy as np
import pickle
import time

from BC import bounded_confidence, select_all
from functions import latest_opinions, set_random_opinions


CONSENSUS_RATE = 0.8


def find_clusters(network, final_opinions, eps_left, eps_right):
    connections = list(nx.edges(network))
    for agent1, agent2 in connections:
        if abs(final_opinions[agent1] - final_opinions[agent2]) >= max([eps_left, eps_right]):
            network.remove_edge(agent1, agent2)
    return list(subgraph.nodes() for subgraph in nx.connected_component_subgraphs(network))


def is_consensus_reached(network, final_opinions, eps_left, eps_right):
    for cluster in find_clusters(network, final_opinions, eps_left, eps_right):
        num_of_agents = nx.number_of_nodes(network)
        if len(cluster) > CONSENSUS_RATE * num_of_agents:
            return True
    return False


def consensus_frequency(network_type, eps, num_of_agents, n=100, *args, **kwargs):
    num_of_consensuses = 0
    for _ in range(n):
        if network_type == 'ba':
            network = nx.barabasi_albert_graph(num_of_agents, *args, **kwargs)
        elif network_type == 'ws':
            network = nx.watts_strogatz_graph(num_of_agents, *args, **kwargs)
        else:
            network = nx.complete_graph(num_of_agents)
        set_random_opinions(network)
        opinions_evolution = bounded_confidence(network, eps, eps, select_all)
        final_opinions = latest_opinions(opinions_evolution)
        if is_consensus_reached(network, final_opinions, eps, eps):
            num_of_consensuses += 1
    return num_of_consensuses/n


def save_res(filename, res):
    with open(filename, "bw") as f:
        pickle.dump(res, f)


def main_b():
    num_of_agents = 100
    network_type = 'ba'
    filename = network_type + '_' + str(num_of_agents) + '.pkl'
    m_values = [2, 4, 6, 8, 10]
    confidence_levels = np.arange(0.16, 0.31, 0.01)
    consensuses = {m: {} for m in m_values}
    for m in m_values:
        for eps in confidence_levels:
            print(eps)
            consensuses[m][eps] = consensus_frequency(network_type, eps, num_of_agents, m=m)
    save_res(filename, consensuses)


def main_cg():
    for num_of_agents in [500]:
        network_type = 'cg'
        filename = network_type + '_' + str(num_of_agents) + '.pkl'
        confidence_levels = np.arange(0.16, 0.31, 0.01)
        consensuses = {}
        for eps in confidence_levels:
            print(eps)
            consensuses[eps] = consensus_frequency(network_type, eps, num_of_agents)
        save_res(filename, consensuses)


def main_ws():
    num_of_agents = 200
    network_type = 'ws'
    for p in [0.2]:
        filename = '2_' + network_type + '_' + str(num_of_agents) + '_' + str(p) + '.pkl'
        k_values = [4, 6, 8, 10, 12]
        confidence_levels = np.arange(0.16, 0.31, 0.01)
        consensuses = {k: {} for k in k_values}
        for k in k_values:
            print(k)
            for eps in confidence_levels:
                consensuses[k][eps] = consensus_frequency(network_type, eps, num_of_agents, k=k, p=p)
        save_res(filename, consensuses)


def main_ws_eps():
    num_of_agents = 200
    network_type = 'ws'
    for p in [0.2]:
        confidence_levels = [0.18, 0.2, 0.22, 0.24, 0.26]
        filename = 'eps_' + network_type + '_' + str(num_of_agents) + '_' + str(p) + '.pkl'
        k_values = [4, 6, 8, 10, 12, 14, 16, 18, 20]
        consensuses = {eps: {} for eps in confidence_levels}
        for eps in confidence_levels:
            print(eps)
            for k in k_values:
                consensuses[eps][k] = consensus_frequency(network_type, eps, num_of_agents, k=k, p=p)
        save_res(filename, consensuses)



def main_ws1():
    network_type = 'ws'
    p = 0.2
    k = 50
    filename = network_type + '_' + str(p) + '_' + str(k) + '.pkl'
    nums = [200]
    consensuses = {num_of_agents: {} for num_of_agents in nums}
    for num_of_agents in nums:
        confidence_levels = np.arange(0.16, 0.31, 0.01)
        for eps in confidence_levels:
            print(eps)
            consensuses[num_of_agents][eps] = consensus_frequency(network_type, eps, num_of_agents, k=k, p=p)
    save_res(filename, consensuses)


if __name__ == "__main__":
    t0 = time.time()
    main_ws_eps()
    t1 = time.time()
    print(t1-t0)
