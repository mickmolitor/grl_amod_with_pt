import csv
from datetime import timedelta
import os
from params.program_params import Mode, ProgramParams
from playground.graph_sage_test import test_graph_sage
from program.execution import execute_graph_reinforcement_learning
from program.grid.grid import Grid
from program.order.orders import Orders
from program.state.state import State
from program.vehicle.vehicles import Vehicles
from static_data_generation.public_transport_graph_creation import generate_shortest_paths_graph
from static_data_generation.vehicle_data_initialization import initialize_vehicle_positions
from static_data_generation.zone_graph_creation import create_zone_graph, fix_zone_graph
from visualization.visualize_vehicle_positions import visualize_vehicle_positions
from visualization.visualize_graph import visualize_zone_graph

def grl_train_and_test():
    initialize_vehicle_positions()
    # Train the algorithm On-Policy
    for i in range(14):
        execute_graph_reinforcement_learning()
        Orders.reset()
        State.reset()
        ProgramParams.SIMULATION_DATE += timedelta(1)
    # Testing
    Vehicles.raze_vehicles()
    initialize_vehicle_positions()
    # Test the algorithm On-Policy
    for i in range(7):
        execute_graph_reinforcement_learning()
        Orders.reset()
        State.reset()
        ProgramParams.SIMULATION_DATE += timedelta(1)

# Read program params
if os.path.isfile("execution/program_params.csv"):
    with open("execution/program_params.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ProgramParams.set_member(row["parameter"], row["value"])
# Read execution file
if os.path.isfile("execution/run.csv"):
    with open("execution/run.csv", mode="r") as file:
        reader = csv.DictReader(file)
        if reader.__next__()["Command"] == "grl":
            ProgramParams.EXECUTION_MODE = Mode.GRAPH_REINFORCEMENT_LEARNING
            if reader.__next__()["Command"] == "train_and_test":
                grl_train_and_test()


while True:
    user_input = input(
        "Which menu you want to enter? (Graph Reinforcement Learning -> 1, Baseline Performance -> 2, Static Data Generation -> 3, Visualization -> 4, Data Analysis -> 5) "
    )
    if user_input == "1":
        ProgramParams.EXECUTION_MODE = Mode.GRAPH_REINFORCEMENT_LEARNING
        while True:
            user_input = input(
                "Which script do you want to start? (Online Training and Testing -> 1, Start Graph Reinforcement Learning (one day) -> 2) "
            )
            if user_input == "1":
                grl_train_and_test()
                break
            if user_input == "2":
                initialize_vehicle_positions()
                execute_graph_reinforcement_learning()
                break
            else:
                print("This option is not allowed. Please try again.")
        break

    elif user_input == "2":
        # while True:
        #     ProgramParams.EXECUTION_MODE = Mode.BASELINE_PERFORMANCE
        #     user_input = input(
        #         "Which script do you want to start? (Offline Policy Evaluation -> 1, Online Training -> 2, Start DRL (one day) -> 3) "
        #     )
        #     if user_input == "1":
        #         initialize_driver_positions()
        #         # Train the ope networks with online data
        #         for i in range(14):
        #             train_ope()
        #             Order.reset()
        #             State.reset()
        #             ProgramParams.SIMULATION_DATE += timedelta(1)
        #         break
        #     elif user_input == "2":
        #         initialize_driver_positions()
        #         # Train the algorithm On-Policy
        #         # You have to set the date in program_params on the Date you want (old date + train duration)
        #         for i in range(7):
        #             start_drl()
        #             Order.reset()
        #             State.reset()
        #             ProgramParams.SIMULATION_DATE += timedelta(1)
        #         break
        #     elif user_input == "3":
        #         start_drl()
        #         break
        #     else:
        #         print("This option is not allowed. Please try again.")
        break

    elif user_input == "3":
        while True:
            user_input = input(
                "Which script do you want to start? (Create Zone Graph -> 1, Create Public Transport Graph -> 2) "
            )
            if user_input == "1":
                create_zone_graph()        
                break
            if user_input == "2":
                generate_shortest_paths_graph()
                break
            else:
                print("This option is not allowed. Please try again.")
        break

    elif user_input == "4":
        while True:
            user_input = input(
                "Which script do you want to start? (Visualize Zone Graph -> 1, Visualize vehicle positions -> 2) "
            )
            if user_input == "1":
                visualize_zone_graph()
                break
            elif user_input == "2":
                visualize_vehicle_positions()
                break
            else:
                print("This option is not allowed. Please try again.")
        break

    # elif user_input == "6":
    #     while True:
    #         user_input = input(
    #             "Which script do you want to start? (Analyse trip data (data_analysis.py need to be adapted[date and folder structure]) -> 1) "
    #         )
    #         if user_input == "1":
    #             analyse_trip_data()
    #             break
    #         else:
    #             print("This option is not allowed. Please try again.")
    #     break

    else:
        print("This option is not allowed. Please try again.")