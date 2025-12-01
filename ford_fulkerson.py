from collections import deque

def ford_fulkerson(graph, s, t):
    n = graph.n
    res = [dict() for _ in range(n)]
    for u in range(n):
        for v, c in graph.adj[u].items():
            res[u][v] = res[u].get(v, 0) + c
            res[v].setdefault(u, res[v].get(u, 0))

    def dfs_find_path():
        stack = [s]
        parent = {s: None}
        while stack:
            u = stack.pop()
            for v, cap in res[u].items():
                if cap > 0 and v not in parent:
                    parent[v] = u
                    if v == t:
                        return parent
                    stack.append(v)
        return None

    max_flow = 0
    while True:
        parent = dfs_find_path()
        if parent is None:
            break
        v = t
        bottleneck = float('inf')
        while parent[v] is not None:
            u = parent[v]
            bottleneck = min(bottleneck, res[u][v])
            v = u
        v = t
        while parent[v] is not None:
            u = parent[v]
            res[u][v] -= bottleneck
            res[v][u] = res[v].get(u, 0) + bottleneck
            v = u
        max_flow += bottleneck

    reachable = {s}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v, cap in res[u].items():
            if cap > 0 and v not in reachable:
                reachable.add(v)
                queue.append(v)
    
    min_cut_edges = []
    for u in range(n):
        if u in reachable:
            for v, cap in graph.adj[u].items():
                if v not in reachable:
                    min_cut_edges.append((u, v))

    return max_flow, min_cut_edges
