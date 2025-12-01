from graphy import Graph
from ford_fulkerson import ford_fulkerson

g = Graph(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 10)
g.add_edge(1, 2, 2)
g.add_edge(1, 3, 4)
g.add_edge(2, 3, 9)

max_flow, min_cut = ford_fulkerson(g, 0, 3)

print(f"Max Flow: {max_flow}")
print(f"Min Cut Edges: {min_cut}")