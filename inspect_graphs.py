import sys
from graph_generator import (
    sparse_random_graph,
    dense_random_graph,
    even_tarjan,
    diamond,
    star_of_stars,
    bipartite_graph,
    count_edges
)

def check_graphs():
    N_VALUES = [200, 1000]
    print(f"{'Type':<15} | {'Target N':<8} | {'Actual N':<8} | {'Edges':<8} | {'Avg Degree':<10} | {'Connected?':<10}")
    print("-" * 80)

    for n in N_VALUES:
        g = sparse_random_graph(n, m=n, cap=50, seed=42)
        connected = is_connected(g, 0, n-1)
        print(f"{'Sparse':<15} | {n:<8} | {g.n:<8} | {count_edges(g):<8} | {count_edges(g)/g.n:<10.2f} | {connected!s:<10}")

    for n in N_VALUES:
        g = dense_random_graph(n, 0.05, cap=50, seed=42)
        connected = is_connected(g, 0, n-1)
        print(f"{'Dense05':<15} | {n:<8} | {g.n:<8} | {count_edges(g):<8} | {count_edges(g)/g.n:<10.2f} | {connected!s:<10}")

    for n in N_VALUES:
        layers = 10
        width = max(5, n // layers)
        g = even_tarjan(layers, width, cap=50)
        connected = is_connected(g, 0, g.n-1)
        print(f"{'EvenTarjan':<15} | {n:<8} | {g.n:<8} | {count_edges(g):<8} | {count_edges(g)/g.n:<10.2f} | {connected!s:<10}")

    for n in N_VALUES:
        diamonds = max(1, (n - 2) // 2)
        g = diamond(diamonds, cap=50)
        connected = is_connected(g, 0, g.n-1)
        print(f"{'Diamond':<15} | {n:<8} | {g.n:<8} | {count_edges(g):<8} | {count_edges(g)/g.n:<10.2f} | {connected!s:<10}")

    for n in N_VALUES:
        k = int(n**0.5)
        g = star_of_stars(k, k, cap=50)
        connected = is_connected(g, 0, g.n-1)
        print(f"{'StarOfStars':<15} | {n:<8} | {g.n:<8} | {count_edges(g):<8} | {count_edges(g)/g.n:<10.2f} | {connected!s:<10}")

def is_connected(g, s, t):
    visited = {s}
    queue = [s]
    while queue:
        u = queue.pop(0)
        if u == t:
            return True
        for v in g.adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)
    return False

if __name__ == "__main__":
    check_graphs()
