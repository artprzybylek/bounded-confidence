import random
import time
import pickle
import networkx as nx
import numpy as np

from BC import bounded_confidence, select_all


RESULTS_PATH = "results/"
NETWORKS = {nx.complete_graph: 'cg', nx.barabasi_albert_graph: 'ba', nx.watts_strogatz_graph: 'ws'}


def set_random_opinions(network):
    num_of_agents = nx.number_of_nodes(network)
    opinions = dict((x, random.random()) for x in range(num_of_agents))
    nx.set_node_attributes(network, name='opinion', values=opinions)


def find_clusters(network, final_opinions, eps_right):
    connections = list(nx.edges(network))
    for agent1, agent2 in connections:
        if abs(final_opinions[agent1] - final_opinions[agent2]) >= eps_right:
            network.remove_edge(agent1, agent2)
    return list(subgraph.nodes() for subgraph in nx.connected_component_subgraphs(network))


def clusters10(clusters):
    biggest_size = max(len(cluster) for cluster in clusters)
    return sum(1 for cluster in clusters if len(cluster)>=0.1*biggest_size)


def latest_opinions(opinions_in_time):
    return [opinion_profile[-1] for opinion_profile in opinions_in_time.values()]


def final_groups(opinions, eps_left, eps_right):
    final_profiles = []
    for opinion in opinions:
        new_profile = True
        for left, right in final_profiles:
            if left < opinion < right:
                new_profile = False
                break
        if new_profile:
            final_profiles.append((opinion - eps_left, opinion + eps_right))
    return len(final_profiles)


def opinions_changes_steps(opinions_dynamics):
    return [sum(abs(agent_op[i+1]-agent_op[i]) for agent_op in opinions_dynamics.values()) / len(opinions_dynamics) for
            i in range(len(opinions_dynamics[0]) - 1)]


def add_opinions_occurrences(opinions, all_occurrences, index):
    for op in opinions:
        all_occurrences[index][round(100 * op)] += 1


def add_number_of_final_groups(all_final_groups, eps, number_of_final_groups):
    all_final_groups[eps].append(number_of_final_groups)


def append_to_dict_results(dictionary, key, new_result):
    dictionary[key].append(new_result)


def avg_freq(all_occurrences, number_of_agents, num_of_simulations):
    return [[x/(number_of_agents*num_of_simulations) for x in inner_list] for inner_list in all_occurrences]


def save_all_results(files_and_results):
    for file_name in files_and_results:
        with open(RESULTS_PATH+file_name, "bw") as fh:
            res = files_and_results[file_name]
            pickle.dump(res, fh)


def num_of_steps(opinions_dynamics):
    return len(opinions_dynamics[0])


def opinions_changes(opinions_dynamics):
    return sum(abs(agent_op[0]-agent_op[-1]) for agent_op in opinions_dynamics.values()) / len(opinions_dynamics)


def final_order(num_of_contact_edges, num_of_all_edges):
    return num_of_contact_edges / num_of_all_edges


def simulate(num_of_simulations, number_of_agents, network_func, eps_left, eps_right, all_occurrences,
             all_final_groups, all_simulation_steps, all_opinions_changes, all_final_orders, all_groups10,
             all_steps_changes, index, *args, opinion_dependent=False, m=0.1):
    for _ in range(num_of_simulations):
        network = network_func(number_of_agents, *args)
        num_of_all_edges = network.number_of_edges()
        set_random_opinions(network)
        opinions_dynamics = bounded_confidence(network, eps_left, eps_right, select_all, opinion_dependent, m)
        steps = num_of_steps(opinions_dynamics)
        final_opinions = latest_opinions(opinions_dynamics)
        clusters = find_clusters(network, final_opinions, eps_right)
        num_of_contact_edges = network.number_of_edges()
        add_opinions_occurrences(final_opinions, all_occurrences, index)
        steps_changes = opinions_changes_steps(opinions_dynamics)
        key = eps_right
        # append_to_dict_results(all_groups10, key, clusters10(clusters))
        # append_to_dict_results(all_final_groups, key, len(clusters))
        # append_to_dict_results(all_simulation_steps, key, steps)
        # append_to_dict_results(all_opinions_changes, key, opinions_changes(opinions_dynamics))
        # append_to_dict_results(all_final_orders, key, final_order(num_of_contact_edges, num_of_all_edges))
        append_to_dict_results(all_steps_changes, key, steps_changes)


