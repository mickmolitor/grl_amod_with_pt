import time
from program.action.action import Action
from program.action.vehicle_action_pair import VehicleActionPair
from program.interval.time_series import TimeSeries
from params.program_stats import ProgramStats
from program.public_transport.station import Station
from program.vehicle.vehicle import Vehicle
from program.logger import LOGGER
from program.state.state import State
import numpy as np
from ortools.graph.python import min_cost_flow

# Solve the bipartite matching problem as a min-cost-flow problem to use the efficient C++ solver
def or_tools_min_cost_flow(vehicle_action_pairs: list[VehicleActionPair]) -> list[tuple[Vehicle, Action]]:

    if len(vehicle_action_pairs) == 0:
        LOGGER.debug("No available vehicles. Skip matching phase")
        return []

    start_time = time.time()
    smcf = min_cost_flow.SimpleMinCostFlow()
    edge_sum = 0

    # 1. Calculate how many edges and nodes we totally have, create mappers to indices
    pair_to_index = {vehicle_action_pairs[i]: i for i in range(len(vehicle_action_pairs))}
    edge_sum += len(pair_to_index)
    # Route -> Order
    route_order_set = set()
    for pair in vehicle_action_pairs:
        if pair.action.is_route():
            if (pair.action, pair.action.route.order) not in route_order_set:
                route_order_set.add((pair.action, pair.action.route.order))
    route_order_list = list(route_order_set)
    del route_order_set
    route_order_to_index = {
        route_order_list[i - edge_sum]: i
        for i in range(edge_sum, edge_sum + len(route_order_list))
    }
    edge_sum += len(route_order_list)

    # Route -> T-Node
    order_t_set = set()
    for tup in route_order_list:
        order_t_set.add(tup[1])
    order_t_list = list(order_t_set)
    del order_t_set
    order_t_to_index = {
        order_t_list[i - edge_sum]: i for i in range(edge_sum, edge_sum + len(order_t_list))
    }
    edge_sum += len(order_t_list)

    # Idling -> T-Node
    idling_t_index = edge_sum
    edge_sum += 1

    node_sum = 0
    # Nodes
    # Vehicles
    vehicle_set = set()
    for pair in vehicle_action_pairs:
        vehicle_set.add(pair.vehicle)
    vehicle_list = list(vehicle_set)
    del vehicle_set
    vehicle_to_index = {vehicle_list[i]: i for i in range(0, len(vehicle_list))}
    node_sum += len(vehicle_list)

    # Actions
    action_set = set()
    idling_node = None
    for pair in vehicle_action_pairs:
        if pair.action.is_idling():
            idling_node = pair.action
        action_set.add(pair.action)
    action_list = list(action_set)
    del action_set
    action_to_index = {
        action_list[i - node_sum]: i for i in range(node_sum, node_sum + len(action_list))
    }
    idling_to_index = action_to_index[idling_node]
    node_sum += len(action_list)

    # Orders
    order_to_index = {order_t_list[i - node_sum]: i for i in range(node_sum, node_sum + len(order_t_list))}
    node_sum += len(order_to_index)
    t_to_index = node_sum
    node_sum += 1

    # 2. Create arrays for edge and node definitions
    # Edges
    start_nodes = [0 for i in range(edge_sum)]
    end_nodes = [0 for i in range(edge_sum)]
    capacities = [1 for i in range(edge_sum)]
    weights = [0 for i in range(edge_sum)]
    for pair in pair_to_index:
        start_nodes[pair_to_index[pair]] = vehicle_to_index[pair.vehicle]
        end_nodes[pair_to_index[pair]] = action_to_index[pair.action]
        capacities[pair_to_index[pair]] = 1
        weights[pair_to_index[pair]] = pair.weight*(-1)
    
    for tup in route_order_to_index:
        start_nodes[route_order_to_index[tup]] = action_to_index[tup[0]]
        end_nodes[route_order_to_index[tup]] = order_to_index[tup[1]]
    
    for order in order_t_to_index:
        start_nodes[order_t_to_index[order]] = order_to_index[order]
        end_nodes[order_t_to_index[order]] = t_to_index
    
    start_nodes[idling_t_index] = idling_to_index
    end_nodes[idling_t_index] = t_to_index
    capacities[idling_t_index] = len(vehicle_list)

    start_arr = np.array(start_nodes)
    end_arr = np.array(end_nodes)
    capacities_arr = np.array(capacities)
    weights_arr = np.array(weights)

    # Nodes
    supplies = [0 for i in range(node_sum)]
    for vehicle in vehicle_to_index:
        supplies[vehicle_to_index[vehicle]] = 1
    
    supplies[t_to_index] = len(vehicle_to_index) * (-1)
    
    # 3. Fill the model
    # Add arcs, capacities and costs in bulk using numpy.
    all_arcs = smcf.add_arcs_with_capacity_and_unit_cost(
        start_arr, end_arr, capacities_arr, weights_arr
    )

    #LOGGER.debug(all_arcs)

    # Add supply for each nodes.
    smcf.set_nodes_supplies(np.arange(0, len(supplies)), supplies)

    medium_time = time.time()

    # 4. Solve
    # Find the min cost flow.
    status = smcf.solve()
    end_time = time.time()
    if status != smcf.OPTIMAL:
        LOGGER.error("There was an issue with the min cost flow input.")
        LOGGER.error(f"Status: {status}")
        exit(1)
    LOGGER.debug(
        f"The calculation took {round((end_time - medium_time)*1000,4)} ms, while preparation took {round((medium_time - start_time)*1000,4)} ms")
    ########################################################################################
    LOGGER.debug(f"Minimum cost: {smcf.optimal_cost()}")

    solution_flows = smcf.flows(all_arcs)
    
    matches = list(filter(lambda pair: solution_flows[pair_to_index[pair]] == 1, vehicle_action_pairs))
    ProgramStats.SUM_OF_TIMESAFE += sum(list(map(lambda pair: pair.action.route.time_reduction, filter(lambda pair: pair.action.is_route(), matches))))
    LOGGER.debug(f"Sum of timesafe: {ProgramStats.SUM_OF_TIMESAFE}")

    hours = (State.get_state().current_time.to_total_minutes() - TimeSeries.get_instance().start_time.to_total_minutes()) / 60
    hours = hours if hours > 0.1 else 0.1
    LOGGER.debug(f"Sum of timesafe per car, per hour, in minutes: {ProgramStats.SUM_OF_TIMESAFE / len(vehicle_list) / hours / 60}")
    return matches

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import floyd_warshall

