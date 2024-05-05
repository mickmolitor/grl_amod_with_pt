import csv
import datetime
import os
import re
import pandas as pd
import shutil
import matplotlib.pyplot as plt

from analysis.configuration import set_params, get_comparison_values
from params.program_params import Mode, ProgramParams

def load_and_merge_data(base_path, filename, dates):
    dfs = []
    
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

def numerical_analysis():
    set_params()

    result_str = ""
    base_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"

    dates = [datetime.date(2023, 7, 24) + datetime.timedelta(days=x) for x in range(7)]

    print(dates)
    # Laden und Zusammenführen der Daten für jeden Dateityp
    data = load_and_merge_data(base_path, "tripdata", dates)
    datarl = load_and_merge_data(base_path, "relocation_trip_data", dates)
    datadriver = load_and_merge_data(base_path, "vehicle_data", dates)
    dataorders = load_and_merge_data("data/for_hire", "orders_", dates)


    result_str += f'Average time reduction: {round(sum(data["time_reduction"]/60/24/len(dates)/ProgramParams.AMOUNT_OF_VEHICLES), 2)}\n'
    result_str += f'Amount of served orders per day: {len(data)/len(dates)}\n'
    result_str += f'Combi route quota: {round(100*sum(data["combi_route"]/len(data)), 2)}%\n'

    result_str += f'Average vehicle route length: {round(sum(data["total_vehicle_distance"]/len(data)),2)}\n'

    amount_occupied = datadriver.loc[datadriver["status"] == "occupied", "status"].count()
    amount_relocation = datadriver.loc[datadriver["status"] == "relocation", "status"].count()
    amount_idling = datadriver.loc[datadriver["status"] == "idling", "status"].count()
    result_str += f"Vehicle workload: {amount_occupied/len(datadriver)} (Relocation: {amount_relocation/len(datadriver)}, Idling: {amount_idling/len(datadriver)})\n"

    result_str += f'Total amount of served orders: {len(data)}\n'

    total_time_reduction =  round(sum(data["time_reduction"]/60), 2)
    result_str += f'Total time reduction in minutes: {total_time_reduction}\n'
    result_str += f'Average time reduction per order in minutes: {total_time_reduction/len(dataorders)}\n'
    result_str += f'Percentage of accepted orders: {round(100*len(data)/len(dataorders), 2)}%\n'

    result_str += f'Amount of relocations: {len(datarl)}\n'
    result_str += f'Average distance of relocation in meters: {round(sum(datarl["distance"]/len(datarl)), 2)}\n'

    figure_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/figures"
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)
    with open(f"{figure_path}/analysis_results.txt", mode="w") as text_file:
        text_file.write(result_str)
    print(result_str)

def numerical_comparison():
    set_params()
    parameter, values = get_comparison_values()
    output_data = {
        "Average time reduction per vehicle per hour in minutes": [],
        "Amount of served orders per day": [],
        "Combi route quota": [],
        "Average vehicle route length in meters": [],
        "Vehicle workload": [],
        "Relocation workload": [],
        "Idling quota": [],
        "Average time reduction per order in minutes": [],
        "Percentage of accepted orders": [],
        "Average distance of relocation in meters": []
    }

    for value in values:
        ProgramParams.set_member(parameter, value)

        base_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"

        dates = [datetime.date(2023, 7, 24) + datetime.timedelta(days=x) for x in range(7)]

        data = load_and_merge_data(base_path, "tripdata", dates)
        datarl = load_and_merge_data(base_path, "relocation_trip_data", dates)
        datadriver = load_and_merge_data(base_path, "vehicle_data", dates)
        dataorders = load_and_merge_data("data/for_hire", "orders_", dates)


        output_data["Average time reduction per vehicle per hour in minutes"].append(round(sum(data["time_reduction"]/60/24/len(dates)/ProgramParams.AMOUNT_OF_VEHICLES), 2))
        output_data["Amount of served orders per day"].append(int(len(data)/len(dates)))
        output_data["Combi route quota"].append(f"{round(100*sum(data['combi_route']/len(data)), 2)}%")
        output_data["Average vehicle route length in meters"].append(round(sum(data["total_vehicle_distance"]/len(data)),2))

        amount_occupied = datadriver.loc[datadriver["status"] == "occupied", "status"].count()
        amount_relocation = datadriver.loc[datadriver["status"] == "relocation", "status"].count()
        amount_idling = datadriver.loc[datadriver["status"] == "idling", "status"].count()
        output_data["Vehicle workload"].append(f"{round(100*amount_occupied/len(datadriver), 2)}%")
        output_data["Relocation workload"].append(f"{round(100*amount_relocation/len(datadriver), 2)}%")
        output_data["Idling quota"].append(f"{round(100*amount_idling/len(datadriver), 2)}%")

        total_time_reduction =  round(sum(data["time_reduction"]/60), 2)
        output_data["Average time reduction per order in minutes"].append(round(total_time_reduction/len(dataorders), 2))
        output_data["Percentage of accepted orders"].append(round(100*len(data)/len(dataorders), 2))
        output_data["Average distance of relocation in meters"].append(round(sum(datarl["distance"]/len(datarl)), 2))
    
    figure_path = f"store/comparisons"
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)
    with open(f"{figure_path}/{parameter}.csv", mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["Criteria"] + [str(value) for value in values])
        for row in output_data:
            writer.writerow([row] + output_data[row])



            
