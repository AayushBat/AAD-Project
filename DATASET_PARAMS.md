# Dataset Parameters - Quick Reference

## Exact Parameter Values for Each Plot

### GROUP A: Fix Density, Vary n

**A1 - Random Graphs (density=0.3)**
- n values: [50, 150, 300, 500, 700, 900]
- 3 trials each = 18 test cases

**A2 - Dense Graphs (density=0.75)**
- n values: [50, 100, 200, 350, 500]
- 4 trials each = 20 test cases

**A3 - Sparse Graphs (m=3n)**
- n values: [50, 150, 300, 500, 700, 1000]
- 3 trials each = 18 test cases

**A4 - Grid Graphs (k×k)**
- k values: [5, 10, 15, 20, 25, 30]
- n values: [25, 100, 225, 400, 625, 900]
- 3 trials each = 18 test cases

**A5 - Layered Graphs (5 layers)**
- layer_width: [10, 20, 40, 60, 80, 100]
- 3 trials each = 18 test cases

**A6 - Bipartite Graphs (balanced)**
- partition_size: [25, 50, 100, 150, 200]
- total n: [50, 100, 200, 300, 400]
- 4 trials each = 20 test cases

---

### GROUP B: Fix n, Vary Density

**B1 - Random Graphs**
- n values: [100, 300, 500]
- density: [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
- 1 trial each = 18 test cases (3×6×1)

**B2 - Bipartite Graphs**
- n values: [100, 200, 400]
- density: [0.2, 0.4, 0.6, 0.8, 1.0]
- 1 trial each = 15 test cases (3×5×1)

---

### GROUP C: Fix Nodes-per-Layer, Vary #Layers

**C1 - Layered Graphs (20 nodes/layer)**
- num_layers: [3, 5, 8, 12, 15, 20]
- 3 trials each = 18 test cases

---

### GROUP D: Fix #Layers, Vary Nodes-per-Layer

**D1 - Layered Graphs (6 layers)**
- nodes_per_layer: [10, 20, 40, 60, 80, 100]
- 3 trials each = 18 test cases

---

### GROUP E: Vary Grid Dimension k

**E1 - Grid Graphs**
- k values: [5, 10, 15, 20, 25, 30]
- n values: [25, 100, 225, 400, 625, 900]
- 3 trials each = 18 test cases

---

### GROUP F: Fix n & Density, Vary Max Capacity

**F1 - Random Graphs (n=300, density=0.3)**
- capacity: [1, 10, 50, 100, 500, 1000]
- 3 trials each = 18 test cases

**F2 - Dense Graphs (n=200, density=0.75)**
- capacity: [1, 10, 50, 100, 500]
- 4 trials each = 20 test cases

**F3 - Sparse Graphs (n=400, m=1200)**
- capacity: [1, 10, 50, 100, 500, 1000]
- 3 trials each = 18 test cases

---

## Summary

- **Total plots**: 14
- **Test cases per plot**: 15-20 (average ~18)
- **Total test cases**: 255
- **Total algorithm runs**: 765 (255 × 3)
- **Estimated runtime**: 10-30 minutes

## Coverage Strategy

Each plot ensures uniform coverage:
- **Small**: 2-3 data points in lower 1/3 of range
- **Medium**: 2-3 data points in middle 1/3 of range
- **Large**: 2-3 data points in upper 1/3 of range

This provides enough data points to see trends without excessive runtime.
