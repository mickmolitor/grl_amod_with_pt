from statistics import mean
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.wkt import loads
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime
import re
from datetime import datetime


## fig 1.
def Time_savings_number_of_cars():
    base_path = "store/for_hire/rl_relocation/drivers"  # manually entered
    driver_counts = [100, 500, 1000, 2000, 3000, 4000, 5000]
    time_savings_avg = {}

    for count in driver_counts:
        total_time_reduction = 0
        file_count = 0
        path = os.path.join(base_path, str(count))
        for file_name in os.listdir(path):
            if file_name.startswith("tripdata") and file_name.endswith(".csv"):
                df = pd.read_csv(os.path.join(path, file_name))
                total_time_reduction += df["time_reduction"].sum()
                file_count += 1

        if file_count > 0:
            avg_time_savings_per_hour_per_car = (total_time_reduction / 60) / (
                24 * file_count
            )
            time_savings_avg[count] = avg_time_savings_per_hour_per_car / int(count)

    # Plotting
    #plt.figure(figsize=(8, 6))
    bar_width = 0.4  # You can adjust the width as needed
    positions = range(len(time_savings_avg))

    plt.bar(positions, time_savings_avg.values(), color="skyblue", width=bar_width)
    plt.xlabel("Number of cars")
    plt.ylabel("Time savings per hour per car (minutes)")
    plt.title("Time savings per hour per car")

    plt.xticks(positions, labels=[str(k) for k in time_savings_avg.keys()])

    # Display can be adjusted. Just select what is desired from moving_average.
    # moving average: calculate_moving_average
    # linear regression: calculate_linear_regression
    values = list(
        time_savings_avg.values()
    )  # Convert values to a list for linear regression
    #regression_values = calculate_moving_average(values, window_size=1)
    #plt.plot(
    #    positions,
    #    regression_values,
    #    color="red",
    #    marker="o",
    #    linestyle="-",
    #    linewidth=2,
    #    label="Linear Regression",
    #)
    plt.savefig("store/plots/Time_savings_number_of_cars.png")
    


#Time_savings_number_of_cars()


## fig 2.
def Rejection_rate_in_different_number_of_cars():
    base_path = "store/for_hire/rl_relocation/drivers"  # manually entered
    driver_counts = [10, 100, 1000, 2000, 5000]
    quota_sums = {}
    file_counts = {}

    for count in driver_counts:
        path = os.path.join(base_path, str(count))
        for file_name in os.listdir(path):
            if file_name.startswith("ordersdata") and file_name.endswith(".csv"):
                file_path = os.path.join(path, file_name)
                df = pd.read_csv(file_path)
                quota_sum = df["quota_of_unserved_orders"].sum()

                if count not in quota_sums:
                    quota_sums[count] = 0
                    file_counts[count] = 0

                quota_sums[count] += quota_sum
                file_counts[count] += len(df)

    avg_quota_per_driver = {
        count: quota_sums[count] / file_counts[count] for count in driver_counts
    }
    plt.figure(figsize=(10, 6))
    positions = range(len(avg_quota_per_driver))
    plt.bar(positions, avg_quota_per_driver.values(), color="skyblue")
    plt.xlabel("Number of cars")
    plt.ylabel("Rejection rate")
    plt.title(
        "Rejection rate in different number of cars（for_hire/rl_relocation）"
    )
    plt.xticks(positions, labels=[str(k) for k in avg_quota_per_driver.keys()])
    # Display can be adjusted. Just select what is desired from moving_average.
    # moving average: calculate_moving_average
    # linear regression: calculate_linear_regression
    values = list(avg_quota_per_driver.values())
    regression_values = calculate_moving_average(values, window_size=1)
    plt.plot(
        positions,
        regression_values,
        color="red",
        marker="o",
        linestyle="-",
        linewidth=2,
        label="Linear Regression",
    )
    plt.savefig("store/plots/Rejection_rate_in_different_number_of_cars.png")
    


#Rejection_rate_in_different_number_of_cars()


def calculate_percentage(combi_route_counts, total_counts):
    combi_route_percentages = {}
    for method, count in combi_route_counts.items():
        total = total_counts[method]
        percentage = (count / total) * 100 if total > 0 else 0
        combi_route_percentages[method] = percentage
    return combi_route_percentages


def process_directory(data_path, combi_route_counts, total_counts):
    pattern = re.compile(r"tripdata\d{4}-\d{2}-\d{2}\.csv$")

    for entry in os.listdir(data_path):
        if pattern.match(entry):  # Checks if the filename matches the pattern
            entry_path = os.path.join(data_path, entry)
            df = pd.read_csv(entry_path)
            # Check if 'combi_route' is in the DataFrame column names to avoid KeyError
            if "combi_route" in df.columns:
                combi_true_count = df[df["combi_route"] == True].shape[0]
                modeling_method = os.path.basename(data_path)
                combi_route_counts[modeling_method] += combi_true_count
                total_counts[modeling_method] += df.shape[0]


