from collections import defaultdict, deque

class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = [dict() for _ in range(n)]

    def add_edge(self, u, v, cap):
        if cap <= 0:
            return
        self.adj[u][v] = self.adj[u].get(v, 0) + cap

    def neighbors(self, u):
        return list(self.adj[u].keys())

    def capacity(self, u, v):
        return self.adj[u].get(v, 0)

    def copy(self):
        g = Graph(self.n)
        for u in range(self.n):
            for v, c in self.adj[u].items():
                g.adj[u][v] = c
        return g

def compute_min_cut_from_residual(graph, residual_adj, s):
    """
    Given the original graph and a residual adjacency (dict-of-dicts) after a
    max-flow computation, return the minimum cut edges as a list of (u, v)
    where u is reachable from s in the residual graph and v is not.

    Inputs:
    - graph: Graph (original capacities)
    - residual_adj: list[dict[int,int]] (residual capacities)
    - s: int (source)

    Output:
    - list of edges (u, v) forming an s-t cut
    """
    from collections import deque

    n = graph.n
    reachable = {s}
    q = deque([s])
    while q:
        u = q.popleft()
        for v, cap in residual_adj[u].items():
            if cap > 0 and v not in reachable:
                reachable.add(v)
                q.append(v)

    cut = []
    for u in range(n):
        if u in reachable:
            for v, cap in graph.adj[u].items():
                if v not in reachable:
                    cut.append((u, v))
    return cut
