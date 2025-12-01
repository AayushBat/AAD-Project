# Makefile for Max Flow Project

PYTHON = python3

.PHONY: all clean benchmark capacity plot visualize

all: benchmark capacity plot visualize

# 1. Run the Structural Benchmark (Graph Types)
benchmark:
	@echo "Running Structural Benchmark..."
	$(PYTHON) advanced_benchmark.py

# 2. Run the Capacity Scaling Benchmark (3D)
capacity:
	@echo "Running Capacity Scaling Benchmark..."
	$(PYTHON) capacity_benchmark.py

# 3. Generate Plots
plot:
	@echo "Generating Plots..."
	$(PYTHON) plot_insane_graphs.py
	$(PYTHON) plot_capacity_2d.py

# 4. Generate Visual Proof
visualize:
	@echo "Generating Min-Cut Visualization..."
	$(PYTHON) visualize_theorem.py

# Clean up generated files
clean:
	@echo "Cleaning up..."
	rm -f *.csv *.png *.pkl
	find . -type d -name "__pycache__" -exec rm -rf {} +