def Number_of_combi_routes_in_percent():
    data_path = "store/for_hire"  # manually entered
    combi_route_counts = {}
    total_counts = {}

    for method_dir in os.listdir(data_path):
        method_path = os.path.join(data_path, method_dir)
        if os.path.isdir(method_path):
            combi_route_counts[method_dir] = 0
            total_counts[method_dir] = 0
            process_directory(method_path, combi_route_counts, total_counts)

    combi_route_percentages = calculate_percentage(combi_route_counts, total_counts)

    method_names = {
        "baseline": "Baseline",
        "rl": "RL",
        "rl_relocation": "RL with relocation",
        "drl": "DRL",
    }

    labels = [
        method_names.get(method, method) for method in combi_route_percentages.keys()
    ]
    percentages = list(combi_route_percentages.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, percentages, color="skyblue")
    plt.xlabel("Modeling method")
    plt.ylabel("Percentage of combi routes (%)")
    plt.title("Number of combi routes in percent")
    plt.xticks(rotation=45)
    # Display can be adjusted. Just select what is desired from moving_average.
    # moving average: calculate_moving_average
    # linear regression: calculate_linear_regression
    values = list(
        combi_route_percentages.values()
    )  # Convert the values to a list for linear regression
    regression_values = calculate_linear_regression(values, window_size=1)
    positions = range(len(labels))
    plt.plot(
        positions,
        regression_values,
        color="red",
        marker="o",
        linestyle="-",
        linewidth=2,
        label="Linear Regression",
    )
    plt.savefig("store/plots/Number_of_combi_routes_in_percent.png")
    


##Number_of_combi_routes_in_percent()


## fig 4.
def process_directory_for_route_distribution(
    data_path, combi_route_counts, direct_route_counts, file_days
):
    pattern = r"^tripdata\d{4}-\d{2}-\d{2}"  # RegEx for files starting with 'tripdata' and containing a date
    for method_dir in os.listdir(data_path):
        method_path = os.path.join(data_path, method_dir)
        if os.path.isdir(method_path):
            combi_route_counts[method_dir] = 0
            direct_route_counts[method_dir] = 0
            file_days[method_dir] = 0

            for file_name in os.listdir(method_path):
                if file_name.endswith(".csv") and re.match(pattern, file_name):
                    df = pd.read_csv(os.path.join(method_path, file_name))
                    if (
                        "combi_route" in df.columns
                    ):  # Ensure the 'combi_route' column exists
                        combi_true_count = df[df["combi_route"] == True].shape[0]
                        combi_false_count = df[df["combi_route"] == False].shape[0]

                        combi_route_counts[method_dir] += combi_true_count
                        direct_route_counts[method_dir] += combi_false_count
                        file_days[method_dir] += 1


def Routes_distribution_per_hour():
    data_path = "store/for_hire"  # Manually entered path

    combi_route_counts = {}
    direct_route_counts = {}
    file_days = {}

    process_directory_for_route_distribution(
        data_path, combi_route_counts, direct_route_counts, file_days
    )
    hours_per_day = 24
    combi_avg_per_hour = {
        method: (
            (combi_route_counts[method] / (file_days[method] * hours_per_day))
            if file_days[method] > 0
            else 0
        )
        for method in combi_route_counts
    }
    direct_avg_per_hour = {
        method: (
            (direct_route_counts[method] / (file_days[method] * hours_per_day))
            if file_days[method] > 0
            else 0
        )
        for method in direct_route_counts
    }

    labels = ["Baseline", "RL", "RL with relocation", "DRL"]
    mapping = {
        "baseline": "Baseline",
        "rl": "RL",
        "rl_relocation": "RL with relocation",
        "drl": "DRL",
    }
    combi_data = [combi_avg_per_hour.get(method, 0) for method in mapping]
    direct_data = [direct_avg_per_hour.get(method, 0) for method in mapping]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, combi_data, width, label="Combi routes")
    rects2 = ax.bar(x + width / 2, direct_data, width, label="Direct routes")

    ax.set_xlabel("Modeling method")
    ax.set_ylabel("Number of routes per hour")
    ax.set_title("Distribution of routes in combi and direct routes per hour")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    plt.savefig("store/plots/Routes_distribution_per_hour.png")
    


# Routes_distribution_per_hour()


## fig 5.
def Combi_routes_per_hour_in_different_number_of_cars():
    base_path = "store/for_hire/rl_relocation/drivers"  # Manually entered path
    driver_counts = [10, 100, 1000, 2000, 5000]
    combi_counts = {}
    file_days = {}

    for count in driver_counts:
        path = os.path.join(base_path, str(count))
        if os.path.isdir(path):
            combi_counts[count] = 0
            file_days[count] = 0

            for file_name in os.listdir(path):
                if file_name.startswith("tripdata") and file_name.endswith(".csv"):
                    file_path = os.path.join(path, file_name)

                    df = pd.read_csv(file_path)
                    combi_true_count = (df["combi_route"] == True).sum()

                    combi_counts[count] += combi_true_count
                    file_days[count] += 1

    hours_per_day = 24
    combi_avg_per_hour = {
        count: (combi_counts[count] / (file_days[count] * hours_per_day * int(count)))
        for count in combi_counts
    }

    plt.figure(figsize=(10, 6))
    plt.bar(
        [str(count) for count in driver_counts],
        [combi_avg_per_hour.get(count, 0) for count in driver_counts],
        color="skyblue",
    )
    plt.xlabel("Number of cars")
    plt.ylabel("Number of combi routes per hour")
    plt.title("Number of combi routes per hour in different number of cars")
    plt.xticks([str(count) for count in driver_counts])
    plt.savefig(
        "store/plots/Combi_routes_per_hour_in_different_number_of_cars.png"
    )
    


