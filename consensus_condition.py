import networkx as nx
from itertools import combinations
import random


def is_condition_satisfied(network, eps):
    remove_not_confident_edges(network, eps)
    n = nx.number_of_nodes(network)
    min_common_neighbours = n/2 - 2
    pairs = combinations(range(n), 2)
    for agent1, agent2 in pairs:
        if num_of_common_neighbors(network, agent1, agent2) < min_common_neighbours:
            return False
    return True


def num_of_common_neighbors(network, agent1, agent2):
    neighbors1 = set(nx.neighbors(network, agent1))
    neighbors2 = set(nx.neighbors(network, agent2))
    return len(neighbors1.intersection(neighbors2))


def remove_not_confident_edges(network, eps):
    connections = nx.edges(network)
    connections_copy = list(connections)
    for agent1, agent2 in connections_copy:
        if abs(network.node[agent1]['opinion'] - network.node[agent2]['opinion']) >= eps:
            network.remove_edge(agent1, agent2)


def setup_network(create_func, n, *args, **kwargs):
    network = create_func(n, *args, **kwargs)
    opinions = dict((x, random.random()) for x in range(n))
    nx.set_node_attributes(network, name='opinion', values=opinions)
    return network


def main():
    n = 200
    eps = 1
    for _ in range(10):
        network = setup_network(nx.watts_strogatz_graph, n, k=round(0.78*n), p=0.2)
        print(is_condition_satisfied(network, eps))


if __name__ == '__main__':
    main()
