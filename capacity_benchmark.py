import time
import sys
import pandas as pd
import random
from graph_generator import (
    sparse_random_graph, 
    dense_random_graph, 
    bipartite_graph,
    diamond,
    even_tarjan,
    star_of_stars,
    count_edges
)
from ford_fulkerson import ford_fulkerson
from dinic import Dinic
from push_relabel import push_relabel

sys.setrecursionlimit(30000)

REPEATS = 3
SEEDS = list(range(5))
RESULTS_FILE = "capacity_benchmark_results.csv"

N_VALUES = [200, 400, 600, 800, 1000]
CAPACITY_RANGES = [
    (1, 1),
    (1, 20)
]

def set_random_capacities(graph, cap_range, seed):
    min_c, max_c = cap_range
    rng = random.Random(seed)
    for u in range(graph.n):
        for v in graph.adj[u]:
            if graph.adj[u][v] > 0:
                graph.adj[u][v] = rng.randint(min_c, max_c)

def run_experiment(name, fn, graph, s, t):
    times = []
    flows = []

    for _ in range(REPEATS):
        if name == "Dinic":
            start = time.perf_counter()
            dinic_solver = Dinic(graph.n)
            for u in range(graph.n):
                for v, c in graph.adj[u].items():
                    dinic_solver.add_edge(u, v, c)
            flow = dinic_solver.max_flow(s, t)
            end = time.perf_counter()
        else:
            g_copy = graph.copy()
            start = time.perf_counter()
            res = fn(g_copy, s, t)
            end = time.perf_counter()
            flow = res[0] if isinstance(res, tuple) else res
        
        times.append(end - start)
        flows.append(flow)

    avg_time = sum(times) / len(times)
    avg_flow = sum(flows) / len(flows)
    return avg_time, avg_flow

def run_capacity_benchmark():
    results = []
    
    algorithms = [
        ("Ford-Fulkerson", ford_fulkerson),
        ("Dinic", None),
        ("Push-Relabel", push_relabel),
    ]

    graph_families = [
        ("SparseRandom", lambda n, s: sparse_random_graph(n, m=n*2, seed=s)),
        ("DenseRandom05", lambda n, s: dense_random_graph(n, 0.05, seed=s)),
        ("Bipartite", lambda n, s: bipartite_graph(n//2, n//2)),
        ("Diamond", lambda n, s: diamond(max(1, (n-2)//2))),
        ("EvenTarjan", lambda n, s: even_tarjan(10, max(5, n//10))),
        ("StarOfStars", lambda n, s: star_of_stars(int(n**0.5), int(n**0.5)))
    ]

    print(f"\n=== Running Capacity Scaling Benchmark ===")
    print(f"N Values: {N_VALUES}")
    print(f"Capacity Ranges: {CAPACITY_RANGES}")
    
    total_runs = len(graph_families) * len(N_VALUES) * len(CAPACITY_RANGES) * len(SEEDS) * len(algorithms)
    current_run = 0

    for fam_name, generator in graph_families:
        print(f"\n=== Family: {fam_name} ===")
        for n in N_VALUES:
            for cap_range in CAPACITY_RANGES:
                cap_label = cap_range[1] 
                
                for seed in SEEDS:
                    G = generator(n, seed)
                    s, t = 0, G.n - 1
                    
                    set_random_capacities(G, cap_range, seed)
                    
                    for alg_name, alg_func in algorithms:
                        current_run += 1
                        if current_run % 50 == 0:
                            print(f"Progress: {current_run}/{total_runs} | {fam_name} N={n} CapRange={cap_range}")

                        try:
                            avg_time, avg_flow = run_experiment(alg_name, alg_func, G, s, t)
                            results.append({
                                "GraphType": fam_name,
                                "N": n,
                                "MaxCapacity": cap_label,
                                "Algorithm": alg_name,
                                "Time": avg_time,
                                "Flow": avg_flow,
                                "Seed": seed
                            })
                        except Exception as e:
                            print(f"Error: {e}")

    df = pd.DataFrame(results)
    df.to_csv(RESULTS_FILE, index=False)
    print(f"\nResults saved to {RESULTS_FILE}")

if __name__ == "__main__":
    run_capacity_benchmark()
