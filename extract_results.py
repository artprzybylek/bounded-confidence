import shelve
import re


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


def read_file_content(file_name):
    simulations = shelve.open(file_name, flag='r')
    num_of_keys = len(simulations)
    num_of_sim = len(simulations['0.04'])
    num_of_agents = len(simulations['0.04']['0'])
    return simulations, num_of_keys, num_of_sim, num_of_agents


def avg_frequencies(results, num_of_keys, num_of_sim, num_of_agents):
    all_occurrences = [[0] * 101 for _ in range(num_of_keys)]
    for index, key in enumerate(results):
        for sim_index in range(num_of_sim):
            simulation = results[key][str(sim_index)]
            final_opinions = _latest_opinions(simulation)
            _add_opinions_occurrences(final_opinions, all_occurrences, index)
    return [[x/(num_of_agents*num_of_sim) for x in inner_list] for inner_list in all_occurrences]


def main():
    file = 'simulations/simulations_barabasi_albert_graph(625,4)_1.db'
    base_name = re.sub('simulations/simulations_', 'results/', file)
    base_name = re.sub('.db', '_', base_name)
    simulations, num_of_keys, num_of_sim, num_of_agents = read_file_content(file)

    simulations.close()

