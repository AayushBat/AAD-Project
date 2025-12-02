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
    """Convert Graph object to dictionary format."""
    graph_dict = {}
    for u in range(g.n):
        graph_dict[u] = {}
        for v, cap in g.adj[u].items():
            graph_dict[u][v] = cap
    return graph_dict


def generate_grid_graph(k, cap=10):
    """Generate a k×k grid graph with source and sink."""
    n = k * k
    g = Graph(n + 2)
    s, t = 0, n + 1
    
    # Source to first column
    for i in range(k):
        g.add_edge(s, 1 + i * k, cap)
    
    # Grid connections (right and down)
    for i in range(k):
        for j in range(k):
            node = 1 + i * k + j
            if j < k - 1:  # Right
                g.add_edge(node, node + 1, cap)
            if i < k - 1:  # Down
                g.add_edge(node, node + k, cap)
    
    # Last column to sink
    for i in range(k):
        g.add_edge(1 + i * k + (k - 1), t, cap)
    
    return g, s, t


def generate_A1_random_vary_n():
    """A1: Random graphs - runtime vs n (fixed density ~0.3)"""
    datasets = []
    fixed_density = 0.3
    fixed_cap = 10
    n_values = [50, 150, 300, 500, 700, 900]  
    trials_per_n = 3  
    
    for n in n_values:
        for trial in range(trials_per_n):
            seed = 1000 + trial
            g = dense_random_graph(n, density=fixed_density, cap=fixed_cap, seed=seed)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'A1',
                'graph_type': 'random',
                'n': n,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': fixed_cap,
                'num_layers': None,
                'nodes_per_layer': None,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': n - 1,
                'trial': trial
            })
    
    print(f"Generated A1: {len(datasets)} random graphs (vary n, fixed density={fixed_density})")
    return datasets


def generate_A2_dense_vary_n():
    """A2: Dense graphs - runtime vs n (density ~0.7-0.8)"""
    datasets = []
    fixed_density = 0.75
    fixed_cap = 10
    n_values = [50, 100, 200, 350, 500] 
    trials_per_n = 4 
    
    for n in n_values:
        for trial in range(trials_per_n):
            seed = 2000 + trial
            g = dense_random_graph(n, density=fixed_density, cap=fixed_cap, seed=seed)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'A2',
                'graph_type': 'dense',
                'n': n,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': fixed_cap,
                'num_layers': None,
                'nodes_per_layer': None,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': n - 1,
                'trial': trial
            })
    
    print(f"Generated A2: {len(datasets)} dense graphs (vary n, fixed density={fixed_density})")
    return datasets


def generate_A3_sparse_vary_n():
    """A3: Sparse graphs - runtime vs n (m = 3*n edges)"""
    datasets = []
    fixed_cap = 10
    n_values = [50, 150, 300, 500, 700, 1000] 
    trials_per_n = 3
    
    for n in n_values:
        for trial in range(trials_per_n):
            seed = 3000 + trial
            m = 3 * n  
            g = sparse_random_graph(n, m, cap=fixed_cap, seed=seed)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'A3',
                'graph_type': 'sparse',
                'n': n,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': fixed_cap,
                'num_layers': None,
                'nodes_per_layer': None,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': n - 1,
                'trial': trial
            })
    
    print(f"Generated A3: {len(datasets)} sparse graphs (vary n, m=3n)")
    return datasets


def generate_A4_grid_vary_n():
    """A4: Grid graphs - runtime vs n (k×k grid, k varies)"""
    datasets = []
    fixed_cap = 10
    k_values = [5, 10, 15, 20, 25, 30] 
    trials_per_k = 3 
    
    for k in k_values:
        for trial in range(trials_per_k):
            g, s, t = generate_grid_graph(k, cap=fixed_cap)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'A4',
                'graph_type': 'grid',
                'n': k * k,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': fixed_cap,
                'num_layers': None,
                'nodes_per_layer': None,
                'grid_k': k,
                'graph': graph_dict,
                'source': s,
                'sink': t,
                'trial': trial
            })
    
    print(f"Generated A4: {len(datasets)} grid graphs (vary k, n=k²)")
    return datasets