# Combi_routes_per_hour_in_different_number_of_cars()


## fig 6.
def average_time_Number_of_cars():
    base_path = "store/for_hire/rl_relocation/drivers"  # Manually entered path
    driver_counts = [100, 500, 1000, 2000, 3000, 4000, 5000]
    status_speed_kmh = {"occupied": 1, "idling": 1, "relocation": 1}

    status_time_proportion = {
        driver: {"occupied": [], "idling": [], "relocation": []}
        for driver in driver_counts
    }

    for count in driver_counts:
        drivers_path = os.path.join(base_path, str(count))
        for file_name in os.listdir(drivers_path):
            if file_name.startswith("driverdata"):
                file_path = os.path.join(drivers_path, file_name)
                df = pd.read_csv(file_path)
                total_records = len(df)
                for status in status_time_proportion[count]:

                    status_records = df[df["status"] == status].shape[0]
                    status_proportion = (
                        status_records / total_records if total_records > 0 else 0
                    )
                    status_time_proportion[count][status].append(status_proportion)

    avg_status_proportion = {
        driver: {
            status: np.mean(proportions) for status, proportions in statuses.items()
        }
        for driver, statuses in status_time_proportion.items()
    }

    avg_distance_data = {
        driver: {
            status: avg_status_proportion[driver][status] * status_speed_kmh[status]
            for status in status_speed_kmh
        }
        for driver in driver_counts
    }

    fig, ax = plt.subplots()
    width = 0.25
    ind = np.arange(len(driver_counts))

    for i, (status, color) in enumerate(
        zip(["occupied", "idling", "relocation"], ["skyblue", "orange", "green"])
    ):
        avg_distances = [avg_distance_data[driver][status] for driver in driver_counts]
        ax.bar(
            ind + i * width,
            avg_distances,
            width,
            label=status.capitalize(),
            color=color,
        )

    ax.set_xlabel("Number of cars")
    ax.set_ylabel("Average time in each status")
    ax.set_title("Average time in each status")
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(driver_counts)
    ax.legend()

    plt.tight_layout()
    plt.savefig("store/plots/average_time_Number_of_cars_presi.png")
    

#average_time_Number_of_cars()


