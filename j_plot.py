"""
Plot Generator for Max Flow Algorithm Analysis
Reads CSV files and generates individual plots + category summary plots
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


# Plot metadata and axis labels
PLOT_METADATA = {
    'A1': {
        'title': 'Random Graphs: Runtime vs n (Fixed Density ≈0.3)',
        'xlabel': 'Number of Nodes (n)',
        'ylabel': 'Runtime (ms)',
        'x_var': 'n',
        'group': 'A'
    },
    'A2': {
        'title': 'Dense Graphs: Runtime vs n (Density ≈0.75)',
        'xlabel': 'Number of Nodes (n)',
        'ylabel': 'Runtime (ms)',
        'x_var': 'n',
        'group': 'A'
    },
    'A3': {
        'title': 'Sparse Graphs: Runtime vs n (m = 3n edges)',
        'xlabel': 'Number of Nodes (n)',
        'ylabel': 'Runtime (ms)',
        'x_var': 'n',
        'group': 'A'
    },
    'A4': {
        'title': 'Grid Graphs: Runtime vs n (k×k grid)',
        'xlabel': 'Number of Nodes (n = k²)',
        'ylabel': 'Runtime (ms)',
        'x_var': 'n',
        'group': 'A'
    },
    'A5': {
        'title': 'Layered Graphs: Runtime vs n (Fixed 5 Layers)',
        'xlabel': 'Number of Nodes (n)',
        'ylabel': 'Runtime (ms)',
        'x_var': 'n',
        'group': 'A'
    },
    'A6': {
        'title': 'Bipartite Graphs: Runtime vs n (Balanced Partitions)',
        'xlabel': 'Number of Nodes (n)',
        'ylabel': 'Runtime (ms)',
        'x_var': 'n',
        'group': 'A'
    },
    'B1': {
        'title': 'Random Graphs: Runtime vs Density (Fixed n)',
        'xlabel': 'Graph Density',
        'ylabel': 'Runtime (ms)',
        'x_var': 'density',
        'group': 'B'
    },
    'B2': {
        'title': 'Bipartite Graphs: Runtime vs Density (Fixed n)',
        'xlabel': 'Graph Density',
        'ylabel': 'Runtime (ms)',
        'x_var': 'density',
        'group': 'B'
    },
    'C1': {
        'title': 'Layered Graphs: Runtime vs Number of Layers',
        'xlabel': 'Number of Layers',
        'ylabel': 'Runtime (ms)',
        'x_var': 'num_layers',
        'group': 'C'
    },
    'D1': {
        'title': 'Layered Graphs: Runtime vs Nodes per Layer',
        'xlabel': 'Nodes per Layer',
        'ylabel': 'Runtime (ms)',
        'x_var': 'nodes_per_layer',
        'group': 'D'
    },
    'E1': {
        'title': 'Grid Graphs: Runtime vs Grid Dimension k',
        'xlabel': 'Grid Dimension (k)',
        'ylabel': 'Runtime (ms)',
        'x_var': 'grid_k',
        'group': 'E'
    },
    'F1': {
        'title': 'Random Graphs: Runtime vs Max Capacity',
        'xlabel': 'Maximum Capacity',
        'ylabel': 'Runtime (ms)',
        'x_var': 'max_capacity',
        'group': 'F'
    },
    'F2': {
        'title': 'Dense Graphs: Runtime vs Max Capacity',
        'xlabel': 'Maximum Capacity',
        'ylabel': 'Runtime (ms)',
        'x_var': 'max_capacity',
        'group': 'F'
    },
    'F3': {
        'title': 'Sparse Graphs: Runtime vs Max Capacity',
        'xlabel': 'Maximum Capacity',
        'ylabel': 'Runtime (ms)',
        'x_var': 'max_capacity',
        'group': 'F'
    }
}


def create_output_directories():
    """Create directory structure for storing plots."""
    base_dir = 'plots'
    
    os.makedirs(base_dir, exist_ok=True)
    
    for group in ['A', 'B', 'C', 'D', 'E', 'F']:
        group_dir = os.path.join(base_dir, f'Group_{group}')
        os.makedirs(group_dir, exist_ok=True)
    
    os.makedirs(os.path.join(base_dir, 'Summaries'), exist_ok=True)
    
    return base_dir


def plot_individual(plot_id, csv_file, output_dir):
    """Generate individual plot for a specific plot ID."""
    
    if not os.path.exists(csv_file):
        print(f"WARNING: {csv_file} not found, skipping {plot_id}")
        return
    
    df = pd.read_csv(csv_file)
    
    df = df[df['runtime_ms'] >= 0]
    
    if df.empty:
        print(f"WARNING: No valid data for {plot_id}")
        return
    
    metadata = PLOT_METADATA[plot_id]
    x_var = metadata['x_var']
    
    if plot_id in ['B1', 'B2']:
        n_values = sorted(df['n'].unique())
        
        fig, axes = plt.subplots(1, len(n_values), figsize=(6*len(n_values), 5))
        if len(n_values) == 1:
            axes = [axes]
        
        for idx, n_val in enumerate(n_values):
            df_n = df[df['n'] == n_val]
            
            for algo in df_n['algorithm'].unique():
                df_algo = df_n[df_n['algorithm'] == algo]
                grouped = df_algo.groupby(x_var)['runtime_ms'].agg(['mean', 'std']).reset_index()
                
                axes[idx].errorbar(grouped[x_var], grouped['mean'], 
                                  yerr=grouped['std'], 
                                  label=algo, marker='o', capsize=5, linewidth=2, markersize=6)
            
            axes[idx].set_xlabel(metadata['xlabel'], fontsize=12, fontweight='bold')
            axes[idx].set_ylabel(metadata['ylabel'], fontsize=12, fontweight='bold')
            axes[idx].set_title(f'n = {n_val}', fontsize=13, fontweight='bold')
            axes[idx].legend(fontsize=10)
            axes[idx].grid(True, alpha=0.3)
        
        fig.suptitle(metadata['title'], fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
    
    else:
        plt.figure(figsize=(12, 7))
        
        for algo in df['algorithm'].unique():
            df_algo = df[df['algorithm'] == algo]
            grouped = df_algo.groupby(x_var)['runtime_ms'].agg(['mean', 'std']).reset_index()
            
            plt.errorbar(grouped[x_var], grouped['mean'], 
                        yerr=grouped['std'], 
                        label=algo, marker='o', capsize=5, linewidth=2, markersize=8)
        
        plt.xlabel(metadata['xlabel'], fontsize=14, fontweight='bold')
        plt.ylabel(metadata['ylabel'], fontsize=14, fontweight='bold')
        plt.title(metadata['title'], fontsize=16, fontweight='bold')
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Use log scale for capacity plots
        if plot_id in ['F1', 'F2', 'F3']:
            plt.xscale('log')
        
        plt.tight_layout()
    
    group = metadata['group']
    filename = os.path.join(output_dir, f'Group_{group}', f'{plot_id}.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Generated: {filename}")


def plot_group_summary(group, plot_ids, base_dir):
    """Generate summary plot for a group of related plots."""
    
    n_plots = len(plot_ids)
    if n_plots <= 3:
        rows, cols = 1, n_plots
        figsize = (6*cols, 5)
    elif n_plots <= 6:
        rows, cols = 2, 3
        figsize = (18, 10)
    else:
        rows, cols = 3, 3
        figsize = (18, 15)
    
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    if n_plots == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    
    for idx, plot_id in enumerate(plot_ids):
        csv_file = f'benchmark_results/{plot_id}_results.csv'
        
        if not os.path.exists(csv_file):
            axes[idx].text(0.5, 0.5, f'{plot_id}\nNo Data', 
                          ha='center', va='center', fontsize=14)
            axes[idx].set_title(plot_id, fontsize=12, fontweight='bold')
            continue
        
        df = pd.read_csv(csv_file)
        df = df[df['runtime_ms'] >= 0]
        
        if df.empty:
            axes[idx].text(0.5, 0.5, f'{plot_id}\nNo Valid Data', 
                          ha='center', va='center', fontsize=14)
            axes[idx].set_title(plot_id, fontsize=12, fontweight='bold')
            continue
        
        metadata = PLOT_METADATA[plot_id]
        x_var = metadata['x_var']
        
        for algo in df['algorithm'].unique():
            df_algo = df[df['algorithm'] == algo]
            grouped = df_algo.groupby(x_var)['runtime_ms'].agg(['mean', 'std']).reset_index()
            
            axes[idx].plot(grouped[x_var], grouped['mean'], 
                          label=algo, marker='o', linewidth=1.5, markersize=5)
        
        axes[idx].set_xlabel(metadata['xlabel'], fontsize=10)
        axes[idx].set_ylabel(metadata['ylabel'], fontsize=10)
        axes[idx].set_title(plot_id, fontsize=12, fontweight='bold')
        axes[idx].legend(fontsize=8)
        axes[idx].grid(True, alpha=0.3)
        
        # Use log scale for capacity plots
        if plot_id in ['F1', 'F2', 'F3']:
            axes[idx].set_xscale('log')
    
    for idx in range(n_plots, len(axes)):
        axes[idx].axis('off')
    
    group_titles = {
        'A': 'Group A: Fix Density, Vary n (Scalability)',
        'B': 'Group B: Fix n, Vary Density',
        'C': 'Group C: Fix Nodes-per-Layer, Vary #Layers',
        'D': 'Group D: Fix #Layers, Vary Nodes-per-Layer',
        'E': 'Group E: Vary Grid Dimension k',
        'F': 'Group F: Fix n & Density, Vary Max Capacity'
    }
    
    fig.suptitle(group_titles.get(group, f'Group {group}'), 
                 fontsize=18, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    # Save summary plot
    filename = os.path.join(base_dir, 'Summaries', f'Group_{group}_Summary.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Generated summary: {filename}")


def plot_overall_heatmap(base_dir):
    """Generate overall heatmap showing algorithm performance across all plot types."""
    
    results = []
    
    for plot_id in PLOT_METADATA.keys():
        csv_file = f'benchmark_results/{plot_id}_results.csv'
        
        if not os.path.exists(csv_file):
            continue
        
        df = pd.read_csv(csv_file)
        df = df[df['runtime_ms'] >= 0]
        
        if df.empty:
            continue
        
        # Calculate average runtime per algorithm
        avg_runtimes = df.groupby('algorithm')['runtime_ms'].mean()
        
        for algo, runtime in avg_runtimes.items():
            results.append({
                'Plot': plot_id,
                'Algorithm': algo,
                'Avg Runtime (ms)': runtime
            })
    
    if not results:
        print("WARNING: No data for overall heatmap")
        return
    
    df_heatmap = pd.DataFrame(results)
    pivot = df_heatmap.pivot(index='Plot', columns='Algorithm', values='Avg Runtime (ms)')
    
    plt.figure(figsize=(10, 12))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', 
                cbar_kws={'label': 'Average Runtime (ms)'})
    plt.xlabel('Algorithm', fontsize=14, fontweight='bold')
    plt.ylabel('Plot Category', fontsize=14, fontweight='bold')
    plt.title('Overall Performance Heatmap - All Plot Categories', 
              fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    filename = os.path.join(base_dir, 'Summaries', 'Overall_Heatmap.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Generated overall heatmap: {filename}")


def generate_all_plots():
    """Generate all individual plots and group summaries."""
    
    print("="*70)
    print("GENERATING ALL PLOTS")
    print("="*70)
    
    base_dir = create_output_directories()
    
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'
    
    print("\nGenerating individual plots...")
    for plot_id in PLOT_METADATA.keys():
        csv_file = f'benchmark_results/{plot_id}_results.csv'
        plot_individual(plot_id, csv_file, base_dir)
    
    print("\nGenerating group summary plots...")
    groups = {
        'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6'],
        'B': ['B1', 'B2'],
        'C': ['C1'],
        'D': ['D1'],
        'E': ['E1'],
        'F': ['F1', 'F2', 'F3']
    }
    
    for group, plot_ids in groups.items():
        plot_group_summary(group, plot_ids, base_dir)
    
    # Generate overall heatmap
    print("\nGenerating overall heatmap...")
    plot_overall_heatmap(base_dir)
    
    print("\n" + "="*70)
    print("PLOT GENERATION COMPLETE!")
    print(f"All plots saved in '{base_dir}/' directory")
    print("="*70)
    print("\nDirectory structure:")
    print(f"  {base_dir}/")
    print(f"    ├── Group_A/  (6 plots: A1-A6)")
    print(f"    ├── Group_B/  (2 plots: B1-B2)")
    print(f"    ├── Group_C/  (1 plot: C1)")
    print(f"    ├── Group_D/  (1 plot: D1)")
    print(f"    ├── Group_E/  (1 plot: E1)")
    print(f"    ├── Group_F/  (3 plots: F1-F3)")
    print(f"    └── Summaries/")
    print(f"          ├── Group_A_Summary.png")
    print(f"          ├── Group_B_Summary.png")
    print(f"          ├── Group_C_Summary.png")
    print(f"          ├── Group_D_Summary.png")
    print(f"          ├── Group_E_Summary.png")
    print(f"          ├── Group_F_Summary.png")
    print(f"          └── Overall_Heatmap.png")
    print("="*70)


if __name__ == "__main__":
    generate_all_plots()