def generate_A5_layered_vary_n():
    """A5: Layered graphs - runtime vs n (fixed layers=5, vary layer_width)"""
    datasets = []
    fixed_layers = 5
    fixed_cap = 10
    layer_widths = [10, 20, 40, 60, 80, 100] 
    trials_per_width = 3 
    
    for width in layer_widths:
        for trial in range(trials_per_width):
            g = layered_graph(n_layers=fixed_layers, layer_width=width, cap=fixed_cap)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'A5',
                'graph_type': 'layered',
                'n': g.n - 2,  # Exclude source and sink
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': fixed_cap,
                'num_layers': fixed_layers,
                'nodes_per_layer': width,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': g.n - 1,
                'trial': trial
            })
    
    print(f"Generated A5: {len(datasets)} layered graphs (vary layer_width, fixed layers={fixed_layers})")
    return datasets


def generate_A6_bipartite_vary_n():
    """A6: Bipartite graphs - runtime vs n (balanced partitions)"""
    datasets = []
    fixed_cap = 10
    partition_sizes = [25, 50, 100, 150, 200]  
    trials_per_size = 4 
    
    for size in partition_sizes:
        for trial in range(trials_per_size):
            g = bipartite_graph(n_left=size, n_right=size, cap=fixed_cap)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'A6',
                'graph_type': 'bipartite',
                'n': 2 * size,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': fixed_cap,
                'num_layers': None,
                'nodes_per_layer': None,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': g.n - 1,
                'trial': trial
            })
    
    print(f"Generated A6: {len(datasets)} bipartite graphs (vary partition_size)")
    return datasets


def generate_B1_random_vary_density():
    """B1: Random graphs - runtime vs density (3 fixed n values)"""
    datasets = []
    fixed_cap = 10
    n_values = [100, 300, 500] 
    density_values = [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]  
    trials_per_config = 1 
    
    for n in n_values:
        for density in density_values:
            for trial in range(trials_per_config):
                seed = 4000 + n + int(density * 100) + trial
                g = dense_random_graph(n, density=density, cap=fixed_cap, seed=seed)
                graph_dict = graph_to_dict(g)
                num_edges = count_edges(g)
                actual_density = calculate_density(g.n, num_edges)
                
                datasets.append({
                    'plot_id': 'B1',
                    'graph_type': 'random',
                    'n': n,
                    'actual_n': g.n,
                    'density': actual_density,
                    'max_capacity': fixed_cap,
                    'num_layers': None,
                    'nodes_per_layer': None,
                    'grid_k': None,
                    'graph': graph_dict,
                    'source': 0,
                    'sink': n - 1,
                    'trial': trial
                })
    
    print(f"Generated B1: {len(datasets)} random graphs (vary density, n in {n_values})")
    return datasets


def generate_B2_bipartite_vary_density():
    """B2: Bipartite graphs - runtime vs density (3 fixed n values)"""
    datasets = []
    fixed_cap = 10
    n_values = [100, 200, 400] 
    density_values = [0.2, 0.4, 0.6, 0.8, 1.0]
    trials_per_config = 1
    
    for n in n_values:
        for density in density_values:
            for trial in range(trials_per_config):
                # For bipartite, we need to control edge density
                # Generate complete bipartite then subsample
                seed = 5000 + n + int(density * 100) + trial
                partition_size = n // 2
                
                g = Graph(n + 2)
                s, t = 0, n + 1
                
                for i in range(partition_size):
                    g.add_edge(s, 1 + i, fixed_cap)
                
                import random
                random.seed(seed)
                for i in range(partition_size):
                    for j in range(partition_size):
                        if random.random() < density:
                            u = 1 + i
                            v = 1 + partition_size + j
                            g.add_edge(u, v, fixed_cap)
                
                for j in range(partition_size):
                    g.add_edge(1 + partition_size + j, t, fixed_cap)
                
                graph_dict = graph_to_dict(g)
                num_edges = count_edges(g)
                actual_density = calculate_density(g.n, num_edges)
                
                datasets.append({
                    'plot_id': 'B2',
                    'graph_type': 'bipartite',
                    'n': n,
                    'actual_n': g.n,
                    'density': actual_density,
                    'max_capacity': fixed_cap,
                    'num_layers': None,
                    'nodes_per_layer': None,
                    'grid_k': None,
                    'graph': graph_dict,
                    'source': s,
                    'sink': t,
                    'trial': trial
                })
    
    print(f"Generated B2: {len(datasets)} bipartite graphs (vary density, n in {n_values})")
    return datasets


