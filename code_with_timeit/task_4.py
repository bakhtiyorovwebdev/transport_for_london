import sys

sys.path.insert(0, 'libraries')

from adjacency_list_graph import *
import mst
import numpy as np
import dijkstra
import bellman_ford

time_entry = list()
station_entry = list()

def list_prep(list_name):
    data_set = list()
    for line in list_name:
        line = line.strip().split(",")
        while "" in line:
            line.remove("")
        data_set.append(line)
    return data_set
    
station_distances = []
station_names = []
def get_station_id(station_name):
    for i in range(len(station_names)):
        if station_names[i][0] == station_name:
            return i

with open ("data/London Underground Data (Elizabeth Line Update).csv", "r+") as data_set:
    data = data_set.readlines()
    data_set = list_prep(data)

    for line in data_set:

        if len(line) == 2:
            if not get_station_id(line[1]): #if station is not in station_names
                station_names.append((line[1], [line[0]])) # add to station names as (station, [lines])
            else: #else
                station_names[get_station_id(line[1])][1].append(line[0]) # append to lines list


        if len(line) == 4:
                station_distances.append(line[1:])
main_graph = AdjacencyListGraph(len(station_names), directed = False, weighted = True)

def get_station_name(id):
    return station_names[id][0]

def add_edges_to_graph():
    """
    This function adds the stations to the graph.
    """
    for edge in station_distances:
        station1 = get_station_id(edge[0])
        station2 = get_station_id(edge[1])
        distance = int(1)

        if not main_graph.has_edge(station1, station2):
            main_graph.insert_edge(station1, station2, distance)

def mst_treeing(graph):
    """
    This function runs Prim's algorithm on the graph and returns the minimum spanning tree.
    """
    tree = mst.prim(graph, 0)
    
    names = tree.strmap(lambda i: station_names[i][0])

    tree = tree.get_edge_list()

    return tree

def find_severed_edges():

    global results
    results = []

    difference = set(main_graph.get_edge_list()) - set(mst_treeing(main_graph))

    for e1, e2 in difference:
        results.append(get_station_name(e1) + " -- " + get_station_name(e2))
    return results

def ui_sever(start, end):

    start_stn = (start + " -- " + end)

    if start_stn in results:
        print (f"Yes you will be able to sever {start_stn}.")
    
    else:
        print (f"You will not be able to sever {start_stn} as it would result in a disconnected graph.")

        
if __name__ == "__main__":

    raw_station_names = [station[0] for station in station_names]
    import timeit, random

    add_edges_to_graph()

    print(find_severed_edges())

    def timer():
        find_severed_edges()
        station_a = random.choice(raw_station_names)
        station_b = random.choice(raw_station_names)

        if station_a == station_b:
            station_b = random.choice(raw_station_names)
        ui_sever(station_a, station_b)

    print(timeit.timeit(timer, number = 10000))

