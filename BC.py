import networkx as nx
import matplotlib.pyplot as plt
import random


def bounded_confidence_simultaneous(network, eps_left, eps_right, select_neighbors, opinion_dependent=False, m=0.1):
    eps = eps_left + eps_right
    agent_opinions = nx.get_node_attributes(network, 'opinion')
    changed = True
    opinions_in_time = {agent: [agent_opinions[agent]] for agent in agent_opinions}
    while changed:
        changed = False
        new_opinions = {}
        for agent in opinions_in_time:
            self_opinion = opinions_in_time[agent][-1]
            neighbors_panel = select_neighbors(agent, network)
            considered_opinions = [self_opinion]
            if opinion_dependent:
                beta_r = m*self_opinion + (1-m)/2
                beta_l = 1 - beta_r
                eps_right = beta_r*eps
                eps_left = beta_l*eps
            for neighbor in neighbors_panel:
                neighbor_opinion = opinions_in_time[neighbor][-1]
                if -eps_left <= neighbor_opinion - self_opinion <= eps_right:
                    considered_opinions.append(neighbor_opinion)
            new_opinions[agent] = sum(considered_opinions) / len(considered_opinions)
        for agent in new_opinions:
            if abs(new_opinions[agent] - opinions_in_time[agent][-1]) > 0.001:
                changed = True
                break
        for agent in new_opinions:
            opinions_in_time[agent].append(new_opinions[agent])
    return opinions_in_time


def bounded_confidence(network, eps_left, eps_right, select_neighbors, opinion_dependent=False, m=0.1):
    number_of_agents = len(network.nodes())
    agent_opinions = nx.get_node_attributes(network, 'opinion')
    opinions_in_time = {agent: [agent_opinions[agent]] for agent in agent_opinions}
    while True:
        _simulate_one_time_step(number_of_agents, network, eps_left, eps_right, agent_opinions, select_neighbors,
                                opinion_dependent, m)
        if _are_opinions_changed(agent_opinions, opinions_in_time):
            _save_current_opinions(agent_opinions, opinions_in_time)
        else:
            break
    return opinions_in_time


def select_all(agent, network):
    return network.neighbors(agent)


def _simulate_one_time_step(number_of_agents, network, eps_left, eps_right, agent_opinions, select_neighbors,
                            opinion_dependent, m):
    for _ in range(number_of_agents):
        agent = random.randrange(number_of_agents)
        _change_agent_opinion(agent, network, eps_left, eps_right, agent_opinions, select_neighbors,
                              opinion_dependent, m)


def _eps_for_opinion_dependent_case(eps, agent_opinion, m):
    beta_r = m * agent_opinion + (1 - m) / 2
    beta_l = 1 - beta_r
    eps_right = beta_r * eps
    eps_left = beta_l * eps
    return eps_left, eps_right


def _change_agent_opinion(agent, network, eps_left, eps_right, agent_opinions, select_neighbors, opinion_dependent, m):
    self_opinion = agent_opinions[agent]
    neighbors_panel = select_neighbors(agent, network)
    if opinion_dependent:
        eps_left, eps_right = _eps_for_opinion_dependent_case(eps_left + eps_right, self_opinion, m)
    considered_opinions = _influential_opinions(self_opinion, agent_opinions, neighbors_panel, eps_left,
                                                         eps_right)
    agent_opinions[agent] = sum(considered_opinions) / len(considered_opinions)


def _influential_opinions(self_opinion, agent_opinions, neighbors_panel, eps_left, eps_right):
    considered_opinions = [self_opinion]
    for neighbor in neighbors_panel:
        neighbor_opinion = agent_opinions[neighbor]
        if -eps_left <= neighbor_opinion - self_opinion <= eps_right:
            considered_opinions.append(neighbor_opinion)
    return considered_opinions


def _are_opinions_changed(agent_opinions, opinions_in_time):
    for agent in agent_opinions:
        if abs(agent_opinions[agent] - opinions_in_time[agent][-1]) > 0.001:
            return True
    return False


def _save_current_opinions(agent_opinions, opinions_in_time):
    for agent in agent_opinions:
        opinions_in_time[agent].append(agent_opinions[agent])


def main():
    number_of_agents = 50
    eps = 0.05
    g = nx.complete_graph(number_of_agents)
    opinions = dict((x, x/(number_of_agents - 1)) for x in range(number_of_agents))
    nx.set_node_attributes(g, 'opinion', opinions)
    opinions_dynamics = bounded_confidence(g, eps, eps, select_all)
    opinions_list = list(opinions_dynamics.values())
    number_of_time_steps = len(opinions_list[0])
    plt.figure()
    for opinion_profile in opinions_list:
        plt.plot(range(number_of_time_steps), opinion_profile, '.-')

    plt.figure()
    for index in range(9):
        opinions_dynamics = bounded_confidence(g, eps, eps, select_all)
        opinions_list = list(opinions_dynamics.values())
        number_of_time_steps = len(opinions_list[0])
        for opinion_profile in opinions_list:
            plt.subplot(331+index)
            plt.plot(range(number_of_time_steps), opinion_profile, '.-')
    plt.show()


if __name__ == "__main__":
    main()