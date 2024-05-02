from datetime import datetime
import os
import re
import pandas as pd
import shutil
import matplotlib.pyplot as plt

from params.program_params import Mode, ProgramParams

def numerical_analysis():

    def load_and_merge_data(base_path, filename):
        dfs = []
        files = [
            f
            for f in os.listdir(base_path)
            if f.endswith(".csv") and f.startswith(filename)
        ]
        dates = [re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) for f in files]
        dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        for date in dates:
            # Tripdata data
            file_name = f"{filename}{date}.csv"
            file_path = os.path.join(base_path, file_name)
            if os.path.exists(file_path):
                data = pd.read_csv(file_path)
                dfs.append(data)

        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True)
        else:
            merged_df = pd.DataFrame()
        return merged_df

    # Set program params
    ProgramParams.EXECUTION_MODE = Mode.GRAPH_REINFORCEMENT_LEARNING
    ProgramParams.DISCOUNT_RATE = 0.95
    ProgramParams.LS = 60
    ProgramParams.LEARNING_RATE = 0.01
    ProgramParams.IDLING_COST = 5
    ProgramParams.AMOUNT_OF_VEHICLES = 100
    ProgramParams.RELOCATION_RADIUS = 10000
    ProgramParams.MAIN_AND_TARGET_NET_SYNC_ITERATIONS = 60

    base_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/yes/data"

    # Laden und Zusammenführen der Daten für jeden Dateityp
    data = load_and_merge_data(base_path, "tripdata")
    datarl = load_and_merge_data(base_path, "relocation_trip_data")
    datadriver = load_and_merge_data(base_path, "vehicle_data")
    dataorders = load_and_merge_data("data/for_hire", "orders_")


    print(f'Durchschnittliche Zeitersparnis: {round(sum(data["time_reduction"]/60/24/21/100), 2)}')
    print(f'Anzahl Orders pro Tag: {len(data)/7}')
    print(f'Prozentualer Anteil Combirouten: {round(sum(data["combi_route"]/len(data)), 2)}')


    print(f'Durschnittliche Routenlänge: {round(sum(data["total_vehicle_distance"]/len(data)),2)}')

    anzahl_occupied = datadriver.loc[datadriver["status"] == "occupied", "status"].count()
    anzahl_relocation = datadriver.loc[datadriver["status"] == "relocation", "status"].count()
    anzahl_idling = datadriver.loc[datadriver["status"] == "idling", "status"].count()
    print(f'Anzahl der "occupied": {anzahl_occupied/len(datadriver), anzahl_relocation/len(datadriver), anzahl_idling/len(datadriver)}')


    print(f'Anzahl der Routen: {len(data)}')

    gesamte_zeitersparnis =  round(sum(data["time_reduction"]/60), 2)
    print(f'Gesame Zeitersparnis in Minute: {gesamte_zeitersparnis}')
    print(f'Durchschnittliche Zeitersparnis pro Order in Minuten: {gesamte_zeitersparnis/len(dataorders)}')
    print(f'Prozentualer Anteil Orders: {len(data)/len(dataorders)}')

    print(f'Anzahl an relocation: {len(datarl)}')
    print(f'Durchschnittliche Entfernung relocation: {round(sum(datarl["distance"]/len(datarl)), 2)}')

    # pathstate = "code/training_data/state_value_table.csv"
    # datastate = pd.read_csv(pathstate)

    # print("##########################################################################################")
    # anzahl_max_statevalue = datastate.loc[datastate["state_value"] == 1000, "state_value"].count()
    # print(f'Anzahl state_value_Werte = maximum: {anzahl_max_statevalue}')
    # print(f'Prozentualer Anteil: {anzahl_max_statevalue/len(datastate)}')

    # anzahl_min_statevalue = datastate.loc[datastate["state_value"] == -1000, "state_value"].count()
    # print(f'Anzahl state_value_Werte = min: {anzahl_min_statevalue}')
    # print(f'Prozentualer Anteil: {anzahl_min_statevalue/len(datastate)}')

    # anzahl_kleiner0_statevalue = datastate.loc[datastate["state_value"] <= 0, "state_value"].count()
    # print(f'Anzahl state_value_Werte = keliner 0: {anzahl_kleiner0_statevalue}')
    # print(f'Prozentualer Anteil: {anzahl_kleiner0_statevalue/len(datastate)}')