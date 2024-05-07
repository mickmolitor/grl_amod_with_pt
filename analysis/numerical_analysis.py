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

def analyse():
    output_data = {
        "Average time reduction per vehicle per hour in minutes": 0.0,
        "Amount of served orders per day": 0.0,
        "Combi route quota": 0.0,
        "Average vehicle route length in meters": 0.0,
        "Vehicle workload": 0.0,
        "Relocation workload": 0.0,
        "Idling quota": 0.0,
        "Average time reduction per order in minutes": 0.0,
        "Percentage of accepted orders": 0.0,
        "Average distance of relocation in meters": 0.0
    }

    base_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"

    dates = [datetime.date(2023, 7, 24) + datetime.timedelta(days=x) for x in range(7)]

    data = load_and_merge_data(base_path, "tripdata", dates)
    datarl = load_and_merge_data(base_path, "relocation_trip_data", dates)
    datadriver = load_and_merge_data(base_path, "vehicle_data", dates)
    dataorders = load_and_merge_data("data/for_hire", "orders_", dates)


    output_data["Average time reduction per vehicle per hour in minutes"] = round(sum(data["time_reduction"]/60/24/len(dates)/ProgramParams.AMOUNT_OF_VEHICLES), 2)
    output_data["Amount of served orders per day"] = int(len(data)/len(dates))
    output_data["Combi route quota"] = f"{round(100*sum(data['combi_route']/len(data)), 2)}%"
    output_data["Average vehicle route length in meters"] = round(sum(data["total_vehicle_distance"]/len(data)),2)

    amount_occupied = datadriver.loc[datadriver["status"] == "occupied", "status"].count()
    amount_relocation = datadriver.loc[datadriver["status"] == "relocation", "status"].count()
    amount_idling = datadriver.loc[datadriver["status"] == "idling", "status"].count()
    output_data["Vehicle workload"] = f"{round(100*amount_occupied/len(datadriver), 2)}%"
    output_data["Relocation workload"] = f"{round(100*amount_relocation/len(datadriver), 2)}%"
    output_data["Idling quota"] = f"{round(100*amount_idling/len(datadriver), 2)}%"

    total_time_reduction =  round(sum(data["time_reduction"]/60), 2)
    output_data["Average time reduction per order in minutes"] = round(total_time_reduction/len(data), 2)
    output_data["Percentage of accepted orders"] = round(100*len(data)/len(dataorders), 2)
    output_data["Average distance of relocation in meters"] = round(sum(datarl["distance"]/len(datarl)), 2)

    return output_data

def numerical_analysis():
    set_params()

    result_str = ""
    
    results = analyse()
    for key in results:
        result_str += f"{key}: {results[key]}\n"

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

        data = analyse()
        for key in data:
            output_data[key].append(data[key])
    
    figure_path = f"store/comparisons"
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)
    with open(f"{figure_path}/{parameter}.csv", mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["Criteria"] + [str(value) for value in values])
        for row in output_data:
            writer.writerow([row] + output_data[row])



            
