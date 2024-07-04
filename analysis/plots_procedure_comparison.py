import csv
from datetime import datetime
import os
import re
import geopandas as gpd
from matplotlib import pyplot as plt
import pandas as pd
from analysis.configuration import get_procedure_comparison_values, set_params
from params.program_params import ProgramParams


def vehicle_postions_procedures():
    procedures, vehicle_params = get_procedure_comparison_values()
    vehicle_dfs = []
    proc_vehicle_pairs = []
    for procedure in procedures:
        for vehicle_amount in vehicle_params[procedure]:
            proc_vehicle_pairs.append((procedure, vehicle_amount))
            set_params()

            for param in vehicle_params[procedure][vehicle_amount]:
                ProgramParams.set_member(param, vehicle_params[procedure][vehicle_amount][param])

            vehicledata_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"
            
            vehicledata_files = [
                f
                for f in os.listdir(vehicledata_path)
                if f.endswith(".csv") and f.startswith("vehicle_data")
            ]
            dates = [re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) for f in vehicledata_files]
            dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"), reverse=True)
            vehicledata_file_name = f"vehicle_data{dates[0]}.csv"
            vehicledata_file_path = os.path.join(vehicledata_path, vehicledata_file_name)
            if os.path.exists(vehicledata_file_path):
                vehicledata = []
                with open(vehicledata_file_path, mode="r") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if int(row["total_seconds"]) == 82800:
                            vehicledata.append({"lat": float(row["lat"]), "lon": float(row["lon"])})
            vehicle_dfs.append(pd.DataFrame(vehicledata))

    city_borders = gpd.read_file("data/nyc_city_borders/borders.shp")
    subway_data_path = "data/continuous_subway_data.csv"
    subway_data_df = pd.read_csv(subway_data_path)
    fig, ax = plt.subplots(3, 2, figsize=(12, 16))
    for i in range(2):
        for j in range(3):
            axs = ax[j,i]
            procedure, vehicle_amount = proc_vehicle_pairs[i*3+j]
            vehicle_df = vehicle_dfs[i*3+j].sample(1000, replace=False, random_state=42)
            # Draw city borders
            city_borders.plot(ax=axs, color="lightgrey", alpha=0.6, label="City borders")

            # Draw stations
            axs.scatter(subway_data_df["LONG"], subway_data_df["LAT"], c="purple", label="Station", alpha=0.7, s = 3)

            # Draw vehicles
            axs.scatter(vehicle_df["lon"], vehicle_df["lat"], c="green", label="Fahrzeug", alpha=0.8, s = 3)

            axs.set_xlim(-74.05, -73.69)
            axs.set_ylim(40.535, 40.92)

            axs.legend(loc="lower right")
            procedure = "GRL" if procedure == "grl" else "QL"
            axs.set_title(f"{vehicle_amount} Fahrzeuge, {procedure}: Verteilung von 1000 zufällig\ngewählten Fahrzeugen am Ende des Testzeitraumes in NYC")
            axs.set_xlabel("Latitude")
            axs.set_ylabel("Longitude")
    plt.subplots_adjust(hspace=0.3)
    figure_path = f"store/procedure_comparisons/figures"
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)
    plt.savefig(f"{figure_path}/vehicle_location.png", dpi=600)