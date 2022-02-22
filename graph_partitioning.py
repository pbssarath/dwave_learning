"""
Taken from https://github.com/dwave-examples/graph-partitioning/blob/master/graph_partitioning.py
"""

import networkx as nx
from collections import defaultdict
from itertools import combinations
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import math

# ------- Set tunable parameters -------
num_reads = 1000
gamma = 80

# ------- Set up our graph -------
graph_nodes = 10
G = nx.gnp_random_graph(graph_nodes, 0.2)
G = nx.random_geometric_graph(n=graph_nodes, radius=0.5, dim=2)

print("Graph on {} nodes created with {} out of {} possible edges.".format(len(G.nodes), len(G.edges),
                                                                           len(G.nodes) * (len(G.nodes) - 1) / 2))

# ------- Set up our QUBO dictionary -------

# Initialize our Q matrix
Q = defaultdict(int)

# Fill in Q matrix
for u, v in G.edges:
    Q[(u, u)] += 1
    Q[(v, v)] += 1
    Q[(u, v)] += -2

for i in G.nodes:
    Q[(i, i)] += gamma * (1 - len(G.nodes))

for i, j in combinations(G.nodes, 2):
    Q[(i, j)] += 2 * gamma

# ------- Run our QUBO on the QPU -------

# Set chain strength
chain_strength = gamma * len(G.nodes)

# Run the QUBO on the solver from your config file
sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))
response = sampler.sample_qubo(Q, chain_strength=chain_strength, num_reads=num_reads)

# See if the best solution found is feasible, and if so print the number of cut edges.
sample = response.record.sample[0]

# In the case when n is odd, the set may have one more or one fewer nodes
if sum(sample) in [math.floor(len(G.nodes) / 2), math.ceil(len(G.nodes) / 2)]:
    num_cut_edges = 0
    for u, v in G.edges:
        num_cut_edges += sample[u] + sample[v] - 2 * sample[u] * sample[v]
    print("Valid partition found with", num_cut_edges, "cut edges.")
else:
    print("Invalid partition.")
