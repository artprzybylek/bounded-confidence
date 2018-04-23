from random import random as rand
import networkx as nx
import random


def qvoter(g, q, p, steps):
    g_size = nx.number_of_nodes(g)
    op = dict((x, 1) for x in range(g_size))
    for i in range(steps):
        for j in range(g_size):
            spinson = random.randint(0, g_size-1)
            u = rand()
            if u < p:
                if rand() < 0.5:
                    op[spinson] = -op[spinson]
            else:
                neighbors = g.neighbors(spinson)
                if len(neighbors) >= q:
                    qpanel = random.sample(neighbors, q)
                    opinions = [op[x] for x in qpanel]
                    if abs(sum(opinions)) == q and op[spinson] != opinions[0]:
                        op[spinson] = opinions[0]
    m = sum(op.values()) / g_size
    return m
