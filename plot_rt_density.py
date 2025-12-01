import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def create_output_directory():
    """Create directory for storing plots."""
    output_dir = 'runtime_density'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def plot_graph_type_density(df, graph_type, output_dir):
    """Create runtime vs density plot for a specific graph type."""
    df_filtered = df[df['graph_type'] == graph_type]
    
    if df_filtered.empty:
        print(f"No data for {graph_type}")
        return
    
    plt.figure(figsize=(12, 8))
    
    for algo in df_filtered['algorithm'].unique():
        df_algo = df_filtered[df_filtered['algorithm'] == algo]
        
        grouped = df_algo.groupby('density')['runtime'].agg(['mean', 'std']).reset_index()
        
        plt.errorbar(grouped['density'], grouped['mean'], 
                    yerr=grouped['std'], 
                    label=algo, marker='o', capsize=5, linewidth=2, markersize=8)
    
    plt.xlabel('Graph Density', fontsize=14, fontweight='bold')
    plt.ylabel('Runtime (seconds)', fontsize=14, fontweight='bold')
    plt.title(f'Runtime vs Density - {graph_type.capitalize()} Graphs', 
              fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, f'density_{graph_type}.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")

def plot_overall_comparison(df, output_dir):
    """Create overall comparison plot across all graph types."""
    plt.figure(figsize=(16, 10))
    
    graph_types = df['graph_type'].unique()
    algorithms = df['algorithm'].unique()
    
    for idx, algo in enumerate(algorithms, 1):
        plt.subplot(2, 2, idx)
        
        for graph_type in graph_types:
            df_filtered = df[(df['algorithm'] == algo) & (df['graph_type'] == graph_type)]
            
            if not df_filtered.empty:
                grouped = df_filtered.groupby('density')['runtime'].mean().reset_index()
                plt.plot(grouped['density'], grouped['runtime'], 
                        label=graph_type.capitalize(), marker='o', linewidth=2, markersize=6)
        
        plt.xlabel('Graph Density', fontsize=12, fontweight='bold')
        plt.ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
        plt.title(f'{algo}', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = os.path.join(output_dir, 'density_overall_comparison.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")

def plot_algorithm_comparison_heatmap(df, output_dir):
    """Create heatmap showing average runtime for each algorithm-graph type combination."""
    # Calculate average runtime for each combination
    pivot_data = df.groupby(['graph_type', 'algorithm'])['runtime'].mean().unstack()
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_data, annot=True, fmt='.4f', cmap='YlOrRd', 
                cbar_kws={'label': 'Average Runtime (seconds)'})
    plt.xlabel('Algorithm', fontsize=14, fontweight='bold')
    plt.ylabel('Graph Type', fontsize=14, fontweight='bold')
    plt.title('Average Runtime Heatmap - All Configurations', 
              fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    filename = os.path.join(output_dir, 'density_heatmap.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")

def plot_density_distribution(df, output_dir):
    """Plot the distribution of densities for each graph type."""
    plt.figure(figsize=(14, 8))
    
    graph_types = df['graph_type'].unique()
    for graph_type in graph_types:
        df_filtered = df[df['graph_type'] == graph_type]
        densities = df_filtered['density'].unique()
        plt.scatter([graph_type] * len(densities), densities, 
                   alpha=0.6, s=100, label=graph_type.capitalize())
    
    plt.xlabel('Graph Type', fontsize=14, fontweight='bold')
    plt.ylabel('Density', fontsize=14, fontweight='bold')
    plt.title('Density Distribution by Graph Type', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    filename = os.path.join(output_dir, 'density_distribution.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")

def generate_all_plots(csv_filename='density_benchmark_results.csv'):
    """Generate all plots from the benchmark results."""
    
    print(f"Reading data from {csv_filename}...")
    
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print(f"ERROR: {csv_filename} not found!")
        print("Please run fixn_run_benchmarks.py first.")
        return
    
    df = df[df['runtime'] >= 0]
    
    print(f"Loaded {len(df)} valid results")
    print(f"Graph types: {df['graph_type'].unique()}")
    print(f"Algorithms: {df['algorithm'].unique()}")
    
    output_dir = create_output_directory()
    print(f"\nCreating plots in '{output_dir}' directory...")
    
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'
    
    print("\nGenerating individual graph type plots...")
    for graph_type in df['graph_type'].unique():
        plot_graph_type_density(df, graph_type, output_dir)
    
    print("\nGenerating overall comparison plot...")
    plot_overall_comparison(df, output_dir)
    
    print("\nGenerating heatmap...")
    plot_algorithm_comparison_heatmap(df, output_dir)
    
    print("\nGenerating density distribution plot...")
    plot_density_distribution(df, output_dir)
    
    print("\n" + "="*60)
    print("All plots generated successfully!")
    print(f"Check the '{output_dir}' folder for the plots")
    print("="*60)

if __name__ == "__main__":
    generate_all_plots()