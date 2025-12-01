
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_capacity_2d():
    csv_file = 'capacity_benchmark_results.csv'
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    df = pd.read_csv(csv_file)
    
    plt.style.use('ggplot')
    
    graph_types = df['GraphType'].unique()
    capacities = df['MaxCapacity'].unique() 

    colors = {'Ford-Fulkerson': '#d62728', 'Dinic': '#1f77b4', 'Push-Relabel': '#9467bd'}
    markers = {'Ford-Fulkerson': 's', 'Dinic': 'o', 'Push-Relabel': '^'}

    for gtype in graph_types:
        for cap in capacities:
            subset = df[(df['GraphType'] == gtype) & (df['MaxCapacity'] == cap)]
            
            if subset.empty:
                continue

            agg = subset.groupby(['Algorithm', 'N'], as_index=False)['Time'].mean()
            
            plt.figure(figsize=(10, 6))
            
            for alg in agg['Algorithm'].unique():
                data = agg[agg['Algorithm'] == alg].sort_values('N')
                plt.plot(data['N'], data['Time'], 
                         label=alg, 
                         color=colors.get(alg, 'black'),
                         marker=markers.get(alg, 'o'),
                         linewidth=2,
                         markersize=6)

            cap_label = "Unit Capacity (1)" if cap == 1 else f"Variable Capacity (1-{cap})"
            plt.title(f"{gtype} - {cap_label}")
            plt.xlabel("Number of Nodes (N)")
            plt.ylabel("Time (seconds)")
            plt.legend()
            plt.grid(True)
            
            filename = f"plot_cap_{gtype}_C{cap}.png"
            plt.savefig(filename, dpi=150)
            print(f"Saved {filename}")
            plt.close()

if __name__ == "__main__":
    plot_capacity_2d()
