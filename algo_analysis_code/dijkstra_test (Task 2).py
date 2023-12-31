print("Running dijkstra_test.py")
import sys, timeit

sys.path.insert(0, 'libraries')

import generate_random_graph, dijkstra
import numpy as np
import matplotlib.pyplot as plt

def graph_maker(input_size):
    test_graph = generate_random_graph.generate_random_graph(input_size, 0.1, by_adjacency_lists=True, directed=False, weighted=True, min_weight=1, max_weight=1)
    return test_graph

if __name__ == "__main__":
    times = []
    sizes = list(range(1, 100))

    for i in sizes:
        main_graph = graph_maker(i)
        times.append(timeit.timeit(lambda: dijkstra.dijkstra(main_graph, 0), number=1))
    plt.plot(sizes, times)
    plt.title("Dijkstra's Algorithm (Task 2)")
    plt.xlabel("Input Size")
    plt.ylabel("Time (s)")
    plt.show()