def generate_C1_layered_vary_layers():
    """C1: Layered graphs - runtime vs number of layers (fixed nodes_per_layer)"""
    datasets = []
    fixed_nodes_per_layer = 20
    fixed_cap = 10
    layer_counts = [3, 5, 8, 12, 15, 20] 
    trials_per_count = 3 
    
    for num_layers in layer_counts:
        for trial in range(trials_per_count):
            g = layered_graph(n_layers=num_layers, layer_width=fixed_nodes_per_layer, cap=fixed_cap)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'C1',
                'graph_type': 'layered',
                'n': g.n - 2,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': fixed_cap,
                'num_layers': num_layers,
                'nodes_per_layer': fixed_nodes_per_layer,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': g.n - 1,
                'trial': trial
            })
    
    print(f"Generated C1: {len(datasets)} layered graphs (vary num_layers, fixed width={fixed_nodes_per_layer})")
    return datasets



def generate_D1_layered_vary_width():
    """D1: Layered graphs - runtime vs nodes per layer (fixed num_layers)"""
    datasets = []
    fixed_layers = 6
    fixed_cap = 10
    width_values = [10, 20, 40, 60, 80, 100] 
    trials_per_width = 3 
    
    for width in width_values:
        for trial in range(trials_per_width):
            g = layered_graph(n_layers=fixed_layers, layer_width=width, cap=fixed_cap)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'D1',
                'graph_type': 'layered',
                'n': g.n - 2,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': fixed_cap,
                'num_layers': fixed_layers,
                'nodes_per_layer': width,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': g.n - 1,
                'trial': trial
            })
    
    print(f"Generated D1: {len(datasets)} layered graphs (vary nodes_per_layer, fixed layers={fixed_layers})")
    return datasets



def generate_E1_grid_vary_k():
    """E1: Grid graphs - runtime vs k (grid dimension)"""
    datasets = []
    fixed_cap = 10
    k_values = [5, 10, 15, 20, 25, 30]
    trials_per_k = 3 
    
    for k in k_values:
        for trial in range(trials_per_k):
            g, s, t = generate_grid_graph(k, cap=fixed_cap)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'E1',
                'graph_type': 'grid',
                'n': k * k,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': fixed_cap,
                'num_layers': None,
                'nodes_per_layer': None,
                'grid_k': k,
                'graph': graph_dict,
                'source': s,
                'sink': t,
                'trial': trial
            })
    
    print(f"Generated E1: {len(datasets)} grid graphs (vary k)")
    return datasets



def generate_F1_random_vary_capacity():
    """F1: Random graphs - runtime vs capacity scale"""
    datasets = []
    fixed_n = 300
    fixed_density = 0.3
    capacity_values = [1, 10, 50, 100, 500, 1000] 
    trials_per_cap = 3
    
    for max_cap in capacity_values:
        for trial in range(trials_per_cap):
            seed = 6000 + max_cap + trial
            g = dense_random_graph(fixed_n, density=fixed_density, cap=max_cap, seed=seed)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'F1',
                'graph_type': 'random',
                'n': fixed_n,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': max_cap,
                'num_layers': None,
                'nodes_per_layer': None,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': fixed_n - 1,
                'trial': trial
            })
    
    print(f"Generated F1: {len(datasets)} random graphs (vary max_capacity)")
    return datasets


def generate_F2_dense_vary_capacity():
    """F2: Dense graphs - runtime vs capacity scale"""
    datasets = []
    fixed_n = 200
    fixed_density = 0.75
    capacity_values = [1, 10, 50, 100, 500] 
    trials_per_cap = 4
    
    for max_cap in capacity_values:
        for trial in range(trials_per_cap):
            seed = 7000 + max_cap + trial
            g = dense_random_graph(fixed_n, density=fixed_density, cap=max_cap, seed=seed)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'F2',
                'graph_type': 'dense',
                'n': fixed_n,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': max_cap,
                'num_layers': None,
                'nodes_per_layer': None,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': fixed_n - 1,
                'trial': trial
            })
    
    print(f"Generated F2: {len(datasets)} dense graphs (vary max_capacity)")
    return datasets


