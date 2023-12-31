#Programme Name: task_1.py
#Authors: Charles Thomas, Roel-Junior Alejo Viernes, John Mendoza, Ma Johann Aniya Lugue
#Summary: Find's the quickest eoute between two stations using Dijkstra's algorithm.

import sys
import matplotlib.pyplot as plt

sys.path.insert(0, 'libraries')

#These are the modules from the library code that we used
from adjacency_list_graph import AdjacencyListGraph #From /Utility Functions
from dijkstra import dijkstra #From Chapter 22
import johnson #From Chapter 23

def list_prep(list_name):
    """
    This function prepares the data set by removing empty strings and splitting the data set into a list of lists.
    """
    data_set = list()
    for line in list_name:
        line = line.strip().split(",")
        while "" in line:
            line.remove("")
        data_set.append(line)
    return data_set

def get_station_id(station_name, station_names):
    """
    This function returns the station id given the station name.
    """
    for i in range(len(station_names)):
        if station_names[i][0] == station_name: #if the station name within the station array is matched, return it's indexed number
            return i

def read_data():
    station_names = []
    station_distances = []

    with open ("data/London Underground Data (Elizabeth Line Update).csv", "r+") as data_set:
        """
        This is where the data from the spreadsheet is collected and stored within their respective areas
        """
        
        data = list_prep(data_set.readlines())

        for line in data:

            if len(line) == 2:
                if not get_station_id(line[1], station_names): #if station is not in station_names
                    station_names.append((line[1], [line[0]])) # add to station names as (station, [lines])
                else: #else
                    station_names[get_station_id(line[1], station_names)][1].append(line[0]) # append to lines list

            if len(line) == 4:
                    station_distances.append(line[1:]) # append to station distances as (station1, station2, distance)
    return station_names, station_distances

def get_station_name(id, station_names):
    """
    This function returns the name of the station given the station id.
    """
    return station_names[id][0]

def add_edges_to_graph(edges, graph, station_names):
    """
    This function adds the stations to the graph.
    """
    for edge in edges:
        station1 = get_station_id(edge[0], station_names) #Collects the id of the first station
        station2 = get_station_id(edge[1], station_names) #Collects the id of the second station

        if not graph.has_edge(station1, station2):
            graph.insert_edge(station1, station2, int(edge[2]))   # Adds the edge to the graph. 

def histogram_generator(graph, xlabel):
    """
    This function generates a histogram of all the station pairs in the data set
    """


    times = johnson.johnson(graph) # Run the Johnson algorithm on the graph
    size = len(times) # Get the size of the matrix (number of stations)
    results = [] # Array to store the times
    for i in range(size): # Loop through every station
        for j in range(i + 1, size): # Start from i + 1 to avoid dupliacate
            results.append(times[i][j])
    

    plt.hist(results, bins = 15)
    plt.xlabel(xlabel)
    plt.ylabel("Frequency")
    plt.title(f"Histogram of all the station pairs")
    plt.show()

def dijkstra_times(graph, station_names):
    """
    This function runs dijkstra's algorithm on the graph and returns the shortest path from the start station to all other stations.
    """
    start_stn = get_station_id(input("What station would you like to start at? "), station_names) # Get's the initial station from the user.
    d, pi = dijkstra(graph, start_stn) # Runs dijkstra's algorithm on the graph.

    end_stn = get_station_id(input("What station would you like to end at? "), station_names)

    prev_stn = pi[end_stn]
    stop_counter = 0

    interim_stns = [end_stn]
    while prev_stn != start_stn:
        interim_stns.append(prev_stn)
        prev_stn = pi[prev_stn]
        stop_counter += 1
    interim_stns.append(start_stn)
    route = str([get_station_name(stn, station_names) for stn in reversed(interim_stns)][1:]).strip("[]").replace("'", "")
    return  (f"To get from {get_station_name(start_stn, station_names)} to {get_station_name(end_stn, station_names)}, you must travel through the following stations: {route}. \
This journey will take {d[end_stn]} minutes and bring you through {stop_counter} stops.")

if __name__ == "__main__":
    #These arrays are where the distance between the station pairs, the names of the stations and their respective lnes are stored   
    station_names, station_distances = read_data()
    graph = AdjacencyListGraph(len(station_names), directed = False, weighted = True) # Creates a graph with the number of stations as the number of vertices.
    add_edges_to_graph(station_distances, graph, station_names)

    print(dijkstra_times(graph, station_names))
    histogram_generator(graph, "Time (minutes)")