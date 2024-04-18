import csv
import random
from params.program_params import ProgramParams
from program.grid.grid import Grid
from program.interval.time import Time
from program.logger import LOGGER
from program.order.order import Order


class Orders:
    _orders_by_time: dict[Time, list[Order]] = None

    # Resets the orders
    def reset() -> None:
        Orders._orders_by_time = None

    def get_orders_by_time() -> dict[Time, list[Order]]:
        if Orders._orders_by_time == None:
            Orders._orders_by_time = {
                Time(hour, minute): [] for minute in range(60) for hour in range(24)
            }
            with open(ProgramParams.ORDERS_FILE_PATH(), mode="r") as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    if i % 50000 == 0:
                        LOGGER.debug(f"Processed {(i // 50000)*50000} orders...")
                    # Extract hour and minute from the pickup datetime
                    hour = int(row["pickup_time"][0:2])
                    minute = int(row["pickup_time"][3:5])
                    # Create a tuple of Pickup and Dropoff Zone IDs
                    pu_zone_id = int(row["PULocationID"])
                    do_zone_id = int(row["DOLocationID"])
                    order = Order(
                        Time(hour, minute),
                        random.Random(i)
                        .choice(Grid.get_instance().cells_dict[pu_zone_id])
                        .center,
                        random.Random(i + 1)
                        .choice(Grid.get_instance().cells_dict[do_zone_id])
                        .center,
                        Grid.get_instance().zones_dict[pu_zone_id],
                    )
                    Orders._orders_by_time[Time(hour, minute)].append(order)
        return Orders._orders_by_time