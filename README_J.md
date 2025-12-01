# Max Flow Algorithm Benchmarking System

Complete benchmarking and visualization system for comparing three max flow algorithms:
- **Ford-Fulkerson**
- **Dinic's Algorithm**
- **Push-Relabel**

## 📊 Plot Categories (14 Total + 6 Summaries)

### Group A: Fix Density, Vary n (Scalability)
- **A1**: Random graphs (density ≈ 0.3)
- **A2**: Dense graphs (density ≈ 0.75)
- **A3**: Sparse graphs (m = 3n edges)
- **A4**: Grid graphs (k×k)
- **A5**: Layered graphs (5 layers)
- **A6**: Bipartite graphs (balanced partitions)

### Group B: Fix n, Vary Density
- **B1**: Random graphs (n ∈ {100, 300, 500})
- **B2**: Bipartite graphs (n ∈ {100, 200, 400})

### Group C: Fix Nodes-per-Layer, Vary #Layers
- **C1**: Layered graphs (20 nodes/layer)

### Group D: Fix #Layers, Vary Nodes-per-Layer
- **D1**: Layered graphs (6 layers)

### Group E: Vary Grid Dimension k
- **E1**: Grid graphs (k varies)

### Group F: Fix n & Density, Vary Max Capacity
- **F1**: Random graphs
- **F2**: Dense graphs
- **F3**: Sparse graphs

---

## 🚀 Usage

### Step 1: Generate Datasets
```bash
python3 j_dtgen.py
```
**Output**: `j_datasets.pkl` (contains all graph instances for all 14 plot categories)

**What it does**:
- Generates graphs with controlled parameters for each plot category
- Creates **~255 test instances total** (~18-20 per plot)
- Varies the appropriate parameter (n, density, capacity, etc.) while keeping others fixed
- Ensures uniform coverage: small, medium, and large values
- Max nodes: 1000 (500 for dense graphs to keep runtime reasonable)

### Step 2: Run Benchmarks
```bash
python3 j_run.py
```
**Output**: `benchmark_results/` directory with 14 CSV files (one per plot)

**What it does**:
- Loads all generated graphs
- Runs Ford-Fulkerson, Dinic, and Push-Relabel on each
- Records runtime (milliseconds), max flow value, and metadata
- Saves results to CSV files grouped by plot ID

### Step 3: Generate Plots
```bash
python3 j_plot.py
```
**Output**: `plots/` directory with organized PNG files

**What it does**:
- Reads CSV results
- Generates 14 individual plots
- Creates 6 group summary plots
- Generates overall performance heatmap

---

## 📁 Output Structure

```
plots/
├── Group_A/
│   ├── A1.png  (Random: runtime vs n)
│   ├── A2.png  (Dense: runtime vs n)
│   ├── A3.png  (Sparse: runtime vs n)
│   ├── A4.png  (Grid: runtime vs n)
│   ├── A5.png  (Layered: runtime vs n)
│   └── A6.png  (Bipartite: runtime vs n)
├── Group_B/
│   ├── B1.png  (Random: runtime vs density)
│   └── B2.png  (Bipartite: runtime vs density)
├── Group_C/
│   └── C1.png  (Layered: runtime vs #layers)
├── Group_D/
│   └── D1.png  (Layered: runtime vs nodes/layer)
├── Group_E/
│   └── E1.png  (Grid: runtime vs k)
├── Group_F/
│   ├── F1.png  (Random: runtime vs capacity)
│   ├── F2.png  (Dense: runtime vs capacity)
│   └── F3.png  (Sparse: runtime vs capacity)
└── Summaries/
    ├── Group_A_Summary.png  (All 6 A plots combined)
    ├── Group_B_Summary.png  (Both B plots)
    ├── Group_C_Summary.png
    ├── Group_D_Summary.png
    ├── Group_E_Summary.png
    ├── Group_F_Summary.png  (All 3 F plots combined)
    └── Overall_Heatmap.png  (Algorithm comparison across all categories)
```

