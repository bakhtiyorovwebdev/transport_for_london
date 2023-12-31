#Programme: task_3.py
#Authors: Charles Thomas, Roel-Junior Alejo Viernes, John Mendoza, Ma Johann Aniya Lugue
#Description: Follows the stance of task 2 using the Bellman_Ford Algorithm

from task_1 import read_data, histogram_generator, get_station_id, get_station_name
from task_2 import add_edges_to_graph

#These are the modules from the library code that we used
from adjacency_list_graph import AdjacencyListGraph #From Utlity Functions
from bellman_ford import bellman_ford #From Chapter x

def bellman_ford_start(graph, station_names):
    """
    This function runs bellman_ford's algorithm on the graph and returns the shortest path from the start station to all other stations.
    """

    start_stn = get_station_id(input("What station would you like to start at? "), station_names) # Get's the initial station from the user.
    _, pi, _ = bellman_ford(graph, start_stn)

    end_stn = input("What station would you like to end at? ")
    end_stn = get_station_id(end_stn, station_names)

    prev_stn = pi[end_stn]

    interim_stns = [end_stn]
    stop_counter = 0
    while prev_stn != start_stn:
        interim_stns.append(prev_stn)
        prev_stn = pi[prev_stn]
        stop_counter += 1
    
    interim_stns.append(start_stn)
    route = str([get_station_name(stn, station_names) for stn in reversed(interim_stns)][1:]).strip("[]").replace("'", "")
    return  (f"To get from {get_station_name(start_stn, station_names)} to {get_station_name(end_stn, station_names)}, you must travel through the following stations: {route[1:]} \
        This journey will bring you through {stop_counter} stops.")

        
if __name__ == "__main__":
    #These arrays are where the distance between the station pairs, the names of the stations and their respective lnes are stored   
    station_names, station_distances = read_data()
    graph = AdjacencyListGraph(len(station_names), directed = False, weighted = True) # Creates a graph with the number of stations as the number of vertices.
    add_edges_to_graph(station_distances, graph, station_names)

    print(bellman_ford_start(graph, station_names))
    histogram_generator(graph, "Number of stations")

