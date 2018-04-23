from BC import bounded_confidence, select_all
import networkx as nx
import matplotlib.pyplot as plt
import random
import time


def _final_groups(agents_opinions, agents_neigbors, eps_left, eps_right):
    final_profiles = {}
    for agent, opinion in enumerate(agents_opinions):
        new_profile = True
        for left, right in final_profiles:
            if left < opinion < right:
                final_profiles[(left, right)].append(agents_neigbors[agent])
                new_profile = False
                break
        if new_profile:
            final_profiles[(opinion - eps_left, opinion + eps_right)] = [agents_neigbors[agent]]
    return final_profiles


def _avg_connection_groups_size(group_size_connections):
    return [sum(group)/len(group) for group in group_size_connections.values()],\
           list(group_size_connections.keys())


def _max_connection_groups_size(group_size_connections):
    return [max(group) for group in group_size_connections.values()], list(group_size_connections.keys())


def _find_clusters(network, final_opinions, eps_right):
    connections = list(nx.edges(network))
    for agent1, agent2 in connections:
        if abs(final_opinions[agent1] - final_opinions[agent2]) >= eps_right:
            network.remove_edge(agent1, agent2)
    return list(subgraph.nodes() for subgraph in nx.connected_component_subgraphs(network))


def main():
    num_of_agents = 100
    eps_left, eps_right = 0.15, 0.15
    all_connections = []
    all_group_size = []
    original_network = nx.barabasi_albert_graph(num_of_agents, 4)
    for i in range(2):
        network = original_network.copy()
        opinions = dict((x, random.random()) for x in range(num_of_agents))
        nx.set_node_attributes(network, name='opinion', values=opinions)
        # agents_neighbors = [len(nx.neighbors(network, agent)) for agent in range(num_of_agents)]
        simulation = bounded_confidence(network, eps_left, eps_right, select_neighbors=select_all)
        print(i)
        final_opinions = [simulation[agent][-1] for agent in range(num_of_agents)]
        clusters = _find_clusters(network, final_opinions, eps_right)
        print(len(clusters), [len(list(cluster)) for cluster in clusters])
        group_size_connections = {}
        """for cluster in clusters:
            if len(cluster) not in group_size_connections:
                group_size_connections[len(cluster)] = [agents_neighbors[agent] for agent in cluster]
            else:
                group_size_connections[len(cluster)] += [agents_neighbors[agent] for agent in cluster]"""

        max_group_connections, group_size = _max_connection_groups_size(group_size_connections)
        all_connections += max_group_connections
        all_group_size += group_size

    """plt.figure()
    plt.plot(all_group_size, all_connections, 'r*')

    plt.figure()
    for agent in simulation:
        plt.plot(simulation[agent])

    plt.figure()
    plt.plot(final_opinions, agents_neighbors, '*')

    plt.show()"""


if __name__ == "__main__":
    main()
