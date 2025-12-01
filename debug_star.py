
import time
from graph_generator import star_of_stars
from push_relabel import push_relabel
import sys

sys.setrecursionlimit(30000)

def run_test():
    N_VALUES = [200, 400, 600, 800, 1000]
    print(f"{'Input N':<10} | {'Actual N':<10} | {'Branches':<10} | {'Size':<10} | {'Time (s)':<15}")
    print("-" * 65)

    for n in N_VALUES:
        branches = max(10, n // 40)
        branch_size = max(10, n // 40)
        g = star_of_stars(branches, branch_size, cap=50)
        s, t = 0, g.n - 1
        
        start = time.perf_counter()
        flow = push_relabel(g, s, t)
        end = time.perf_counter()
        
        print(f"{n:<10} | {g.n:<10} | {branches:<10} | {branch_size:<10} | {end - start:.6f}")

if __name__ == "__main__":
    run_test()
