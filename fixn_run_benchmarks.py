import pickle
import csv
import time
from graphy import Graph
from ford_fulkerson import ford_fulkerson
from dinic import Dinic
from push_relabel import push_relabel

def dict_to_graph(graph_dict):
    """Convert dictionary format to Graph object."""
    n = len(graph_dict)
    g = Graph(n)
    for u in graph_dict:
        for v, cap in graph_dict[u].items():
            g.add_edge(u, v, cap)
    return g

def dict_to_dinic(graph_dict):
    """Convert dictionary format to Dinic object."""
    n = len(graph_dict)
    d = Dinic(n)
    for u in graph_dict:
        for v, cap in graph_dict[u].items():
            d.add_edge(u, v, cap)
    return d

def run_algorithm(algo_name, graph_dict, source, sink):
    """Run a specific algorithm and return execution time and max flow value."""
    start_time = time.time()
    
    if algo_name == "Ford-Fulkerson":
        g = dict_to_graph(graph_dict)
        max_flow_value, _ = ford_fulkerson(g, source, sink)
    elif algo_name == "Dinic":
        d = dict_to_dinic(graph_dict)
        max_flow_value = d.max_flow(source, sink)
    elif algo_name == "Push-Relabel":
        g = dict_to_graph(graph_dict)
        max_flow_value = push_relabel(g, source, sink)
    else:
        raise ValueError(f"Unknown algorithm: {algo_name}")
    
    end_time = time.time()
    runtime = end_time - start_time
    
    return runtime, max_flow_value

def run_all_benchmarks():
    """Load test cases and run all benchmarks."""
    
    # Load test cases
    testcases_file = 'density_testcases.pkl'
    print(f"Loading test cases from {testcases_file}...")
    
    try:
        with open(testcases_file, 'rb') as f:
            all_testcases = pickle.load(f)
    except FileNotFoundError:
        print(f"ERROR: {testcases_file} not found!")
        print("Please run fixn_generate_testcases.py first.")
        return
    
    print(f"Loaded {len(all_testcases)} test cases")
    
    algorithms = ['Ford-Fulkerson', 'Dinic', 'Push-Relabel']
    
    # CSV file setup
    csv_filename = 'density_benchmark_results.csv'
    
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['graph_type', 'n', 'density', 'test_case', 'algorithm', 'runtime', 'max_flow']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        total_runs = len(all_testcases) * len(algorithms)
        current_run = 0
        
        for testcase in all_testcases:
            graph_type = testcase['graph_type']
            n = testcase['n']
            density = testcase['density']
            test_case_id = testcase['test_case_id']
            graph = testcase['graph']
            source = testcase['source']
            sink = testcase['sink']
            
            print(f"\n{'='*60}")
            print(f"Testing: {graph_type} (n={n}, density={density:.4f}, test_case={test_case_id})")
            print(f"{'='*60}")
            
            # Run each algorithm
            for algo in algorithms:
                current_run += 1
                print(f"[{current_run}/{total_runs}] Running {algo}...", end=' ')
                
                try:
                    runtime, max_flow = run_algorithm(algo, graph, source, sink)
                    print(f"Runtime: {runtime:.4f}s, Max Flow: {max_flow}")
                    
                    # Write to CSV
                    writer.writerow({
                        'graph_type': graph_type,
                        'n': n,
                        'density': density,
                        'test_case': test_case_id,
                        'algorithm': algo,
                        'runtime': runtime,
                        'max_flow': max_flow
                    })
                    csvfile.flush()  # Ensure data is written immediately
                    
                except Exception as e:
                    print(f"ERROR: {str(e)}")
                    writer.writerow({
                        'graph_type': graph_type,
                        'n': n,
                        'density': density,
                        'test_case': test_case_id,
                        'algorithm': algo,
                        'runtime': -1,
                        'max_flow': -1
                    })
                    csvfile.flush()
    
    print(f"\n{'='*60}")
    print(f"Benchmarking complete! Results saved to {csv_filename}")
    print(f"Total runs: {current_run}")
    print(f"{'='*60}")

if __name__ == "__main__":
    run_all_benchmarks()