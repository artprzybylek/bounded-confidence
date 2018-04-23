import random
import time
import shelve
import networkx as nx
import numpy as np
from BC import bounded_confidence, select_all


def _simulate(num_of_simulations, number_of_agents, network, eps_left, eps_right, results, parent_function,
              opinion_dependent=False, m=0.1):
    if parent_function == simulate_changing_m.__name__:
        key = m
    else:
        key = eps_right
    results[str(key)] = {}
    for sim_index in range(num_of_simulations):
        opinions = dict((x, random.random()) for x in range(number_of_agents))
        nx.set_node_attributes(network, 'opinion', opinions)
        opinions_dynamics = bounded_confidence(network, eps_left, eps_right, select_all, opinion_dependent, m)
        results[str(key)][str(sim_index)] = opinions_dynamics


def simulate_changing_eps(network, e=np.arange(0.01, 0.41, 0.01), num_of_simulations=50, coeff=1):
    number_of_agents = nx.number_of_nodes(network)
    results = shelve.open('simulations/simulations_' + str(network) + '_' + str(coeff) + '.db', writeback=True)
    t0 = time.time()
    for eps_right in e:
        eps_left = coeff * eps_right
        print(eps_right)
        _simulate(num_of_simulations, number_of_agents, network, eps_left, eps_right, results,
                  simulate_changing_eps.__name__)
    results.close()
    t1 = time.time()
    print(t1-t0)


def simulate_changing_m(network, eps, m_values=np.arange(0, 1.01, 0.04), num_of_simulations=50):
    eps_left = eps / 2
    eps_right = eps_left
    number_of_agents = nx.number_of_nodes(network)
    results = shelve.open('simulations/simulations_eps_' + str(eps) + '_' + str(network) + '.db')
    t0 = time.time()
    for m in m_values:
        print(m)
        _simulate(num_of_simulations, number_of_agents, network, eps_left, eps_right, results,
                  simulate_changing_m.__name__, opinion_dependent=True, m=m)
    results.close()
    t1 = time.time()
    print(t1-t0)


if __name__ == "__main__":
    for c in (0.9, 0.7, 0.5, 0.3, 0.1):
        simulate_changing_eps(nx.barabasi_albert_graph(625, 4), coeff=c)