def generate_F3_sparse_vary_capacity():
    """F3: Sparse graphs - runtime vs capacity scale"""
    datasets = []
    fixed_n = 400
    fixed_m = 1200 
    capacity_values = [1, 10, 50, 100, 500, 1000] 
    trials_per_cap = 3 
    
    for max_cap in capacity_values:
        for trial in range(trials_per_cap):
            seed = 8000 + max_cap + trial
            g = sparse_random_graph(fixed_n, fixed_m, cap=max_cap, seed=seed)
            graph_dict = graph_to_dict(g)
            num_edges = count_edges(g)
            actual_density = calculate_density(g.n, num_edges)
            
            datasets.append({
                'plot_id': 'F3',
                'graph_type': 'sparse',
                'n': fixed_n,
                'actual_n': g.n,
                'density': actual_density,
                'max_capacity': max_cap,
                'num_layers': None,
                'nodes_per_layer': None,
                'grid_k': None,
                'graph': graph_dict,
                'source': 0,
                'sink': fixed_n - 1,
                'trial': trial
            })
    
    print(f"Generated F3: {len(datasets)} sparse graphs (vary max_capacity)")
    return datasets


def generate_all_datasets():
    """Generate all datasets for all 14 plots."""
    
    print("="*70)
    print("GENERATING ALL DATASETS FOR 14 PLOT CATEGORIES")
    print("="*70)
    
    all_datasets = []
    
    # Group A: Fix density, vary n
    print("\n--- GROUP A: FIX DENSITY, VARY n ---")
    all_datasets.extend(generate_A1_random_vary_n())
    all_datasets.extend(generate_A2_dense_vary_n())
    all_datasets.extend(generate_A3_sparse_vary_n())
    all_datasets.extend(generate_A4_grid_vary_n())
    all_datasets.extend(generate_A5_layered_vary_n())
    all_datasets.extend(generate_A6_bipartite_vary_n())
    
    # Group B: Fix n, vary density
    print("\n--- GROUP B: FIX n, VARY DENSITY ---")
    all_datasets.extend(generate_B1_random_vary_density())
    all_datasets.extend(generate_B2_bipartite_vary_density())
    
    # Group C: Fix nodes-per-layer, vary #layers
    print("\n--- GROUP C: FIX NODES-PER-LAYER, VARY #LAYERS ---")
    all_datasets.extend(generate_C1_layered_vary_layers())
    
    # Group D: Fix #layers, vary nodes-per-layer
    print("\n--- GROUP D: FIX #LAYERS, VARY NODES-PER-LAYER ---")
    all_datasets.extend(generate_D1_layered_vary_width())
    
    # Group E: Vary grid dimension k
    print("\n--- GROUP E: VARY GRID DIMENSION k ---")
    all_datasets.extend(generate_E1_grid_vary_k())
    
    # Group F: Fix n & density, vary max capacity
    print("\n--- GROUP F: FIX n & DENSITY, VARY MAX CAPACITY ---")
    all_datasets.extend(generate_F1_random_vary_capacity())
    all_datasets.extend(generate_F2_dense_vary_capacity())
    all_datasets.extend(generate_F3_sparse_vary_capacity())
    
    # Save to pickle file
    output_file = 'j_datasets.pkl'
    with open(output_file, 'wb') as f:
        pickle.dump(all_datasets, f)
    
    print("\n" + "="*70)
    print(f"DATASET GENERATION COMPLETE!")
    print(f"Total datasets generated: {len(all_datasets)}")
    print(f"Saved to: {output_file}")
    print("="*70)
    
    # Print summary by plot_id
    print("\nSummary by Plot ID:")
    plot_counts = {}
    for ds in all_datasets:
        plot_id = ds['plot_id']
        plot_counts[plot_id] = plot_counts.get(plot_id, 0) + 1
    
    for plot_id in sorted(plot_counts.keys()):
        print(f"  {plot_id}: {plot_counts[plot_id]} test cases")
    
    return all_datasets


if __name__ == "__main__":
    generate_all_datasets()