def simulate_changing_eps(network_func, number_of_agents, *args, e=np.arange(0.01, 0.41, 0.01),
                          num_of_simulations=100):
    all_occurrences = [[0] * 101 for _ in range(len(e))]
    all_final_groups = {eps: [] for eps in e}
    all_simulation_steps = {eps: [] for eps in e}
    all_opinions_changes = {eps: [] for eps in e}
    all_final_orders = {eps: [] for eps in e}
    all_groups10 = {eps: [] for eps in e}
    all_steps_changes = {eps: [] for eps in e}
    t0 = time.time()
    for index, eps_right in enumerate(e):
        eps_left = eps_right
        print(eps_right)
        simulate(num_of_simulations, number_of_agents, network_func, eps_left, eps_right, all_occurrences,
                 all_final_groups, all_simulation_steps, all_opinions_changes, all_final_orders, all_groups10,
                 all_steps_changes, index, *args)
    # avg_frequencies = avg_freq(all_occurrences, number_of_agents, num_of_simulations)

    agents = str(number_of_agents)
    avg_freq_name = '_'.join(['avg_freq', NETWORKS[network_func], agents]+[str(arg) for arg in args]) + '.pkl'
    final_groups_name = '_'.join(['final_groups', NETWORKS[network_func], agents]+[str(arg) for arg in args]) + '.pkl'
    steps_name = '_'.join(['steps', NETWORKS[network_func], agents]+[str(arg) for arg in args]) + '.pkl'
    changes_name = '_'.join(['changes', NETWORKS[network_func], agents]+[str(arg) for arg in args]) + '.pkl'
    order_name = '_'.join(['order', NETWORKS[network_func], agents]+[str(arg) for arg in args]) + '.pkl'
    groups10_name = '_'.join(['groups10', NETWORKS[network_func], agents]+[str(arg) for arg in args]) + '.pkl'
    steps_changes_name = '_'.join(['steps_changes', NETWORKS[network_func], agents]+[str(arg) for arg in args]) + '.pkl'
    files_and_results = {
        # avg_freq_name: avg_frequencies,
        # final_groups_name: all_final_groups,
        # steps_name: all_simulation_steps,
        # changes_name: all_opinions_changes,
        # order_name: all_final_orders,
        # groups10_name: all_groups10
        steps_changes_name: all_steps_changes
    }
    save_all_results(files_and_results)
    t1 = time.time()
    print(t1-t0)


def simulate_changing_m(network, eps, m_values=np.arange(0, 1.01, 0.04), num_of_simulations=50):
    eps_left = eps / 2
    eps_right = eps_left
    number_of_agents = nx.number_of_nodes(network)
    all_occurrences = [[0] * 101 for _ in range(len(m_values))]
    all_final_groups = {m: [] for m in m_values}
    all_simulation_steps = {m: [] for m in m_values}
    t0 = time.time()
    for index, m in enumerate(m_values):
        print(m)
        simulate(num_of_simulations, number_of_agents, network, eps_left, eps_right, all_occurrences,
                 all_final_groups, all_simulation_steps, index, opinion_dependent=True, m=m)
    avg_frequencies = avg_freq(all_occurrences, number_of_agents, num_of_simulations)

    avg_freq_name = 'op_dep_' + str(eps) + '_' + str(network) + '_avg_freq' + '.pkl'
    final_groups_name = 'op_dep_' + str(eps) + '_' + str(network) + '_final_groups' + '.pkl'
    steps_name = 'op_dep_' + str(eps) + '_' + str(network) + '_steps' + '.pkl'
    files_and_results = {avg_freq_name: avg_frequencies,
                         final_groups_name: all_final_groups,
                         steps_name: all_simulation_steps}
    save_all_results(files_and_results)
    t1 = time.time()
    print(t1-t0)


if __name__ == "__main__":
    e = [0.05, 0.15, 0.25, 0.35]

    """simulate_changing_eps(nx.barabasi_albert_graph, 200, 2, e=e)
    print()
    simulate_changing_eps(nx.barabasi_albert_graph, 200, 4, e=e)
    print()
    simulate_changing_eps(nx.barabasi_albert_graph, 200, 6, e=e)
    print()
    simulate_changing_eps(nx.barabasi_albert_graph, 200, 8, e=e)
    print()
    simulate_changing_eps(nx.barabasi_albert_graph, 200, 10, e=e)
    print()

    print('ws1')
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 10, 0.3, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 20, 0.3, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 30, 0.3, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 40, 0.3, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 50, 0.3, e=e)
    print()

    print('ws2')
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 20, 0.1, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 20, 0.2, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 20, 0.4, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 20, 0.5, e=e)
    print()

    print('cg')
    simulate_changing_eps(nx.complete_graph, 500, e=e)
    print()
    simulate_changing_eps(nx.complete_graph, 200, e=e)
    print()
    simulate_changing_eps(nx.complete_graph, 100, e=e)
    print()

    print('extra')
    simulate_changing_eps(nx.barabasi_albert_graph, 100, 6, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 100, 20, 0.3, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 500, 20, 0.3, e=e)
    print()
    simulate_changing_eps(nx.barabasi_albert_graph, 500, 6, e=e)
    print()"""

    print('ws1')
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 4, 0.2, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 6, 0.2, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 8, 0.2, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 10, 0.2, e=e)
    print()
    simulate_changing_eps(nx.watts_strogatz_graph, 200, 12, 0.2, e=e)
    print()

