import sys

sys.path.insert(0, 'libraries')

from adjacency_list_graph import *
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

def bellman_ford_start(graph):
    """
    This function runs bellman_ford's algorithm on the graph and returns the shortest path from the start station to all other stations.
    """
    start_stn = get_station_id(input("What station would you like to start at? ")) # Get's the initial station from the user.
    d, pi, cycle = bellman_ford.bellman_ford(graph, start_stn) 
    print("No negative-weight cycle:", cycle) # Runs bellman_ford's algorithm on the graph.

    end_stn = input("What station would you like to end at? ")
    end_stn = get_station_id(end_stn)

    prev_stn = pi[end_stn]

    interim_stns = [end_stn]
    while prev_stn != start_stn:
        interim_stns.append(prev_stn)
        prev_stn = pi[prev_stn]
    interim_stns.append(start_stn)
    route = [get_station_name(stn) for stn in reversed(interim_stns)]
    return  (f"To get from {get_station_name(start_stn)} to {get_station_name(end_stn)}, you must travel through the following stations: {route} \
        This journey will bring you through {len(route)} stops.")

        
if __name__ == "__main__":

    add_edges_to_graph()

    print (main_graph.strmap(lambda i: station_names[i][0]))

    print(bellman_ford_start(main_graph))

