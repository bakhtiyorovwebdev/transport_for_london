#Program Name: task_2.py
#Authors: Charles Thomas, Roel-Junior Alejo Viernes, John Mendoza, Ma Johann Aniya Lugue
#Description: Follows the stance of task 1 where all weights are 1

from task_1 import read_data, histogram_generator, get_station_id, get_station_name

#These are the modules from the library code that we used
from adjacency_list_graph import AdjacencyListGraph
import dijkstra #From Chapter x

def add_edges_to_graph(edges, graph, station_names):
    """
    This function adds the stations to the graph.
    """
    for edge in edges: 
        station1 = get_station_id(edge[0], station_names) #Collects the id of the first station
        station2 = get_station_id(edge[1], station_names) #Collects the id of the second station
        distance = int(1) # the distance between each station

        if not graph.has_edge(station1, station2):
            graph.insert_edge(station1, station2, distance)   # Adds the edge to the graph. 

def dijkstra_stops(graph, station_names):
    """
    This function runs dijkstra's algorithm on the graph and returns the shortest path from the start station to all other stations.
    """

    start_stn = input("What station would you like to start at? ") # Get's the initial station from the user.
    start_stn = get_station_id(start_stn, station_names) # Gets the station id from the station name.
    d, pi = dijkstra.dijkstra(graph, start_stn) # Runs dijkstra's algorithm on the graph.

    end_stn = get_station_id(input("What station would you like to end at? "), station_names)

    prev_stn = pi[end_stn]

    interim_stns = [end_stn]
    while prev_stn != start_stn:
        interim_stns.append(prev_stn)
        prev_stn = pi[prev_stn]
    
    interim_stns.append(start_stn)
    route = str([get_station_name(stn, station_names) for stn in reversed(interim_stns)][1:]).strip("[]").replace("'", "")
    return  (f"To get from {get_station_name(start_stn, station_names)} to {get_station_name(end_stn, station_names)}, you must travel through the following stations: {route}. \
This journey will bring you through {d[end_stn] + 1} stops.")

        
if __name__ == "__main__":
    #These arrays are where the distance between the station pairs, the names of the stations and their respective lnes are stored   
    station_names, station_distances = read_data()
    graph = AdjacencyListGraph(len(station_names), directed = False, weighted = True) # Creates a graph with the number of stations as the number of vertices.
    add_edges_to_graph(station_distances, graph, station_names)

    print(dijkstra_stops(graph, station_names))
    histogram_generator(graph, "Number of intermediate stations")
