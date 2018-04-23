import networkx as nx


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
