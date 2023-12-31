#Programme Name: task_1.py
#Authors: Charles Thomas, Roel-Junior Alejo Viernes, John Mendoza, Ma Johann Aniya Lugue
#Summary: Find's the quickest 
import sys
import matplotlib.pyplot as plt

sys.path.insert(0, 'libraries')

from adjacency_list_graph import *
import dijkstra
import johnson

time_entry = list()
station_entry = list()

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
    
station_distances = []
station_names = []

def get_station_id(station_name):
    """
    This function returns the station id given the station name.
    """
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
                station_distances.append(line[1:]) # append to station distances as (station1, station2, distance)

main_graph = AdjacencyListGraph(len(station_names), directed = False, weighted = True) # Creates a graph with the number of stations as the number of vertices.

def get_station_name(id):
    """
    This function returns the name of the station given the station id.
    """
    return station_names[id][0]

def add_edges_to_graph():
    """
    This function adds the stations to the graph.
    """
    for edge in station_distances: 
        station1 = get_station_id(edge[0])
        station2 = get_station_id(edge[1])

        if not main_graph.has_edge(station1, station2):
            main_graph.insert_edge(station1, station2, int(edge[2]))   # Adds the edge to the graph. 


def get_distance(start_id, end_id, graph):
    """
    Gets rekt
    """
    d, _ = dijkstra.dijkstra(graph, start_id) # Runs dijkstra's algorithm on the graph.

    return d[end_id]



def histogram_generator():
    """
    This function generates a histogram of all the station pairs in the data set
    """


    times = [y for x in johnson.johnson(main_graph) for y in x]
    

    plt.hist(times, bins = 25)
    plt.xlabel("Time (minutes)")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of all the station pairs")
    plt.show()




def dijkstra_start(graph, start, end):
    """
    This function runs dijkstra's algorithm on the graph and returns the shortest path from the start station to all other stations.
    """
    start_stn = get_station_id(start) # Get's the initial station from the user.
    d, pi = dijkstra.dijkstra(graph, start_stn) # Runs dijkstra's algorithm on the graph.

    end_stn = (get_station_id(end))

    prev_stn = pi[end_stn]

    interim_stns = [end_stn]


    while prev_stn != start_stn:
        interim_stns.append(prev_stn)# Adds the previous station to the list of stations.
        prev_stn = pi[prev_stn]# Gets the previous station from the pi map.

    interim_stns.append(start_stn)# Adds the start station to the list of stations.
    route = [get_station_name(stn) for stn in reversed(interim_stns)]# Reverses the list of stations and gets the station names.


    return  (f"To get from {get_station_name(start_stn)} to {get_station_name(end_stn)}, you must travel through the following stations: {route[1:]} \
        This journey will take {d[end_stn]} minutes.")

        
if __name__ == "__main__":


    raw_station_names = [station[0] for station in station_names]
    import timeit, random
    add_edges_to_graph()

    def time_dijkstra():

        station_a = random.choice(raw_station_names)
        station_b = random.choice(raw_station_names)

        if station_a == station_b:
            station_b = random.choice(raw_station_names)
        dijkstra_start(main_graph, station_a, station_b)

    print(timeit.timeit(time_dijkstra, number = 1))

    histogram_generator()