def average_trip_distances_per_day_amount_of_cars():
    base_path = "store/for_hire/rl_relocation/drivers"  # Manually entered path
    driver_counts = ["10", "100", "500" "1000", "2000", "3000", "4000", "5000"]
    average_route_length = {
        count: {"driver_to_pickup_distance_km": [], "pickup_to_dropoff_distance_km": []}
        for count in driver_counts
    }
    average_combi_route_length = {
        count: {
            "driver_to_pickup_distance_km": [],
            "pickup_to_dropoff_distance_km": [],
            "dropoff_to_destination_distance_km": [],
            "driver_to_dropoff_distance_km": [],
        }
        for count in driver_counts
    }
    average_route_length_list = []
    average_combi_route_length_list = []

    taxi_zones_file_path = "code/data/taxi_zones.csv"
    taxi_zones = pd.read_csv(taxi_zones_file_path)
    # Convert polygon strings to shapely polygon objects
    taxi_zones["polygon"] = taxi_zones["the_geom"].apply(loads)
    # Calculate the latitude and longitude of the center for each zone
    taxi_zones["center"] = taxi_zones["polygon"].apply(
        lambda p: (p.centroid.y, p.centroid.x)
    )
    # Create a dictionary to map zone IDs to their center latitude and longitude
    zone_centers = dict(zip(taxi_zones["LocationID"], taxi_zones["center"]))

    # Define a function to calculate the distance between two zones in kilometers
    def calculate_distance_km(zone1_id, zone2_id):
        if zone1_id in zone_centers and zone2_id in zone_centers:
            # Use geodesic from geopy to calculate the distance
            return geodesic(zone_centers[zone1_id], zone_centers[zone2_id]).kilometers
        else:
            raise Exception(f"{zone1_id} or {zone2_id} not found")

    for count in driver_counts:
        tripdata_path = os.path.join(base_path, str(count))
        tripdata_files = [
            f for f in os.listdir(tripdata_path) if f.endswith(".csv") and f.startswith("tripdata")
        ]
        dates = [re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1) for f in tripdata_files]
        dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        # Use last 7 days
        for date in dates[-7:]:
            # Tripdata data
            tripdata_file_name = f"tripdata{date}.csv"
            tripdata_file_path = os.path.join(tripdata_path, tripdata_file_name)
            if os.path.exists(tripdata_file_path):
                tripdata = pd.read_csv(tripdata_file_path)
                # Calculate distances for each trip in the dataset
                tripdata["driver_to_pickup_distance_km"] = tripdata.apply(
                    lambda x: calculate_distance_km(
                        x["driver_start_zone_id"], x["passenger_pickup_zone_id"]
                    ),
                    axis=1,
                )
                tripdata["pickup_to_dropoff_distance_km"] = tripdata.apply(
                    lambda x: calculate_distance_km(
                        x["passenger_pickup_zone_id"], x["passenger_dropoff_zone_id"]
                    ),
                    axis=1,
                )
                tripdata["dropoff_to_destination_distance_km"] = tripdata.apply(
                    lambda x: calculate_distance_km(
                        x["passenger_dropoff_zone_id"], x["destination_id"]
                    ),
                    axis=1,
                )
                average_route_length[count]["driver_to_pickup_distance_km"].append(
                    tripdata[tripdata["combi_route"]][
                        "driver_to_pickup_distance_km"
                    ].mean()
                )
                average_route_length[count]["pickup_to_dropoff_distance_km"].append(
                    tripdata[tripdata["combi_route"]][
                        "pickup_to_dropoff_distance_km"
                    ].mean()
                )
                average_combi_route_length[count][
                    "driver_to_pickup_distance_km"
                ].append(
                    tripdata[tripdata["combi_route"]][
                        "driver_to_pickup_distance_km"
                    ].mean()
                )

                average_combi_route_length[count][
                    "pickup_to_dropoff_distance_km"
                ].append(
                    tripdata[tripdata["combi_route"]][
                        "pickup_to_dropoff_distance_km"
                    ].mean()
                )

                average_combi_route_length[count][
                    "dropoff_to_destination_distance_km"
                ].append(
                    tripdata[tripdata["combi_route"]][
                        "dropoff_to_destination_distance_km"
                    ].mean()
                )

        average_route_length_list.append(
            [
                count,
                mean(average_route_length[count]["driver_to_pickup_distance_km"]),
                mean(average_route_length[count]["pickup_to_dropoff_distance_km"]),
            ]
        )
        average_combi_route_length_list.append(
            [
                count,
                mean(average_combi_route_length[count]["driver_to_pickup_distance_km"]),
                mean(
                    average_combi_route_length[count]["pickup_to_dropoff_distance_km"]
                ),
                mean(
                    average_combi_route_length[count][
                        "dropoff_to_destination_distance_km"
                    ]
                ),
                mean(average_combi_route_length[count]["driver_to_pickup_distance_km"])
                + mean(
                    average_combi_route_length[count]["pickup_to_dropoff_distance_km"]
                ),
            ]
        )
    max_y = 0
    for entry in average_combi_route_length_list:
        if max_y < entry[1] + entry[2] + entry[3]:
            max_y = entry[1] + entry[2] + entry[3]
    max_y = int(max_y) + 1

    average_route_length_df = pd.DataFrame(
        average_route_length_list,
        columns=[
            "driver_count",
            "driver_to_pickup_distance_km",
            "pickup_to_dropoff_distance_km",
        ],
    )
    average_combi_route_length_df = pd.DataFrame(
        average_combi_route_length_list,
        columns=[
            "driver_count",
            "driver_to_pickup_distance_km",
            "pickup_to_dropoff_distance_km",
            "dropoff_to_destination_distance_km",
            "driver_to_dropoff_distance_km",
        ],
    )
    fig, axs = plt.subplots(1, 2, figsize=(30, 12))
    ax5, ax6 = axs.flatten()
    # Direct plot
    ax5.bar(
        driver_counts,
        average_route_length_df["driver_to_pickup_distance_km"],
        color="#90EE90",
        label="Driver position to pickup point",
    )
    ax5.bar(
        driver_counts,
        average_route_length_df["pickup_to_dropoff_distance_km"],
        color="green",
        label="Pickup point to destination",
        bottom=average_route_length_df["driver_to_pickup_distance_km"],
    )
    ax5.set_ylim(0, max_y)
    ax5.set_xlabel("Number of cars")
    ax5.set_ylabel("Average trip distances per day in km")
    ax5.set_title("Average trip distances per day for direct routes")
    ax5.legend()
    # Combined plot
    ax6.bar(
        driver_counts,
        average_combi_route_length_df["driver_to_pickup_distance_km"],
        color="#90EE90",
        label="Driver position to pickup point",
    )
    ax6.bar(
        driver_counts,
        average_combi_route_length_df["pickup_to_dropoff_distance_km"],
        color="green",
        label="Pickup point to station",
        bottom=average_combi_route_length_df["driver_to_pickup_distance_km"],
    )
    ax6.bar(
        driver_counts,
        average_combi_route_length_df["dropoff_to_destination_distance_km"],
        color="#006400",
        label="Station to destination",
        bottom=average_combi_route_length_df["driver_to_dropoff_distance_km"],
    )
    ax6.set_ylim(0, max_y)
    ax6.set_xlabel("Number of cars")
    ax6.set_ylabel("Average trip distances per day in km")
    ax6.set_title("Average trip distances per day for combination routes")
    ax6.legend()
    plt.savefig("store/plots/average_trip_distances_per_day_for_combination_routes.png")
    
