import time
import sys
import pandas as pd
import pickle
import os
import math

from graph_generator import (
    sparse_random_graph,
    dense_random_graph,
    layered_graph,
    chain_graph,
    complete_graph,
    bipartite_graph,
    even_tarjan,
    diamond,
    star_of_stars,
    count_edges
)

from ford_fulkerson import ford_fulkerson
from dinic import Dinic
from push_relabel import push_relabel, push_relabel_min_cut

sys.setrecursionlimit(30000)

REPEATS = 5
SEEDS = list(range(5))
MAX_N = 1000
DATASET_FILE = "graph_dataset.pkl"
RESULTS_FILE = "advanced_benchmark_results.csv"

N_VALUES = [200, 400, 600, 800, 1000]

def run_experiment(name, fn, graph, s, t):
    times = []
    flows = []
    cut_caps = []
    cut_edges_last = None

    for _ in range(REPEATS):
        if name == "Dinic":
            # Build solver and run max_flow_min_cut using original graph
            dinic_solver = Dinic(graph.n)
            for u in range(graph.n):
                for v, c in graph.adj[u].items():
                    dinic_solver.add_edge(u, v, c)
            start = time.perf_counter()
            flow, cut_edges = dinic_solver.max_flow_min_cut(s, t, original_graph=graph)
            end = time.perf_counter()
        elif name == "Push-Relabel":
            g_copy = graph.copy()
            start = time.perf_counter()
            flow, cut_edges = push_relabel_min_cut(g_copy, s, t)
            end = time.perf_counter()
        else:  # Ford-Fulkerson
            g_copy = graph.copy()
            start = time.perf_counter()
            flow, cut_edges = ford_fulkerson(g_copy, s, t)
            end = time.perf_counter()

        # Compute cut capacity for this run
        cut_cap = sum(graph.adj[u][v] for (u, v) in cut_edges)

        times.append(end - start)
        flows.append(flow)
        cut_caps.append(cut_cap)
        cut_edges_last = cut_edges

    avg_time = sum(times) / len(times)
    avg_flow = sum(flows) / len(flows)
    avg_cut_cap = sum(cut_caps) / len(cut_caps)
    # Return last cut edges for representative listing in CSV
    return avg_time, avg_flow, avg_cut_cap, cut_edges_last

