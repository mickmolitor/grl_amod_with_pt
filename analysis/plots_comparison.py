import csv
from datetime import datetime
import os
import re

from matplotlib import pyplot as plt
from numpy import mean
import pandas as pd
from analysis.configuration import get_comparison_values, set_params
from analysis.numerical_analysis import calculate_vehicle_distribution
from params.program_params import ProgramParams


def plot_comparison():
    set_params()
    parameter, values = get_comparison_values()
    values.sort()

    fig, ax = plt.subplots(2, 3, figsize=(15, 12))

    time_reduction_per_order(ax[0, 0], parameter, values)
    amount_of_orders_per_vehicle(ax[0, 1], parameter, values)
    amount_of_orders(ax[0, 2], parameter, values)
    workload(ax[1,0], parameter, values)
    combi_route_quota(ax[1,1], parameter, values)
    vehicle_distribution(ax[1,2], parameter, values)
    plt.legend()
    plt.tight_layout()
    figure_path = f"store/comparisons/figures"
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)
    plt.savefig(f"{figure_path}/{parameter}.png")


def time_reduction_per_order(ax, parameter: str, values: list):
    time_reductions = []
    for value in values:
        ProgramParams.set_member(parameter, value)

        tripdata_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"
        time_reduction_per_order = []

        tripdata_files = [
            f
            for f in os.listdir(tripdata_path)
            if f.endswith(".csv") and f.startswith("tripdata")
        ]
        dates = [re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) for f in tripdata_files]
        dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        dates = dates[-7:]
        for date in dates:
            # Tripdata data
            tripdata_file_name = f"tripdata{date}.csv"
            tripdata_file_path = os.path.join(tripdata_path, tripdata_file_name)
            if os.path.exists(tripdata_file_path):
                tripdata = pd.read_csv(tripdata_file_path)
                time_reduction_per_order.append(
                    tripdata["time_reduction"].sum() / 60 / len(tripdata)
                )
            else:
                time_reduction_per_order.append(float("nan"))

        time_reductions.append(mean(time_reduction_per_order))

    string_values = list(map(lambda x: str(x), values))

    ax.bar(string_values, time_reductions, color="orange")
    ax.set_xlabel(parameter)
    ax.set_ylabel("Time reduction in minutes")
    ax.set_title("Average time reduction per served order in minutes")
    ax.set_xticklabels(values, rotation=45)


def amount_of_orders_per_vehicle(ax, parameter: str, values: list):
    amount_of_orders_per_vehicle = []
    for value in values:
        ProgramParams.set_member(parameter, value)

        tripdata_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"
        amount_of_orders_per_vehicle_per_day = []

        tripdata_files = [
            f
            for f in os.listdir(tripdata_path)
            if f.endswith(".csv") and f.startswith("tripdata")
        ]
        dates = [re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) for f in tripdata_files]
        dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        dates = dates[-7:]
        for date in dates:
            # Tripdata data
            tripdata_file_name = f"tripdata{date}.csv"
            tripdata_file_path = os.path.join(tripdata_path, tripdata_file_name)
            if os.path.exists(tripdata_file_path):
                tripdata = pd.read_csv(tripdata_file_path)
                amount_of_orders_per_vehicle_per_day.append(
                    len(tripdata) / ProgramParams.AMOUNT_OF_VEHICLES
                )
            else:
                amount_of_orders_per_vehicle_per_day.append(float("nan"))

        amount_of_orders_per_vehicle.append(mean(amount_of_orders_per_vehicle_per_day))

    string_values = list(map(lambda x: str(x), values))

    ax.bar(string_values, amount_of_orders_per_vehicle, color="red")
    ax.set_xlabel(parameter)
    ax.set_ylabel("Amount of orders per vehicle per day")
    ax.set_title("Amount of orders served per vehicle per day")
    ax.set_xticklabels(values, rotation=45)


def amount_of_orders(ax, parameter: str, values: list):
    amount_of_orders = []
    for value in values:
        ProgramParams.set_member(parameter, value)

        tripdata_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"
        amount_of_orders_per_day = []

        tripdata_files = [
            f
            for f in os.listdir(tripdata_path)
            if f.endswith(".csv") and f.startswith("tripdata")
        ]
        dates = [re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) for f in tripdata_files]
        dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        dates = dates[-7:]
        for date in dates:
            # Tripdata data
            tripdata_file_name = f"tripdata{date}.csv"
            tripdata_file_path = os.path.join(tripdata_path, tripdata_file_name)
            if os.path.exists(tripdata_file_path):
                tripdata = pd.read_csv(tripdata_file_path)
                amount_of_orders_per_day.append(len(tripdata))
            else:
                amount_of_orders_per_day.append(float("nan"))

        amount_of_orders.append(mean(amount_of_orders_per_day))

    string_values = list(map(lambda x: str(x), values))

    ax.bar(string_values, amount_of_orders, color="darkred")
    ax.set_xlabel(parameter)
    ax.set_ylabel("Amount of orders per day")
    ax.set_title("Amount of orders served per day")
    ax.set_xticklabels(values, rotation=45)