# Use the Floyd-Warshall algorithm to solve the all-pair shortest path problem
# Input undirected edges as tuples [station1, weight, station2]
def solve_all_pair_shortest_path_problem(connections: list[tuple[Station, float, Station]]) -> dict[int, dict[int, tuple[list[Station], float]]]:
    # Build a dict containing all stations mapped by their id
    station_id_dict = {}
    for connection in connections:
        station1 = connection[0]
        station2 = connection[2]

        if station1.id not in station_id_dict:
            station_id_dict[station1.id] = station1
        if station2.id not in station_id_dict:
            station_id_dict[station2.id] = station2
    
    # Create Mapper from station id -> index and other direction in graph matrix 
    sorted_station_ids = sorted(station_id_dict.keys())
    index_to_id_dict = {i: sorted_station_ids[i] for i in range(len(sorted_station_ids))}
    id_to_index_dict = {sorted_station_ids[i]: i for i in range(len(sorted_station_ids))}

    graph = [[0 for i in range(len(sorted_station_ids))] for j in range(len(sorted_station_ids))]

    # Fill connections in graph
    for connection in connections:
        graph[id_to_index_dict[connection[0].id]][id_to_index_dict[connection[2].id]] = connection[1]
    
    # Convert graph to network
    graph = csr_matrix(graph)

    # Solve the problem
    dist_matrix, predecessors = floyd_warshall(csgraph=graph, directed=False, return_predecessors=True)

    result_dict = {id: {id2: None for id2 in sorted_station_ids} for id in sorted_station_ids}
    LOGGER.debug(type(dist_matrix))
    for idx1 in range(len(dist_matrix)):
        for idx2 in range(len(dist_matrix)):
            idx = predecessors[idx1][idx2]
            station1 = station_id_dict[index_to_id_dict[idx1]]
            station2 = station_id_dict[index_to_id_dict[idx2]]

            if idx == -9999:
                del result_dict[station1.id][station2.id]
                continue
            
            stations = [station1]
            while idx != idx1:
                stations.append(station_id_dict[index_to_id_dict[idx]])
                idx = predecessors[idx1][idx]
            stations.append(station2)
            

            result_dict[station1.id][station2.id] = (stations, dist_matrix[idx1][idx2])
    
    return result_dict
