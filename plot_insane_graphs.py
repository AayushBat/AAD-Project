import pandas as pd
import matplotlib.pyplot as plt

def plot_results(csv_file='advanced_benchmark_results.csv'):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Run advanced_benchmark.py first.")
        return

    plt.style.use('ggplot')
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'sans-serif'
    })

    marker_map = {
        'Ford-Fulkerson': 'o',
        'Dinic': 's',
        'Push-Relabel': '^'
    }

    graph_types = df['GraphType'].unique()

    for gtype in graph_types:
        subset = df[df['GraphType'] == gtype].copy()
        if subset.empty:
            continue

        subset = subset.groupby(['Algorithm', 'N'], as_index=False)['Time'].mean()
        subset = subset.sort_values(by='N')

        plt.figure(figsize=(10, 6))

        for alg in subset['Algorithm'].unique():
            data = subset[subset['Algorithm'] == alg]

            plt.plot(
                data['N'],
                data['Time'],
                marker=marker_map.get(alg, 'o'),
                linewidth=2.5,
                label=alg
            )

        plt.title(f"{gtype} Graphs — Algorithm Performance", fontsize=16, fontweight='bold')
        plt.xlabel("N (Number of Nodes)", fontsize=14)
        plt.ylabel("Time (seconds)", fontsize=14)

        plt.legend(title="Algorithm", title_fontsize=13, fontsize=12)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()

        filename = f"plot_{gtype.lower()}.png"
        plt.savefig(filename, dpi=300)
        print(f"Generated {filename}")

if __name__ == "__main__":
    plot_results()
