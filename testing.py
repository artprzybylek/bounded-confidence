import random
import time
import pickle
import networkx as nx
import numpy as np
from BC import bounded_confidence, select_all


RESULTS_PATH = "C:/studia/python/praca_magisterska/results/"


def _latest_opinions(opinions_in_time):
    return [opinion_profile[-1] for opinion_profile in opinions_in_time.values()]


def _final_groups(opinions, eps_left, eps_right):
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


def _add_opinions_occurrences(opinions, all_occurrences, index):
    for op in opinions:
        all_occurrences[index][round(100 * op)] += 1


def _add_number_of_final_groups(all_final_groups, eps, number_of_final_groups):
    all_final_groups[eps].append(number_of_final_groups)


def _append_to_dict_results(dictionary, key, new_result):
    dictionary[key].append(new_result)


def _avg_freq(all_occurrences, number_of_agents, num_of_simulations):
    return [[x/(number_of_agents*num_of_simulations) for x in inner_list] for inner_list in all_occurrences]


def _save_all_results(files_and_results):
    for file_name in files_and_results:
        with open(RESULTS_PATH+file_name, "bw") as fh:
            res = files_and_results[file_name]
            pickle.dump(res, fh)


def _num_of_steps(opinions_dynamics):
    return len(opinions_dynamics[0])


def _simulate(num_of_simulations, number_of_agents, network, eps_left, eps_right, all_occurrences,
              all_final_groups, all_simulation_steps, index, opinion_dependent=False, m=0.1):
    for _ in range(num_of_simulations):
        opinions = dict((x, random.random()) for x in range(number_of_agents))
        nx.set_node_attributes(network, 'opinion', opinions)
        opinions_dynamics = bounded_confidence(network, eps_left, eps_right, select_all, opinion_dependent, m)
        steps = _num_of_steps(opinions_dynamics)
        final_opinions = _latest_opinions(opinions_dynamics)
        _add_opinions_occurrences(final_opinions, all_occurrences, index)
        if opinion_dependent:
            key = m
        else:
            key = eps_right
        _append_to_dict_results(all_final_groups, key, _final_groups(final_opinions, eps_left, eps_right))
        _append_to_dict_results(all_simulation_steps, key, steps)


def simulate_changing_eps(network, e=np.arange(0.01, 0.41, 0.01), num_of_simulations=50, coeff=1):
    number_of_agents = nx.number_of_nodes(network)
    all_occurrences = [[0] * 101 for _ in range(len(e))]
    all_final_groups = {eps: [] for eps in e}
    all_simulation_steps = {eps: [] for eps in e}
    t0 = time.time()
    for index, eps_right in enumerate(e):
        eps_left = coeff * eps_right
        print(eps_right)
        _simulate(num_of_simulations, number_of_agents, network, eps_left, eps_right, all_occurrences,
                  all_final_groups, all_simulation_steps, index)
    avg_frequencies = _avg_freq(all_occurrences, number_of_agents, num_of_simulations)

    avg_freq_name = str(network) + '_avg_freq_' + str(coeff) + '.pkl'
    final_groups_name = str(network) + '_final_groups_' + str(coeff) + '.pkl'
    steps_name = str(network) + '_steps_' + str(coeff) + '.pkl'
    files_and_results = {avg_freq_name: avg_frequencies,
                         final_groups_name: all_final_groups,
                         steps_name: all_simulation_steps}
    _save_all_results(files_and_results)
    t1 = time.time()
    print(t1-t0)


def simulate_changing_m(network, eps, m_values=np.arange(0, 1, 0.04), num_of_simulations=50):
    eps_left = eps / 2
    eps_right = eps_left
    number_of_agents = nx.number_of_nodes(network)
    all_occurrences = [[0] * 101 for _ in range(len(m_values))]
    all_final_groups = {m: [] for m in m_values}
    all_simulation_steps = {m: [] for m in m_values}
    t0 = time.time()
    for index, m in enumerate(m_values):
        print(m)
        _simulate(num_of_simulations, number_of_agents, network, eps_left, eps_right, all_occurrences,
                  all_final_groups, all_simulation_steps, index, opinion_dependent=True, m=m)
    avg_frequencies = _avg_freq(all_occurrences, number_of_agents, num_of_simulations)

    avg_freq_name = 'op_dep_' + str(network) + '_avg_freq_' + '.pkl'
    final_groups_name = 'op_dep_' + str(network) + '_final_groups_' + '.pkl'
    steps_name = 'op_dep_' + str(network) + '_steps_' + '.pkl'
    files_and_results = {avg_freq_name: avg_frequencies,
                         final_groups_name: all_final_groups,
                         steps_name: all_simulation_steps}
    _save_all_results(files_and_results)
    t1 = time.time()
    print(t1-t0)


if __name__ == "__main__":
    simulate_changing_m(nx.barabasi_albert_graph(625, 4), 0.2)
