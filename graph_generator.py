from graphy import Graph

def _lcg(state):
    a = 1664525
    c = 1013904223
    return (a * state + c) % (2**32)

def complete_graph(n, cap=1):
    g = Graph(n)
    for u in range(n):
        for v in range(n):
            if u != v:
                g.add_edge(u, v, cap)
    return g

def chain_graph(n, cap=1):
    g = Graph(n)
    for u in range(n - 1):
        g.add_edge(u, u + 1, cap)
    return g

def layered_graph(n_layers, layer_width, cap=1):
    n = n_layers * layer_width + 2
    s, t = 0, n - 1
    g = Graph(n)
    for i in range(layer_width):
        g.add_edge(s, 1 + i, cap)
    for L in range(n_layers - 1):
        base_u = 1 + L * layer_width
        base_v = 1 + (L + 1) * layer_width
        for i in range(layer_width):
            for j in range(layer_width):
                g.add_edge(base_u + i, base_v + j, cap)
    base = 1 + (n_layers - 1) * layer_width
    for i in range(layer_width):
        g.add_edge(base + i, t, cap)
    return g

def sparse_random_graph(n, m, cap=10, seed=42):
    g = Graph(n)
    edges = set()
    state = seed
    attempts = 0
    while len(edges) < m and attempts < 10 * m:
        state = _lcg(state)
        u = state % n
        state = _lcg(state)
        v = state % n
        if u != v:
            edges.add((u, v))
        attempts += 1
    for (u, v) in edges:
        state = _lcg(state)
        g.add_edge(u, v, 1 + (state % cap))
    return g

def dense_random_graph(n, density, cap=10, seed=42):
    g = Graph(n)
    state = seed
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            state = _lcg(state)
            if (state / 4294967296.0) < density:
                state = _lcg(state)
                g.add_edge(u, v, 1 + (state % cap))
    return g

def bipartite_graph(n_left, n_right, cap=1):
    n = n_left + n_right + 2
    s, t = 0, n - 1
    g = Graph(n)
    for i in range(n_left):
        g.add_edge(s, 1 + i, cap)
    for i in range(n_left):
        u = 1 + i
        for j in range(n_right):
            v = 1 + n_left + j
            g.add_edge(u, v, cap)
    base = 1 + n_left
    for j in range(n_right):
        g.add_edge(base + j, t, cap)
    return g

def even_tarjan(n_layers, width, cap=1):
    from random import seed, random
    seed(123)
    n = n_layers * width + 2
    s, t = 0, n - 1
    g = Graph(n)
    for L in range(n_layers - 1):
        base_u = 1 + L * width
        base_v = 1 + (L + 1) * width
        for i in range(width):
            for j in range(width):
                g.add_edge(base_u + i, base_v + j, cap)
    for i in range(width):
        g.add_edge(s, 1 + i, cap)
    base = 1 + (n_layers - 1) * width
    for i in range(width):
        g.add_edge(base + i, t, cap)
    for L in range(1, n_layers):
        u_base = 1 + L * width
        for i in range(width):
            u = u_base + i
            for prev_L in range(L):
                v_base = 1 + prev_L * width
                for j in range(width):
                    if random() < 0.5:
                        v = v_base + j
                        g.add_edge(u, v, cap)
    return g

def diamond(n_diamonds, cap=1):
    n = 2 * n_diamonds + 2
    s, t = 0, n - 1
    g = Graph(n)
    for i in range(n_diamonds):
        u = 1 + 2 * i
        v = u + 1
        if i == 0:
            g.add_edge(s, u, cap)
        else:
            g.add_edge(u - 2, u, cap)
        g.add_edge(u, v, 1)
        g.add_edge(u, v, cap)
    g.add_edge(2 * n_diamonds, t, cap)
    return g

def star_of_stars(n_branches=50, branch_size=50, cap=1):
    total_nodes = 2 + n_branches * (1 + branch_size)
    s, t = 0, total_nodes - 1
    g = Graph(total_nodes)
    node_id = 1
    for b in range(n_branches):
        hub = node_id
        node_id += 1
        g.add_edge(s, hub, cap)
        for i in range(branch_size):
            leaf = node_id
            node_id += 1
            g.add_edge(hub, leaf, cap)
            g.add_edge(leaf, t, cap)
    return g

def count_edges(g: Graph):
    return sum(len(g.adj[u]) for u in range(g.n))
