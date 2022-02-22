import networkx as nx
import dwave_networkx as dnx

import matplotlib.pyplot as plt

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
my_sampler = EmbeddingComposite(DWaveSampler())

G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (6, 7)])

S = dnx.maximum_independent_set(G, sampler=my_sampler, num_reads=10)

print(' Maximum independent set size found is', len(S))
print(S)

## visualization

k = G.subgraph(S)
notS = list(set(G.nodes()) - set(S))
othersubgraph = G.subgraph(notS)
pos = nx.spring_layout(G)
plt.figure()

nx.draw(G, pos=pos, with_labels=True)
nx.draw(k, pos=pos, with_labels=True)
nx.draw(othersubgraph, pos=pos, node_color='b', with_labels=True)
plt.show()