---

## 📋 CSV File Format

Each CSV in `benchmark_results/` contains:

| Column | Description |
|--------|-------------|
| `algorithm` | Ford-Fulkerson / Dinic / Push-Relabel |
| `n` | Number of nodes (parameter value) |
| `actual_n` | Actual nodes including source/sink |
| `density` | Graph density (edges / max_possible_edges) |
| `num_layers` | Number of layers (layered graphs only) |
| `nodes_per_layer` | Nodes per layer (layered graphs only) |
| `grid_k` | Grid dimension k (grid graphs only) |
| `max_capacity` | Maximum edge capacity |
| `runtime_ms` | Runtime in milliseconds |
| `max_flow` | Computed max flow value |
| `trial` | Trial number (for repeated experiments) |
| `graph_type` | random / dense / sparse / grid / layered / bipartite |
| `error` | Error message (if any) |

---

## 🔧 Technical Details

### Graph Generation Parameters

**Group A (Scalability)**:
- n varies: 50 → 1500 (depending on graph type)
- Density fixed per graph type
- Capacity fixed at 10

**Group B (Density Variation)**:
- n fixed at 3 values
- Density varies: 0.05 → 1.0
- Capacity fixed at 10

**Group C & D (Layered Structure)**:
- Varies layers or nodes-per-layer
- Other parameter fixed
- Capacity fixed at 10

**Group E (Grid)**:
- k varies: 5 → 35
- n = k²
- Capacity fixed at 10

**Group F (Capacity Scaling)**:
- n and density fixed
- Capacity varies: 1 → 1000
- Tests algorithm sensitivity to edge capacities

### Trials per Configuration
- Most plots: 3 trials for statistical reliability
- Some plots (A2, A6, F2): 4 trials
- B-group plots: 1 trial (already testing multiple n values)

### Test Cases Per Plot
Each plot has **15-20 test cases** uniformly distributed across:
- **Small values**: Lower range of x-axis
- **Medium values**: Mid-range of x-axis  
- **Large values**: Upper range of x-axis

**Total**: 255 test cases across all 14 plots = 765 algorithm runs

---

## 📊 Plot Features

- **Error bars**: Show standard deviation across trials
- **Log scale**: Used for capacity plots (F1, F2, F3)
- **Multiple subplots**: B1 and B2 show separate plots for each n value
- **Color coding**: Consistent algorithm colors across all plots
- **High resolution**: All plots saved at 300 DPI

---

## 🎯 Analysis Goals

1. **Scalability (Group A)**: How do algorithms scale with graph size?
2. **Density Impact (Group B)**: How does edge density affect performance?
3. **Structural Complexity (C, D, E)**: How do graph structures matter?
4. **Capacity Sensitivity (Group F)**: Are algorithms affected by capacity values?

---

## ⚙️ Requirements

- Python 3.7+
- pandas
- matplotlib
- seaborn
- numpy

Install dependencies:
```bash
pip install pandas matplotlib seaborn numpy
```

---

## 🔍 Interpreting Results

- **Ford-Fulkerson**: May show exponential behavior with high capacities (F-group)
- **Dinic**: Generally efficient on layered structures
- **Push-Relabel**: Often fastest on dense graphs, may struggle on sparse

Look for:
- Which algorithm wins in each category?
- Where do algorithms show similar performance?
- Any surprising outliers or patterns?

---

## 📝 Notes

- Benchmarking step 2 may take **10-30 minutes** depending on your system (reduced from original estimate)
- Failed runs (errors) are recorded but excluded from plots
- All graphs use the same random seed base for reproducibility
- WSL/headless environments supported via Agg backend
- Maximum node count capped at 1000 (500 for dense graphs) for reasonable runtimes
- Each plot has ~20 test cases with uniform coverage of the x-axis range

---

## 🤝 Credits

Generated for AAD (Advanced Algorithm Design) project comparing max flow algorithms.
