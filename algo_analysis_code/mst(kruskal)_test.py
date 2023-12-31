import sys, timeit

sys.path.insert(0, 'libraries')

import generate_random_graph, mst
import matplotlib.pyplot as plt

def graph_maker(input_size):
    test_graph = generate_random_graph.generate_random_graph(input_size, 0.1, by_adjacency_lists=True, directed=False, weighted=True, min_weight=0, max_weight=10)
    return test_graph


if __name__ == "__main__":
    times = []
    sizes = list(range(1, 100))

    for i in sizes:
        main_graph = graph_maker(i)
        times.append(timeit.timeit(lambda: mst.kruskal(main_graph), number=1))
    plt.plot(sizes, times)
    plt.title("Minimum Spanning Tree (Kruskal's Algorithm)")
    plt.xlabel("Input Size")
    plt.ylabel("Time (s)")
    plt.show()


