import networkx as nx
import matplotlib.pyplot as plt


plt.figure()

network = nx.complete_graph(20)
nx.draw_circular(network)
plt.savefig('net_cg_20.pdf')

plt.figure()

network = nx.watts_strogatz_graph(20, 4, 0.25)
nx.draw_circular(network)
plt.savefig('net_ws_4_0,25.pdf')

plt.figure()

network = nx.barabasi_albert_graph(20, 2)
nx.draw_circular(network)
plt.savefig('net_ba_20_2.pdf')

plt.show()
