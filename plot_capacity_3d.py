import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_3d_capacity():
    try:
        df = pd.read_csv('capacity_benchmark_results.csv')
    except FileNotFoundError:
        print("Error: capacity_benchmark_results.csv not found.")
        return

    graph_types = df['GraphType'].unique()

    for gtype in graph_types:
        subset_g = df[df['GraphType'] == gtype]
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')

        algs = subset_g['Algorithm'].unique()
        colors = {'Ford-Fulkerson': 'red', 'Dinic': 'blue', 'Push-Relabel': 'green'}

        for alg in algs:
            data = subset_g[subset_g['Algorithm'] == alg]
            
            grouped = data.groupby(['N', 'Capacity'])['Time'].mean().reset_index()
            
            pivot_table = grouped.pivot(index='Capacity', columns='N', values='Time')
            
            X_vals = pivot_table.columns.values
            Y_vals = np.log10(pivot_table.index.values)
            X, Y = np.meshgrid(X_vals, Y_vals)
            Z = pivot_table.values

            ax.plot_surface(X, Y, Z, alpha=0.5, color=colors.get(alg, 'gray'), label=alg)
            ax.plot([0], [0], [0], color=colors.get(alg, 'gray'), label=alg)

        ax.set_xlabel('Number of Nodes (N)')
        ax.set_ylabel('Log10(Max Capacity)')
        ax.set_zlabel('Time (seconds)')
        ax.set_title(f'3D Performance: {gtype} (Time vs N vs Capacity)')
        ax.legend()

        output_file = f"plot_3d_capacity_{gtype}.png"
        plt.savefig(output_file)
        print(f"Saved 3D plot to {output_file}")
        plt.close()

if __name__ == "__main__":
    plot_3d_capacity()
