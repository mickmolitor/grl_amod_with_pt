from params.program_params import Mode, ProgramParams
from playground.graph_sage_test import test_graph_sage
from program.grid.grid import Grid
from static_data_generation.public_transport_graph_creation import generate_shortest_paths_graph
from static_data_generation.zone_graph_creation import create_zone_graph, fix_zone_graph
from visualization.visualize_graph import visualize_zone_graph


# Orders einlesen
# State aktualisieren
# Grid Embedding
# Routen und Pairs berechnen
# State updaten
# relocations
# state value updaten

while True:
    user_input = input(
        "Which menu you want to enter? (Graph Reinforcement Learning -> 1, Baseline Performance -> 2, Static Data Generation -> 3, Visualization -> 4, Data Analysis -> 5) "
    )
    if user_input == "1":
        # ProgramParams.EXECUTION_MODE = Mode.GRAPH_REINFORCEMENT_LEARNING
        # while True:
        #     user_input = input(
        #         "Which script do you want to start? (Online Training and Testing -> 1, Start Q-Learning (one day)-> 2) "
        #     )
        #     if user_input == "1":
        #         StateValueTable.get_state_value_table().raze_state_value_table()
        #         initialize_driver_positions()
        #         # Train the algorithm On-Policy
        #         for i in range(14):
        #             start_q_learning()
        #             Order.reset()
        #             State.reset()
        #             ProgramParams.SIMULATION_DATE += timedelta(1)
        #         # Testing
        #         Drivers.raze_drivers()
        #         initialize_driver_positions()
        #         # Test the algorithm On-Policy
        #         for i in range(7):
        #             start_q_learning()
        #             Order.reset()
        #             State.reset()
        #             ProgramParams.SIMULATION_DATE += timedelta(1)
        #         break
        #     if user_input == "2":
        #         start_q_learning()
        #         break
        #     else:
        #         print("This option is not allowed. Please try again.")
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
        # while True:
        #     user_input = input(
        #         "Which script do you want to start? (Grid Cell Creation -> 1, Generate Trajectories -> 2, Remove Idle Trajectories -> 3, Initialize Drivers -> 4, Discretize days -> 5) "
        #     )
        #     if user_input == "1":
        #         create_cell_grid()
        #         break
        #     elif user_input == "2":
        #         initialize_driver_positions_for_trajectories()
        #         generate_trajectories()
        #         break
        #     elif user_input == "3":
        #         remove_idle_trajectories()
        #         break
        #     elif user_input == "4":
        #         initialize_driver_positions()
        #         break
        #     elif user_input == "5":
        #         TimeSeriesDiscretization.discretize_day()
        #         break
        #     else:
        #         print("This option is not allowed. Please try again.")
        break

    elif user_input == "5":
        # while True:
        #     user_input = input(
        #         "Which script do you want to start? (Visualize driver positions -> 1, Visualize order positions -> 2, Visualize trip data -> 3) "
        #     )
        #     if user_input == "1":
        #         visualize_drivers(f"drivers_{ProgramParams.SIMULATION_DATE.strftime('%Y-%m-%d')}.png")
        #         break
        #     elif user_input == "2":
        #         visualize_orders(f"orders_{ProgramParams.SIMULATION_DATE.strftime('%Y-%m-%d')}.png")
        #         break
        #     elif user_input == "3":
        #         visualize_trip_data()
        #         break
        #     else:
        #         print("This option is not allowed. Please try again.")
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
