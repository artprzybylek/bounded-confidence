import networkx as nx
from random import random as rand
import numpy as np


class Lattice2D:

    def __init__(self, n1, n2):
        self.G = nx.Graph()
        for i in range(n1):
            for j in range(n2):
                self.G.add_node(i * n2 + j, pos=(i, j))
        for i in range(n1):
            for j in range(n2):
                if j != 0:
                    self.G.add_edge(i * n2 + j, i * n2 + j - 1)
                if j != n2 - 1:
                    self.G.add_edge(i * n2 + j, i * n2 + j)
                if i != 0:
                    self.G.add_edge(i * n2 + j, i * n2 + j - n2)
                if i != n1 - 1:
                    self.G.add_edge(i * n2 + j, i * n2 + j + n2)


class RandomGraph:

    def __init__(self, N, p):
        self.G = nx.Graph()
        self.G.add_nodes_from(range(N))
        for i in range(N):
            for j in range(i + 1, N):
                x = rand()
                if x < p:
                    self.G.add_edge(i, j)


class WattsStrogatz:

    def __init__(self, N, K, beta):
        self.G = nx.Graph()
        self.G.add_nodes_from(range(N))
        for i in range(N):
            for j in range(i + 1, N):
                if 0 < abs(i - j) % (N - 1 - int( K /2)) <= int( K /2):
                    self.G.add_edge(i, j)
        for edge in self.G.edges():
            x = rand()
            if x < beta:
                i = edge[0]
                j = edge[1]
                self.G.remove_edge(i, j)
                k = round(rand() * (N - 1))
                while k == i or (i, k) in self.G.edges():
                    k = round(rand() * (N - 1))
                self.G.add_edge(i, k)


class BarabasiAlbert:

    def __init__(self, N, m_0, m):
        self.G = nx.Graph()
        self.G.add_nodes_from(range(m_0))
        q = [0] * m_0
        for i in range(m_0-1):
            self.G.add_edge(i, i+1)
            q[i] += 1
            q[i + 1] += 1
        for i in range(m_0, N):
            length = len(self.G.edges())
            self.G.add_node(i)
            vertices = np.random.choice(i, m, replace=False, p=[x / (2*length) for x in q])
            q.append(m)
            for v in vertices:
                self.G.add_edge(v, i)
                q[v] += 1
            length += m
