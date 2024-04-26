from collections import deque, namedtuple
import csv
import math
from params.program_params import ProgramParams
from program.logger import LOGGER

# This file generates the fastest connection public transit network only
# This is a Dijkstra algorithm. For a faster solution use the Floyd-Warshall algorithm to solve the all-pair shortest path problem (see code/model_builder)
Edge = namedtuple("Edge", "start, end, cost")

def create_edge(start, end, cost):
    return Edge(start, end, cost)

class Graph:
    def __init__(self, edges):
        self.edges = [create_edge(*e) for e in edges]

    def vertices(self): 
        return set(e.start for e in self.edges).union(e.end for e in self.edges)
    
    def get_neighbours(self, v):
        neighbours = []
        for e in self.edges:
            if e.start == v:
                neighbours.append((e.end, e.cost))
        return neighbours

    def dijkstra(self, source, destination): 
        distances = {v: float("inf") for v in self.vertices()} # each node gets a distance of infinity
        prev_v = {v: None for v in self.vertices()} # each node gets a predecessor of None

        distances[source] = 0 # the distance of the start node is set to 0
        vertices = list(self.vertices())[:]
        while len(vertices) > 0:
            v = min(vertices, key=lambda u: distances[u]) # the node with the smallest distance is selected
            vertices.remove(v) # the node is removed from the list
            if distances[v] == float("inf"):
                break # if the distance of the node is infinite, then there is no path to the destination node
            for neighbour, cost in self.get_neighbours(v):
                path_cost = distances[v] + cost # the distance of the neighbor is calculated
                if path_cost < distances[neighbour]:
                    distances[neighbour] = path_cost
                    prev_v[neighbour] = v
        path = []
        curr_v = destination
        while curr_v and prev_v[curr_v] is not None:
            path.insert(0, curr_v)
            curr_v = prev_v[curr_v] # the predecessor of the node becomes the current node
        if curr_v:
            path.insert(0, curr_v)
        return path, distances[destination]

###############################################################################

def lat_lon_to_meters(lat1, lon1, lat2, lon2):
    # Conversion factors
    meters_per_degree_lat = 111000  # approximately 111 kilometers per degree
    meters_per_degree_lon = meters_per_degree_lat * math.cos(math.radians((lat1 + lat2) / 2))

    # Conversion to meters
    delta_lat_meters = (lat1 - lat2) * meters_per_degree_lat
    delta_lon_meters = (lon1 - lon2) * meters_per_degree_lon

    return delta_lat_meters, delta_lon_meters

def manhattan_distance(lat1, lon1, lat2, lon2):
    delta_lat_meters, delta_lon_meters = lat_lon_to_meters(lat1, lon1, lat2, lon2)
    return abs(delta_lat_meters) + abs(delta_lon_meters)

###############################################################################

def read_csv_data(filename):
    data = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append((int(row["ID"]), row["station_name"], row["line"], float(row["LAT"]), float(row["LONG"])))
    return data

###############################################################################

def create_edges(data):
    edges = []
    station_duration = ProgramParams.STATION_DURATION # Set the value for Station_Duration here
    transfer_same_station = ProgramParams.TRANSFER_SAME_STATION  # Set the value for Transfer_Same_Station here
    max_walking_duration = ProgramParams.MAX_WALKING_DURATION
    walking_speed = ProgramParams.WALKING_SPEED 
    
    # Count variables for the different types of edges
    line_edges_count = 0
    transfer_edges_count = 0
    remaining_edges_count = 0

    # Helper functions and structures
    id_to_name = {station_id: stop_name for station_id, stop_name, _ , _, _ in data}
    name_to_ids = {}
    for station_id, stop_name, _, _, _ in data:
        if stop_name not in name_to_ids:
            name_to_ids[stop_name] = []
        name_to_ids[stop_name].append(station_id)

    # Edges for the same line
    for i in range(len(data) - 1):
        id1, name1, line1, lat1, lon1 = data[i]
        id2, name2, line2, lat2, lon2 = data[i + 1]
        if line1 == line2:
            edges.append((id1, id2, station_duration))
            edges.append((id2, id1, station_duration))
            line_edges_count += 1

    # Edges for transfers at the same station
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            id1, name1, line1, lat1, lon1 = data[i]
            id2, name2, line2, lat2, lon2 = data[j]
            if name1 == name2 and line1 != line2:
                edges.append((id1, id2, transfer_same_station))
                edges.append((id2, id1, transfer_same_station))
                transfer_edges_count += 1
    
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            id1, name1, line1, lat1, lon1 = data[i]
            id2, name2, line2, lat2, lon2 = data[j]
            distance = manhattan_distance(lat1, lon1, lat2, lon2)
            cost = distance * walking_speed  # Calculation of costs

            if cost < max_walking_duration and not (line1 == line2 or name1 == name2):
                edges.append((id1, id2, cost))
                edges.append((id2, id1, cost))
                remaining_edges_count += 1

    LOGGER.info(f"Number of edges within the same line: {line_edges_count}")
    LOGGER.info(f"Number of edges for transfers at the same station: {transfer_edges_count}")
    LOGGER.info(f"Number of remaining edges: {remaining_edges_count}")
    return edges

# calculation of shortest paths
def calculate_shortest_paths(graph, nodes):
    paths = []
    for i, start_node in enumerate(nodes):
        for j, end_node in enumerate(nodes):
            if i*j % (len(nodes)*len(nodes)*0.05) == 0:
                LOGGER.info(f"{i*j} of {len(nodes)*len(nodes)} ({i*j // (len(nodes)*len(nodes)*0.05)}%) shortest paths calculated.")
            if start_node != end_node:
                shortest_path = graph.dijkstra(start_node, end_node)
                paths.append((start_node, end_node, shortest_path))
    return paths

def save_paths_to_csv(paths, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["start_station", "end_station", "connection"])
        for start, end, path in paths:
            writer.writerow([start, end, " -> ".join(map(str, path))])



def generate_shortest_paths_graph():
    station_data = read_csv_data("data/continuous_subway_data.csv")
    station_data.sort(key=lambda x: x[0])
    edges = create_edges(station_data)
    graph = Graph(edges)

    nodes = list(graph.vertices())  # List of all nodes (stations)
    shortest_paths = calculate_shortest_paths(graph, nodes)
    LOGGER.info("Saving begins")
    save_paths_to_csv(shortest_paths, "data/shortest_paths.csv")
