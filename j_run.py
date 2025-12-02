import pickle
import csv
import time
import os
from graphy import Graph
from ford_fulkerson import ford_fulkerson
from dinic import Dinic
from push_relabel import push_relabel, push_relabel_min_cut


def dict_to_graph(graph_dict):
    n = len(graph_dict)
    g = Graph(n)
    for u in graph_dict:
        for v, cap in graph_dict[u].items():
            g.add_edge(u, v, cap)
    return g


def dict_to_dinic(graph_dict):
    n = len(graph_dict)
    d = Dinic(n)
    for u in graph_dict:
        for v, cap in graph_dict[u].items():
            d.add_edge(u, v, cap)
    return d


def run_algorithm(algo_name, graph_dict, source, sink):
    start_time = time.perf_counter()
    
    try:
        if algo_name == "Ford-Fulkerson":
            g = dict_to_graph(graph_dict)
            max_flow_value, cut_edges = ford_fulkerson(g, source, sink)
            cut_cap = sum(g.adj[u][v] for (u, v) in cut_edges)
        elif algo_name == "Dinic":
            # Use max_flow_min_cut to also extract cut
            d = dict_to_dinic(graph_dict)
            # Build original graph for accurate capacities
            g = dict_to_graph(graph_dict)
            max_flow_value, cut_edges = d.max_flow_min_cut(source, sink, original_graph=g)
            cut_cap = sum(g.adj[u][v] for (u, v) in cut_edges)
        elif algo_name == "Push-Relabel":
            g = dict_to_graph(graph_dict)
            # Use wrapper returning both flow and cut
            max_flow_value, cut_edges = push_relabel_min_cut(g, source, sink)
            cut_cap = sum(g.adj[u][v] for (u, v) in cut_edges)
        else:
            raise ValueError(f"Unknown algorithm: {algo_name}")
        
        end_time = time.perf_counter()
        runtime_ms = (end_time - start_time) * 1000 
        
        return runtime_ms, max_flow_value, cut_cap, cut_edges, None
    
    except Exception as e:
        return -1, -1, -1, [], str(e)


def run_all_benchmarks():    
    datasets_file = 'j_datasets.pkl'
    print(f"Loading datasets from {datasets_file}...")
    
    try:
        with open(datasets_file, 'rb') as f:
            all_datasets = pickle.load(f)
    except FileNotFoundError:
        print(f"ERROR: {datasets_file} not found!")
        print("Please run j_dtgen.py first.")
        return
    
    print(f"Loaded {len(all_datasets)} test cases")
    
    algorithms = ['Ford-Fulkerson', 'Dinic', 'Push-Relabel']
    
    # Group datasets by plot_id
    datasets_by_plot = {}
    for ds in all_datasets:
        plot_id = ds['plot_id']
        if plot_id not in datasets_by_plot:
            datasets_by_plot[plot_id] = []
        datasets_by_plot[plot_id].append(ds)
    
    print(f"Datasets grouped into {len(datasets_by_plot)} plot categories")
    
    os.makedirs('benchmark_results', exist_ok=True)
    
    total_runs = len(all_datasets) * len(algorithms)
    current_run = 0
    
    for plot_id in sorted(datasets_by_plot.keys()):
        datasets = datasets_by_plot[plot_id]
        csv_filename = f'benchmark_results/{plot_id}_results.csv'
        
        print(f"\n{'='*70}")
        print(f"Processing {plot_id}: {len(datasets)} test cases × {len(algorithms)} algorithms")
        print(f"{'='*70}")
        
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = [
                'algorithm', 'n', 'actual_n', 'density', 'num_layers', 
                'nodes_per_layer', 'grid_k', 'max_capacity', 'runtime_ms', 
                'max_flow', 'min_cut_capacity', 'min_cut_edges', 'trial', 'graph_type', 'error'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # Counters to verify Max-Flow Min-Cut theorem for this plot group
            rows_total = 0
            rows_mismatch = 0
            
            for ds in datasets:
                graph = ds['graph']
                source = ds['source']
                sink = ds['sink']
                
                for algo in algorithms:
                    current_run += 1
                    progress = f"[{current_run}/{total_runs}]"
                    
                    print(f"{progress} {plot_id} | {algo} | n={ds['n']} | trial={ds['trial']}...", end=' ')
                    
                    runtime_ms, max_flow, min_cut_capacity, min_cut_edges, error = run_algorithm(algo, graph, source, sink)
                    
                    if error:
                        print(f"ERROR: {error}")
                    else:
                        print(f"{runtime_ms:.2f} ms")
                    
                    writer.writerow({
                        'algorithm': algo,
                        'n': ds['n'],
                        'actual_n': ds['actual_n'],
                        'density': ds['density'],
                        'num_layers': ds['num_layers'] if ds['num_layers'] is not None else '',
                        'nodes_per_layer': ds['nodes_per_layer'] if ds['nodes_per_layer'] is not None else '',
                        'grid_k': ds['grid_k'] if ds['grid_k'] is not None else '',
                        'max_capacity': ds['max_capacity'],
                        'runtime_ms': runtime_ms,
                        'max_flow': max_flow,
                        'min_cut_capacity': min_cut_capacity,
                        'min_cut_edges': min_cut_edges,
                        'trial': ds['trial'],
                        'graph_type': ds['graph_type'],
                        'error': error if error else ''
                    })
                    csvfile.flush()

                    # Theorem check per row: Flow should equal MinCutCapacity
                    rows_total += 1
                    if not error and max_flow != min_cut_capacity:
                        rows_mismatch += 1
                        # Print a compact warning for visibility
                        print(f" -> Theorem mismatch: flow={max_flow} != min_cut_capacity={min_cut_capacity}")
            # Summary for this plot group
            print(f"Theorem check summary for {plot_id}: total rows {rows_total}, mismatches {rows_mismatch}")
        
        print(f"✓ Saved results to {csv_filename}")
    
    print("\n" + "="*70)
    print("BENCHMARKING COMPLETE!")
    print(f"Results saved in 'benchmark_results/' directory")
    print(f"Total runs: {current_run}")
    print("="*70)


if __name__ == "__main__":
    run_all_benchmarks()
