from collections import deque

class Dinic:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.adj[u].append([v, len(self.adj[v]), c])
        self.adj[v].append([u, len(self.adj[u]) - 1, 0])

    def max_flow(self, s, t):
        flow = 0
        n = self.n
        while True:
            level = [-1] * n
            q = deque([s])
            level[s] = 0
            while q:
                u = q.popleft()
                for v, rev, cap in self.adj[u]:
                    if cap > 0 and level[v] < 0:
                        level[v] = level[u] + 1
                        q.append(v)
            if level[t] < 0:
                return flow
            it = [0] * n

            def dfs(u, f):
                if u == t:
                    return f
                for i in range(it[u], len(self.adj[u])):
                    it[u] = i
                    v, rev, cap = self.adj[u][i]
                    if cap > 0 and level[v] == level[u] + 1:
                        pushed = dfs(v, min(f, cap))
                        if pushed > 0:
                            self.adj[u][i][2] -= pushed
                            self.adj[v][rev][2] += pushed
                            return pushed
                return 0

            while True:
                pushed = dfs(s, float('inf'))
                if pushed == 0:
                    break
                flow += pushed

    def max_flow_min_cut(self, s, t, original_graph=None):
        # Snapshot original capacities to reconstruct cut if not provided
        n = self.n
        if original_graph is None:
            from graphy import Graph
            original_graph = Graph(n)
            for u in range(n):
                for v, rev, cap in self.adj[u]:
                    pass 
        # Run max flow
        flow = self.max_flow(s, t)

        # Build residual adjacency dict-of-dicts from self.adj
        residual = [dict() for _ in range(n)]
        for u in range(n):
            for idx, (v, rev, cap) in enumerate(self.adj[u]):
                residual[u][v] = residual[u].get(v, 0) + cap

        # Compute cut
        from graphy import compute_min_cut_from_residual
        cut = compute_min_cut_from_residual(original_graph, residual, s)
        return flow, cut