def workload(ax, parameter: str, values: list):
    occ = []
    idl = []
    rel = []
    not_idl = []
    for value in values:
        ProgramParams.set_member(parameter, value)

        vehicle_data_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"
        occupied = []
        idle = []
        relocation = []

        vehicle_data_files = [
            f
            for f in os.listdir(vehicle_data_path)
            if f.endswith(".csv") and f.startswith("vehicle_data")
        ]
        dates = [
            re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) for f in vehicle_data_files
        ]
        dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        dates = dates[-7:]
        for date in dates:
            # Tripdata data
            vehicle_data_filename = f"vehicle_data{date}.csv"
            vehicle_data_filepath = os.path.join(vehicle_data_path, vehicle_data_filename)
            if os.path.exists(vehicle_data_filepath):
                vehicle_data = pd.read_csv(vehicle_data_filepath)
                occupied.append(
                    vehicle_data.loc[
                        vehicle_data["status"] == "occupied", "status"
                    ].count()
                    / len(vehicle_data)
                )
                idle.append(
                    vehicle_data.loc[
                        vehicle_data["status"] == "idling", "status"
                    ].count()
                    / len(vehicle_data)
                )
                relocation.append(
                    vehicle_data.loc[
                        vehicle_data["status"] == "relocation", "status"
                    ].count()
                    / len(vehicle_data)
                )

            else:
                occupied.append(float("nan"))
                relocation.append(float("nan"))
                idle.append(float("nan"))

        occ.append(mean(occupied))
        idl.append(mean(idle))
        rel.append(mean(relocation))
        not_idl.append(occ[-1] + rel[-1])

    string_values = list(map(lambda x: str(x), values))
    print(occ)
    print(rel)
    print(idl)

    ax.bar(
        string_values,
        occ,
        color="blue",
        label="Occupied",
    )
    ax.bar(
        string_values,
        rel,
        color="green",
        label="Relocation",
        bottom=occ,
    )
    ax.bar(
        string_values,
        idl,
        color="grey",
        label="Idling",
        bottom=not_idl,
    )

    ax.set_xlabel(parameter)
    ax.set_ylabel("Workload quota")
    ax.set_title("Quota of occupied, idle and relocated vehicles over the whole time")
    ax.set_xticklabels(values, rotation=45)

def combi_route_quota(ax, parameter: str, values: list):
    combi_quota = []
    for value in values:
        ProgramParams.set_member(parameter, value)

        tripdata_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"
        combi_quota_per_day = []

        tripdata_files = [
            f
            for f in os.listdir(tripdata_path)
            if f.endswith(".csv") and f.startswith("tripdata")
        ]
        dates = [re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) for f in tripdata_files]
        dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        dates = dates[-7:]
        for date in dates:
            # Tripdata data
            tripdata_file_name = f"tripdata{date}.csv"
            tripdata_file_path = os.path.join(tripdata_path, tripdata_file_name)
            if os.path.exists(tripdata_file_path):
                tripdata = pd.read_csv(tripdata_file_path)
                combi_quota_per_day.append(len(tripdata[tripdata["combi_route"] == True]) / len(tripdata))
            else:
                combi_quota_per_day.append(float("nan"))

        combi_quota.append(mean(combi_quota_per_day))

    string_values = list(map(lambda x: str(x), values))

    ax.bar(string_values, combi_quota, color="lightgreen")
    ax.set_xlabel(parameter)
    ax.set_ylabel("Combi route quota")
    ax.set_title("Combi route quota under served orders")
    ax.set_xticklabels(values, rotation=45)


def vehicle_distribution(ax, parameter: str, values: list):
    distribution = []
    for value in values:
        ProgramParams.set_member(parameter, value)

        vehicle_data_path = f"store/{ProgramParams.DATA_OUTPUT_FILE_PATH()}/data"
        distribution_per_day = []

        vehicle_data_files = [
            f
            for f in os.listdir(vehicle_data_path)
            if f.endswith(".csv") and f.startswith("vehicle_data")
        ]
        dates = [
            re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) for f in vehicle_data_files
        ]
        dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        dates = dates[-7:]
        for date in dates:
            # Tripdata data
            vehicle_data_file_name = f"vehicle_data{date}.csv"
            vehicle_data_file_path = os.path.join(vehicle_data_path, vehicle_data_file_name)
            if os.path.exists(vehicle_data_file_path):
                vehicle_data = pd.read_csv(vehicle_data_file_path)
                distribution_per_day.append(calculate_vehicle_distribution(vehicle_data))
            else:
                distribution_per_day.append(float("nan"))

        distribution.append(mean(distribution_per_day))

    string_values = list(map(lambda x: str(x), values))

    ax.bar(string_values, distribution, color="purple")
    ax.set_xlabel(parameter)
    ax.set_ylabel("Jensen-Shannon divergence")
    ax.set_title("Vehicle distribution in comparison to station distribution")
    ax.set_xticklabels(values, rotation=45)