import pickle
import os
from graph_generator import (
    dense_random_graph, 
    sparse_random_graph, 
    layered_graph, 
    bipartite_graph,
    count_edges
)
from graphy import Graph

def calculate_density(n, m):
    """Calculate graph density."""
    max_edges = n * (n - 1)
    return m / max_edges if max_edges > 0 else 0

def graph_to_dict(g):
    """Convert Graph object to dictionary format for algorithms."""
    graph_dict = {}
    for u in range(g.n):
        graph_dict[u] = {}
        for v, cap in g.adj[u].items():
            graph_dict[u][v] = cap
    return graph_dict

def generate_grid_graph(rows, cols, cap=1):
    """Generate a grid graph with source and sink."""
    n = rows * cols
    g = Graph(n + 2)  # +2 for source and sink
    s, t = 0, n + 1
    
    # Connect source to first column
    for i in range(rows):
        g.add_edge(s, 1 + i * cols, cap)
    
    # Grid connections (right and down)
    for i in range(rows):
        for j in range(cols):
            node = 1 + i * cols + j
            # Right
            if j < cols - 1:
                g.add_edge(node, node + 1, cap)
            # Down
            if i < rows - 1:
                g.add_edge(node, node + cols, cap)
    
    # Connect last column to sink
    for i in range(rows):
        g.add_edge(1 + i * cols + (cols - 1), t, cap)
    
    return g, s, t

def generate_all_testcases():
    """Generate all test cases and save them to a file."""
    
    # Parameters
    node_sizes = [50, 250, 1000]
    graph_types = ['random', 'sparse', 'dense', 'layered', 'bipartite', 'grid']
    test_cases_per_config = 10
    
    # Storage for all test cases
    all_testcases = []
    
    total_configs = len(node_sizes) * len(graph_types) * test_cases_per_config
    current_config = 0
    
    for n in node_sizes:
        for graph_type in graph_types:
            print(f"\n{'='*60}")
            print(f"Generating {graph_type} graphs with n={n}")
            print(f"{'='*60}")
            
            for test_case in range(test_cases_per_config):
                current_config += 1
                print(f"[{current_config}/{total_configs}] Test case {test_case + 1}/{test_cases_per_config}")
                
                # Generate graph based on type
                # Use different seeds for each test case
                seed = 42 + test_case * 100
                
                if graph_type == 'random':
                    # Random graph with medium density
                    g = dense_random_graph(n, density=0.3, cap=10, seed=seed)
                    source, sink = 0, n - 1
                elif graph_type == 'sparse':
                    # Sparse graph with ~2n edges
                    m = 2 * n
                    g = sparse_random_graph(n, m, cap=10, seed=seed)
                    source, sink = 0, n - 1
                elif graph_type == 'dense':
                    # Dense graph with high density
                    g = dense_random_graph(n, density=0.7, cap=10, seed=seed)
                    source, sink = 0, n - 1
                elif graph_type == 'layered':
                    # Layered graph
                    g = layered_graph(n_layers=5, layer_width=n // 6, cap=10)
                    source, sink = 0, g.n - 1
                elif graph_type == 'bipartite':
                    # Bipartite graph
                    g = bipartite_graph(n // 2, n // 2, cap=10)
                    source, sink = 0, g.n - 1
                elif graph_type == 'grid':
                    grid_size = int(n ** 0.5)
                    g, source, sink = generate_grid_graph(grid_size, grid_size, cap=10)
                
                # Convert Graph object to dictionary format
                graph = graph_to_dict(g)
                
                # Calculate number of edges and density
                num_edges = count_edges(g)
                actual_n = g.n
                density = calculate_density(actual_n, num_edges)
                
                print(f"  Nodes: {actual_n}, Edges: {num_edges}, Density: {density:.4f}")
                
                # Store test case
                testcase = {
                    'graph_type': graph_type,
                    'n': n,
                    'density': density,
                    'test_case_id': test_case,
                    'graph': graph,
                    'source': source,
                    'sink': sink,
                    'num_edges': num_edges
                }
                all_testcases.append(testcase)
    
    # Save to pickle file
    output_file = 'density_testcases.pkl'
    with open(output_file, 'wb') as f:
        pickle.dump(all_testcases, f)
    
    print(f"\n{'='*60}")
    print(f"Test case generation complete!")
    print(f"Total test cases generated: {len(all_testcases)}")
    print(f"Saved to: {output_file}")
    print(f"{'='*60}")
    
    # Print summary
    print("\nSummary:")
    for n in node_sizes:
        for graph_type in graph_types:
            count = sum(1 for tc in all_testcases if tc['n'] == n and tc['graph_type'] == graph_type)
            print(f"  {graph_type} (n={n}): {count} test cases")

if __name__ == "__main__":
    generate_all_testcases()