def generate_new_dataset():
    dataset = []
    
    print("\n=== Generating New Dataset ===")

    for n in N_VALUES:
        for seed in SEEDS:
            G = sparse_random_graph(n, m=n, cap=50, seed=seed)
            s, t = 0, n - 1
            dataset.append({
                "type": "Sparse", "n": n, "seed": seed, "graph": G, "s": s, "t": t
            })

    for n in N_VALUES:
        for seed in SEEDS:
            G = dense_random_graph(n, 0.05, cap=50, seed=seed)
            s, t = 0, n - 1
            dataset.append({
                "type": "Dense05", "n": n, "seed": seed, "graph": G, "s": s, "t": t
            })

    for n in N_VALUES:
        left = right = n // 2
        G = bipartite_graph(left, right, cap=50)
        s, t = 0, G.n - 1
        dataset.append({
            "type": "Bipartite", "n": G.n, "seed": -1, "graph": G, "s": s, "t": t
        })

    for n in N_VALUES:
        layers = 10
        width = max(5, n // layers)
        G = even_tarjan(layers, width, cap=50)
        s, t = 0, G.n - 1
        dataset.append({
            "type": "EvenTarjan", "n": G.n, "seed": -1, "graph": G, "s": s, "t": t
        })

    for n in N_VALUES:
        diamonds = max(1, (n - 2) // 2)
        G = diamond(diamonds, cap=50)
        s, t = 0, G.n - 1
        dataset.append({
            "type": "Diamond", "n": G.n, "seed": -1, "graph": G, "s": s, "t": t
        })

    for n in N_VALUES:
        k = int(n**0.5)
        branches = k
        branch_size = k
        G = star_of_stars(branches, branch_size, cap=50)
        s, t = 0, G.n - 1
        dataset.append({
            "type": "StarOfStars", "n": G.n, "seed": -1, "graph": G, "s": s, "t": t
        })

    print(f"  Generation Complete. {len(dataset)} graph instances created.")
    return dataset

def run_benchmark_on_dataset(dataset):
    results = []
    
    algorithms = [
        ("Ford-Fulkerson", ford_fulkerson),
        ("Dinic", None),
        ("Push-Relabel", push_relabel_min_cut),
    ]

    total_items = len(dataset)
    print(f"\n=== Running Benchmarks on {total_items} Graphs ===")

    for i, item in enumerate(dataset):
        g_type = item['type']
        n = item['n']
        seed = item['seed']
        G = item['graph']
        s = item['s']
        t = item['t']
        
        M = count_edges(G)

        print(f"[{i+1}/{total_items}] Processing {g_type} (N={n}, Seed={seed})...")

        if G.n < 2:
            continue

        for alg_name, alg_func in algorithms:
            try:
                avg_time, avg_flow, avg_cut_cap, cut_edges = run_experiment(alg_name, alg_func, G, s, t)
                results.append({
                    "GraphType": g_type,
                    "N": n,
                    "M": M,
                    "Algorithm": alg_name,
                    "Time": avg_time,
                    "Flow": avg_flow,
                    "MinCutCapacity": avg_cut_cap,
                    "MinCutEdges": cut_edges,
                    "Seed": seed
                })
            except Exception as e:
                print(f"  Error running {alg_name} on {g_type} N={n}: {e}")

    return results

def save_results(results, filename=RESULTS_FILE):
    if not results:
        print("No results to save.")
        return
        
    df = pd.DataFrame(results)
    cols = ["GraphType", "Algorithm", "N", "M", "Seed", "Time", "Flow", "MinCutCapacity", "MinCutEdges"]
    for c in df.columns:
        if c not in cols:
            cols.append(c)
    
    df = df[cols]
    df.to_csv(filename, index=False)
    print(f"\nResults saved to {filename}")

def main():
    dataset = None
    
    if os.path.exists(DATASET_FILE):
        print(f"Found existing dataset: {DATASET_FILE}")
        choice = input("Do you want to use the existing dataset? (y/n): ").strip().lower()
        if choice == 'y':
            print("Loading dataset...")
            with open(DATASET_FILE, 'rb') as f:
                dataset = pickle.load(f)
            print("Dataset loaded.")
    
    if dataset is None:
        print("Generating new dataset...")
        dataset = generate_new_dataset()
        
        save_choice = input("Do you want to save this new dataset for future use? (y/n): ").strip().lower()
        if save_choice == 'y':
            with open(DATASET_FILE, 'wb') as f:
                pickle.dump(dataset, f)
            print(f"Dataset saved to {DATASET_FILE}")

    results = run_benchmark_on_dataset(dataset)
    
    save_results(results)

    # === Empirical max-flow min-cut theorem check ===
    try:
        df = pd.DataFrame(results)
        mismatches = df[df["Flow"] != df["MinCutCapacity"]]
        print("\n=== Max-Flow Min-Cut Verification ===")
        print(f"Total result rows: {len(df)}")
        print(f"Rows with Flow != MinCutCapacity: {len(mismatches)}")
        if not mismatches.empty:
            print("First mismatch examples:")
            print(mismatches.head()[["GraphType","Algorithm","Flow","MinCutCapacity","MinCutEdges"]])
        else:
            print("All rows satisfy Flow == MinCutCapacity.")
        # Optional: sample display
        print("\nSample rows:")
        print(df.head()[["GraphType","Algorithm","Flow","MinCutCapacity","MinCutEdges"]])
    except Exception as e:
        print(f"Verification step failed: {e}")
    # === End verification ===

    print("\nBenchmark complete.")
    
    if not os.path.exists(DATASET_FILE):
        save_final = input("Do you want to save the dataset now? (y/n): ").strip().lower()
        if save_final == 'y':
            with open(DATASET_FILE, 'wb') as f:
                pickle.dump(dataset, f)
            print(f"Dataset saved to {DATASET_FILE}")
    else:
        overwrite = input("Do you want to overwrite/update the saved dataset file? (y/n): ").strip().lower()
        if overwrite == 'y':
            with open(DATASET_FILE, 'wb') as f:
                pickle.dump(dataset, f)
            print(f"Dataset overwritten to {DATASET_FILE}")

if __name__ == "__main__":
    main()
