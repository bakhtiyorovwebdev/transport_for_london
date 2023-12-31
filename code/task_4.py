from task_1 import read_data, histogram_generator, get_station_name, add_edges_to_graph
from task_2 import add_edges_to_graph as add_edges_to_graph2

from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal

def find_severed_edges(graph, tree, station_names):
    """
    Finds stations which, if severed, would result in a disconnected graph (using set Notation)
    """
    results = []

    difference = set(graph.get_edge_list()) - set(tree.get_edge_list())

    for e1, e2 in difference:
        results.append(get_station_name(e1, station_names) + " -- " + get_station_name(e2, station_names))
    return results

def ui_sever(results):
    """
    Asks the user which stations they would like to assess and returns whether they can be severed or not.
    """

    formatted_results = str(results).strip("[]").replace("'", "")

    print (f"Here are the stations that can be severed: {formatted_results}")
    start_stn, end_stn = input("Which stations would you like to assess? (Input it in the form 'Station1 and Station2')").split(" and ")
    combined = start_stn + " -- " + end_stn

    if combined in results or end_stn + " -- " + start_stn in results:
        return f"Yes you will be able to sever {combined}."
    
    else:
        return "You will not be able to sever these stations as it would result in a disconnected graph."

        
if __name__ == "__main__":
    #These arrays are where the distance between the station pairs, the names of the stations and their respective lnes are stored   
    station_names, station_distances = read_data()
    graph = AdjacencyListGraph(len(station_names), directed = False, weighted = True) # Creates a graph with the number of stations as the number of vertices.
    add_edges_to_graph(station_distances, graph, station_names)
    
    tree = kruskal(graph)
    results = find_severed_edges(graph, tree, station_names) # Finds the severed edges
    print(ui_sever(results)) # Asks the user which stations they would like to assess and returns whether they can be severed or not.

    histogram_generator(tree, "Time (minutes)")