import networkx as nx
import matplotlib.pyplot as plt
from ford_fulkerson import ford_fulkerson
from graphy import Graph

def visualize_min_cut_theorem():
    print("Generating visual proof for Max-Flow Min-Cut Theorem...")
    
    G_custom = Graph(6)
    edges = [
        (0, 1, 10), (0, 2, 10),
        (1, 2, 2), (1, 3, 4), (1, 4, 8),
        (2, 4, 9),
        (3, 5, 10),
        (4, 3, 6), (4, 5, 10)
    ]
    for u, v, c in edges:
        G_custom.add_edge(u, v, c)
    
    s, t = 0, 5

    nx_G = nx.DiGraph()
    for u, v, c in edges:
        nx_G.add_edge(u, v, capacity=c)
        
    flow_value, flow_dict = nx.maximum_flow(nx_G, s, t)
    cut_value, partition = nx.minimum_cut(nx_G, s, t)
    reachable, non_reachable = partition

    print(f"Max Flow: {flow_value}")
    print(f"Min Cut: {cut_value}")
    print(f"Theorem Holds: {flow_value == cut_value}")

    pos = nx.spring_layout(nx_G, seed=42)
    plt.figure(figsize=(10, 6))

    nx.draw_networkx_nodes(nx_G, pos, nodelist=list(reachable), node_color='lightblue', label="Source Side (S)")
    nx.draw_networkx_nodes(nx_G, pos, nodelist=list(non_reachable), node_color='salmon', label="Sink Side (T)")
    nx.draw_networkx_labels(nx_G, pos)

    cut_edges = []
    other_edges = []
    for u, v in nx_G.edges():
        if u in reachable and v in non_reachable:
            cut_edges.append((u, v))
        else:
            other_edges.append((u, v))

    nx.draw_networkx_edges(nx_G, pos, edgelist=other_edges, edge_color='gray', alpha=0.5)
    nx.draw_networkx_edges(nx_G, pos, edgelist=cut_edges, edge_color='black', width=2.5, style='dashed', label='Min-Cut Edges')

    edge_labels = {(u, v): f"{c}" for u, v, c in edges}
    nx.draw_networkx_edge_labels(nx_G, pos, edge_labels=edge_labels)

    plt.title(f"Max-Flow Min-Cut Theorem Visualization\nMax Flow = {flow_value} | Min Cut Capacity = {cut_value}")
    plt.legend()
    plt.axis('off')
    
    plt.savefig('visual_proof_min_cut.png')
    print("Saved visualization to visual_proof_min_cut.png")

if __name__ == "__main__":
    visualize_min_cut_theorem()