#average_trip_distances_per_day_amount_of_cars()

## fig 7.
def average_driven_distance_modeling_method():
    base_path = "store/for_hire"  # Manually entered path
    methods = ["baseline", "rl", "rl_relocation", "drl"]
    status_speed = {"occupied": 1, "idling": 1, "relocation": 1}

    status_proportions = {
        method: {"occupied": [], "idling": [], "relocation": []} for method in methods
    }
    total_counts = {method: [] for method in methods}

    for method in methods:
        method_path = os.path.join(base_path, method)
        for file_name in os.listdir(method_path):
            if file_name.startswith("driverdata"):
                file_path = os.path.join(method_path, file_name)
                df = pd.read_csv(file_path)
                total_count = len(df)
                for status in status_speed:
                    status_count = df[df["status"] == status].shape[0]
                    status_proportions[method][status].append(
                        status_count / total_count if total_count else 0
                    )

    avg_proportions = {
        method: {
            status: np.mean(proportions) for status, proportions in status_data.items()
        }
        for method, status_data in status_proportions.items()
    }

    avg_distance_data = {
        method: {
            status: avg_proportions[method][status] * status_speed[status] * 3.6
            for status in status_speed
        }
        for method in methods
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.2
    ind = np.arange(len(methods))
    for i, (status, color) in enumerate(
        zip(["occupied", "idling", "relocation"], ["skyblue", "orange", "green"])
    ):
        avg_distances = [avg_distance_data[method][status] for method in methods]
        ax.bar(
            ind + i * width,
            avg_distances,
            width,
            label=status.capitalize(),
            color=color,
        )

    ax.set_xlabel("Modeling method")
    ax.set_ylabel("Average driven distance per hour (km)")
    ax.set_title("Average driven distance by method and status")
    ax.set_xticks(ind + width)
    ax.set_xticklabels(methods)
    ax.legend()

    plt.tight_layout()
    plt.savefig("store/plots/average_driven_distance_modeling_method.png")
    


# average_driven_distance_modeling_method()


## fig. 8
## fig. 8-1
def calculate_moving_average(values, window_size):
    """Calculates the moving average with a specific window size."""
    # Extend the values at the beginning to start the moving average from the first point
    extended_values = np.pad(values, (window_size - 1, 0), mode="edge")
    moving_average = np.convolve(
        extended_values, np.ones(window_size) / window_size, mode="valid"
    )
    return moving_average


def custom_rolling_avg(values, window_size):
    # Manual calculation of the moving average for the edges
    avg = np.empty_like(values, dtype=float)
    for i in range(len(values)):
        start = max(0, i - window_size + 1)
        end = i + 1
        avg[i] = np.mean(values[start:end])
    return avg


def compare_time_savings_rl_bl():
    number_of_cars = 100
    base_paths = {"baseline": "store/for_hire/baseline/drivers/100", "rl": "store/for_hire/rl/drivers/100"}
    time_savings = {"baseline": {}, "rl": {}}

    for model, base_path in base_paths.items():
        for file_name in os.listdir(base_path):
            match = re.match(r"tripdata(\d{4}-\d{2}-\d{2})\.csv", file_name)
            if match:
                date = match.group(1)
                df = pd.read_csv(os.path.join(base_path, file_name))
                if "time_reduction" in df.columns:
                    total_time_reduction_seconds = df["time_reduction"].sum()
                    avg_time_savings_per_hour_per_car = (
                        total_time_reduction_seconds / 60 / 24
                    ) / number_of_cars
                    time_savings[model][date] = avg_time_savings_per_hour_per_car

    dates = sorted(
        set(time_savings["baseline"].keys()) | set(time_savings["rl"].keys())
    )
    baseline_savings = [time_savings["baseline"].get(date, 0) for date in dates]
    rl_savings = [time_savings["rl"].get(date, 0) for date in dates]

    window_size = 3

    # Using the custom function for the moving average
    baseline_rolling_avg = custom_rolling_avg(np.array(baseline_savings), window_size)
    rl_rolling_avg = custom_rolling_avg(np.array(rl_savings), window_size)

    plt.figure(figsize=(10, 6))
    x = np.arange(len(dates))  # Direct use of the full length of 'dates'

    color_baseline = "blue"
    color_rl = "orange"

    plt.bar(x + 0.2, rl_savings, width=0.4, label="RL", color=color_rl)
    plt.bar(
        x - 0.2, baseline_savings, width=0.4, label="Baseline", color=color_baseline
    )

    plt.plot(
        x,
        rl_rolling_avg,
        label="RL (Moving Average)",
        color="orangered",
        marker="o",
        linestyle="-",
        markersize=5,
    )
    plt.plot(
        x,
        baseline_rolling_avg,
        label="Baseline (Moving Average)",
        color="darkblue",
        marker="o",
        linestyle="-",
        markersize=5,
    )

    plt.ylim([0, 200])
    plt.xlabel("Date")
    plt.ylabel("Time savings (minutes)")
    plt.title("Time savings per car per hour (RL vs Baseline)")
    plt.xticks(x, dates, rotation=45)
    plt.legend(loc ='lower left')
    plt.tight_layout()
    plt.savefig("store/plots/compare_time_savings_rl_bl_100_presi.png")
    #


#compare_time_savings_rl_bl()


## fig. 8-2


def compare_time_savings_rlre_drl():
    number_of_cars = 100  # you can change to the current number of cars
    base_paths = {"drl": "store/for_hire/drl/drivers/smalldata", "rl": "store/for_hire/rl_relocation/drivers/smalldata"}
    time_savings = {"drl": {}, "rl": {}}

    for model, base_path in base_paths.items():
        for file_name in os.listdir(base_path):
            match = re.match(r"tripdata(\d{4}-\d{2}-\d{2})\.csv", file_name)
            if match:
                date = match.group(1)
                df = pd.read_csv(os.path.join(base_path, file_name))

                if "time_reduction" in df.columns:
                    total_time_reduction_seconds = df["time_reduction"].sum()
                    avg_time_savings_per_hour_per_car = (
                        total_time_reduction_seconds / 60 / 24
                    ) / number_of_cars
                    time_savings[model][date] = avg_time_savings_per_hour_per_car

    dates = sorted(set(time_savings["drl"].keys()) | set(time_savings["rl"].keys()))
    drl_savings = [time_savings["drl"].get(date, 0) for date in dates]
    rl_savings = [time_savings["rl"].get(date, 0) for date in dates]

    window_size = 5

    plt.figure(figsize=(10, 6))
    x = np.arange(len(dates))  # Use the full length of 'dates'

    color_drl = "cornflowerblue"
    color_rl = "goldenrod"

    plt.bar(x + 0.2, rl_savings, width=0.4, label="RLRE", color=color_rl)
    plt.bar(x - 0.2, drl_savings, width=0.4, label="DRL", color=color_drl)
    plt.axvline(x=13.5, ymin=0, ymax=0.7, color = "red", linestyle = '--', label = "left side training, right side testing")


    plt.ylim([0, 130])
    plt.xlabel("Date")
    plt.ylabel("Time saving (minutes)")
    plt.title("Time saving per car per hour (DRL vs RLRE)")
    plt.xticks(x, dates, rotation=45)
    plt.legend(loc ='upper right')
    plt.tight_layout()
    plt.savefig("store/plots/compare_time_savings_rlre_drl_100_paper.png")
    


#compare_time_savings_rlre_drl()


## fig. 8-3
def compare_time_savings_rl_rlre():
    number_of_cars = 2000  # you can change to the current number of cars
    base_paths = {
        "rl_relocation": "store/for_hire/rl_relocation",
        "rl": "store/for_hire/rl",
    }
    time_savings = {"rl_relocation": {}, "rl": {}}

    for model, base_path in base_paths.items():
        for file_name in os.listdir(base_path):
            match = re.match(r"tripdata(\d{4}-\d{2}-\d{2})\.csv", file_name)
            if match:
                date = match.group(1)
                df = pd.read_csv(os.path.join(base_path, file_name))

                if "time_reduction" in df.columns:
                    total_time_reduction_seconds = df["time_reduction"].sum()
                    avg_time_savings_per_hour_per_car = (
                        total_time_reduction_seconds / 60 / 24
                    ) / number_of_cars
                    time_savings[model][date] = avg_time_savings_per_hour_per_car

    dates = sorted(
        set(time_savings["rl_relocation"].keys()) | set(time_savings["rl"].keys())
    )
    rlre_savings = [time_savings["rl_relocation"].get(date, 0) for date in dates]
    rl_savings = [time_savings["rl"].get(date, 0) for date in dates]

    window_size = 3
    rlre_rolling_avg = custom_rolling_avg(np.array(rlre_savings), window_size)
    rl_rolling_avg = custom_rolling_avg(np.array(rl_savings), window_size)
    plt.figure(figsize=(10, 6))
    x = np.arange(len(dates))  # Use full length of 'dates'

    color_rlre = "darkgreen"
    color_rl = "orange"

    plt.bar(x + 0.2, rl_savings, width=0.4, label="RL", color=color_rl)
    plt.bar(
        x - 0.2, rlre_savings, width=0.4, label="RL with Relocation", color=color_rlre
    )

    plt.plot(
        x,
        rl_rolling_avg,
        label="RL (Moving Average)",
        color="orangered",
        marker="o",
        linestyle="-",
        markersize=5,
    )
    plt.plot(
        x,
        rlre_rolling_avg,
        label="RL with Relocation (Moving Average)",
        color="green",
        marker="o",
        linestyle="-",
        markersize=5,
    )

    plt.ylim([0, 200])
    plt.xlabel("Date")
    plt.ylabel("Time savings (minutes)")
    plt.title("Time savings per car per hour (RL vs RL with Relocation)")
    plt.xticks(x, dates, rotation=45)
    #plt.legend(loc = 'lower left')
    plt.tight_layout()
    plt.savefig("store/plots/compare_time_savings_rl_rlre_2000_poster.png")
    #


#compare_time_savings_rl_rlre()


def compare_time_savings_rl_bl_rl_relocation():
    #number_of_cars = 2000
    #base_paths = {"baseline": "store/for_hire/baseline", "rl": "store/for_hire/rl", "rl_relocation": "store/for_hire/rl_relocation"}
    number_of_cars = 100
    base_paths = {"baseline": "store/for_hire/baseline/drivers/100", "rl": "store/for_hire/rl/drivers/100", "rl_relocation": "store/for_hire/rl_relocation/drivers/100"}
    time_savings = {"baseline": {}, "rl": {}, "rl_relocation":{}}

    for model, base_path in base_paths.items():
        for file_name in os.listdir(base_path):
            match = re.match(r"tripdata(\d{4}-\d{2}-\d{2})\.csv", file_name)
            if match:
                date = match.group(1)
                df = pd.read_csv(os.path.join(base_path, file_name))
                if "time_reduction" in df.columns:
                    total_time_reduction_seconds = df["time_reduction"].sum()
                    avg_time_savings_per_hour_per_car = (
                        total_time_reduction_seconds / 60 / 24
                    ) / number_of_cars
                    time_savings[model][date] = avg_time_savings_per_hour_per_car

    dates = sorted(
        set(time_savings["baseline"].keys()) | set(time_savings["rl"].keys()) | set(time_savings["rl_relocation"].keys())
    )
    baseline_savings = [time_savings["baseline"].get(date, 0) for date in dates]
    rl_savings = [time_savings["rl"].get(date, 0) for date in dates]
    rl_relocation_savings = [time_savings["rl_relocation"].get(date, 0) for date in dates]
    window_size = 3

    # Using the custom function for the moving average
    baseline_rolling_avg = custom_rolling_avg(np.array(baseline_savings), window_size)
    rl_rolling_avg = custom_rolling_avg(np.array(rl_savings), window_size)
    rl_relocation_rolling_avg = custom_rolling_avg(np.array(rl_relocation_savings), window_size)
    plt.figure(figsize=(10, 6))
    x = np.arange(len(dates))  # Direct use of the full length of 'dates'

    color_baseline = "mediumseagreen"
    color_rl = "sienna"
    color_rl_relocation = "goldenrod"
    plt.bar(x -0.3, baseline_savings, width=0.3, label="Baseline", color=color_baseline)
    plt.bar(x , rl_savings, width=0.3, label="RL", color=color_rl)
    plt.bar(x + 0.3, rl_relocation_savings, width=0.3, label="RLRE", color=color_rl_relocation)
    plt.axvline(x=13.5, ymin=0, ymax=0.9, color = "red", linestyle = '--', label = "left side training, right side testing")


    plt.ylim([0, 200])

    plt.xlabel("Date")
    plt.ylabel("Time saving (minutes)")
    plt.title("Time saving per car per hour (BL vs RL vs RLRE)")
    plt.xticks(x, dates, rotation=45)
    plt.legend(loc ='lower right')
    plt.tight_layout()
    plt.savefig("store/plots/compare_time_savings_rl_bl_relocation_100_paper.png")
    


#compare_time_savings_rl_bl_rl_relocation()

# visualisation for the paper
def compare_time_savings_rl_bl_rl_relocation100ge2():
    # Initialization with a smaller number of cars and paths
    number_of_cars = 100
    base_paths = {
        "baseline": "store/for_hire/baseline/drivers/100",
        "rl": "store/for_hire/rl/drivers/100",
        "rl_relocation": "store/for_hire/rl_relocation/drivers/100"
    }
    time_savings = {"baseline": {}, "rl": {}, "rl_relocation": {}}

    # Read and process data
    for model, base_path in base_paths.items():
        for file_name in os.listdir(base_path):
            match = re.match(r"tripdata(\d{4}-\d{2}-\d{2})\.csv", file_name)
            if match:
                date = match.group(1)
                df = pd.read_csv(os.path.join(base_path, file_name))
                if "time_reduction" in df.columns:
                    total_time_reduction_seconds = df["time_reduction"].sum()
                    avg_time_savings_per_hour_per_car = (
                        total_time_reduction_seconds / 60 / 24
                    ) / number_of_cars
                    time_savings[model][date] = avg_time_savings_per_hour_per_car

    # Prepare data for visualization
    dates = sorted(set(time_savings["baseline"].keys()) | set(time_savings["rl"].keys()) | set(time_savings["rl_relocation"].keys()))
    baseline_savings = [time_savings["baseline"].get(date, 0) for date in dates]
    rl_savings = [time_savings["rl"].get(date, 0) for date in dates]
    rl_relocation_savings = [time_savings["rl_relocation"].get(date, 0) for date in dates]

    # Adjust the data for visualization (only every second day)
    dates_every_second_day = dates[::2]
    baseline_savings_every_second_day = baseline_savings[::2]
    rl_savings_every_second_day = rl_savings[::2]
    rl_relocation_savings_every_second_day = rl_relocation_savings[::2]
    x_every_second_day = np.arange(len(dates_every_second_day))

    # Visualization
    plt.figure(figsize=(5, 5))
    color_baseline = "mediumseagreen"
    color_rl = "sienna"
    color_rl_relocation = "goldenrod"
    plt.bar(x_every_second_day - 0.3, baseline_savings_every_second_day, width=0.3, label="Baseline", color=color_baseline)
    plt.bar(x_every_second_day, rl_savings_every_second_day, width=0.3, label="QL", color=color_rl)
    plt.bar(x_every_second_day + 0.3, rl_relocation_savings_every_second_day, width=0.3, label="QLRE", color=color_rl_relocation)
    plt.axvline(x=6.5, ymin=0, ymax=0.9, color = "red", linestyle = '--', label = "left side training, right side testing")
    plt.ylim([0, 180])
    plt.tick_params(axis='y', labelsize='large')
    plt.tick_params(axis='x', labelsize='large')
    plt.xlabel("Date",size = 15)
    plt.ylabel("Time saving (minutes)", size = 15 )
    plt.title("100 vehicles ",size = 15, pad = 84)
    plt.xticks(x_every_second_day, dates_every_second_day, rotation=45)
    plt.legend(fontsize = "large", loc=(0.06, 1.01),ncol =1)
       #plt.legend(loc='upper center',fontsize = "large", bbox_to_anchor = (0.5, 1.71),ncol =1)
    plt.tight_layout()
    plt.savefig("store/plots/compare_time_savings_rl_bl_relocation_100_paper12.png")


# visualisation for the paper
def compare_time_savings_rl_bl_rl_relocation2000ge2():
    # Initialization with a smaller number of cars and paths
    number_of_cars = 2000
    base_paths = {"baseline": "store/for_hire/baseline", "rl": "store/for_hire/rl", "rl_relocation": "store/for_hire/rl_relocation"}
    time_savings = {"baseline": {}, "rl": {}, "rl_relocation": {}}

    # Read and process data
    for model, base_path in base_paths.items():
        for file_name in os.listdir(base_path):
            match = re.match(r"tripdata(\d{4}-\d{2}-\d{2})\.csv", file_name)
            if match:
                date = match.group(1)
                df = pd.read_csv(os.path.join(base_path, file_name))
                if "time_reduction" in df.columns:
                    total_time_reduction_seconds = df["time_reduction"].sum()
                    avg_time_savings_per_hour_per_car = (
                        total_time_reduction_seconds / 60 / 24
                    ) / number_of_cars
                    time_savings[model][date] = avg_time_savings_per_hour_per_car

    # Prepare data for visualization
    dates = sorted(set(time_savings["baseline"].keys()) | set(time_savings["rl"].keys()) | set(time_savings["rl_relocation"].keys()))
    baseline_savings = [time_savings["baseline"].get(date, 0) for date in dates]
    rl_savings = [time_savings["rl"].get(date, 0) for date in dates]
    rl_relocation_savings = [time_savings["rl_relocation"].get(date, 0) for date in dates]

    # Adjust the data for visualization (only every second day)
    dates_every_second_day = dates[::2]
    baseline_savings_every_second_day = baseline_savings[::2]
    rl_savings_every_second_day = rl_savings[::2]
    rl_relocation_savings_every_second_day = rl_relocation_savings[::2]
    x_every_second_day = np.arange(len(dates_every_second_day))
    
    # Visualization
    plt.figure(figsize=(5, 5))
    color_baseline = "mediumseagreen"
    color_rl = "sienna"
    color_rl_relocation = "goldenrod"
    plt.bar(x_every_second_day - 0.3, baseline_savings_every_second_day, width=0.3, label="Baseline", color=color_baseline)
    plt.bar(x_every_second_day, rl_savings_every_second_day, width=0.3, label="QL", color=color_rl)
    plt.bar(x_every_second_day + 0.3, rl_relocation_savings_every_second_day, width=0.3, label="QLRE", color=color_rl_relocation)
    plt.axvline(x=6.5, ymin=0, ymax=0.9, color = "red", linestyle = '--', label = "left side training, right side testing")
    plt.ylim([0, 180])
    plt.tick_params(axis='y', labelsize='large')
    plt.tick_params(axis='x', labelsize='large')
    plt.xlabel("Date",size = 15)
    plt.ylabel("Time saving (minutes)", size = 15 )
    plt.title("2000 vehicles ",size = 15, pad = 84)
    plt.xticks(x_every_second_day, dates_every_second_day, rotation=45)
    plt.legend(loc=(0.06, 1.01), fontsize = "large",ncol =1)
    #plt.legend(fontsize = "large", bbox_to_anchor = (0.31, 0.9700),ncol =1)
    plt.tight_layout()
    plt.savefig("store/plots/compare_time_savings_rl_bl_relocation_2000_paper12.png")
    


#compare_time_savings_rl_bl_rl_relocation2000ge2()
