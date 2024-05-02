import csv
import os
import random
from program.grid.grid import Grid
from program.interval.time import Time
from program.order.orders import Orders
from params.program_params import ProgramParams
from program.vehicle.vehicle import Vehicle


def initialize_vehicle_positions() -> None:
    # We do a similar approach as in the Feng et al. (2022) paper: 
    # the distribution of vehicles positions follows the distribution 
    # of orders in the first 30min of the studied period.
    # In our case we randomly take orders from the first 30mins 
    # and do a one to one mapping with vehicles, where each vehicle 
    # is positioned randomly in a radius of two GridCells from the order.
    grid = Grid.get_instance()
    orders_by_time = Orders.get_orders_by_time()
    first_orders = []
    for minute in range(30):
        first_orders.extend(orders_by_time[Time.of_total_minutes(minute)])
    sampled_orders = random.Random(42).choices(first_orders, k=ProgramParams.AMOUNT_OF_VEHICLES)

    counter = 0
    vehicles = []
    for order in sampled_orders:
        cell = grid.find_cell(order.start)
        cells = list(filter(lambda x: not x.is_empty(), grid.find_n_adjacent_cells(cell, 2)))
        vehicle_cell = random.Random(counter).choice(cells)
        vehicles.append(Vehicle(vehicle_cell.center))
        counter += 1
    if not os.path.exists("input_data"):
        os.makedirs("input_data")
    with open("input_data/vehicles.csv", mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["vehicle_id", "lat", "lon"])
        for vehicle in vehicles:
            writer.writerow(
                [
                    vehicle.id,
                    vehicle.current_position.lat,
                    vehicle.current_position.lon,
                ]
            )