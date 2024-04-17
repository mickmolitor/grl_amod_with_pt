from __future__ import annotations
import csv
import sys
from program.location.location import Location
from program.logger import LOGGER
import shapely

# csv.field_size_limit(sys.maxsize)
if sys.maxsize > 2**32:
    csv.field_size_limit(2**31 - 1)  # für 64-Bit-Systeme
else:
    csv.field_size_limit(2**15 - 1)


# We have the problem that zones not all the time match some straight lines
# We define our zones as sets of smaller squares where it is super easy to
# find the fitting square in a coordinate system (2-layer binary search)
# Initial setup in static_data_generation/grid_builder.py
class Zone:
    _zones: list[Zone] = None

    def get_zones() -> list[Zone]:
        if Zone._zones == None:
            LOGGER.debug("Starting to create zones")
            Zone._zones = []

            with open("data/zones.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Zone._zones.append(
                        Zone(
                            int(row["zone_id"]),
                            Location(
                                float(row["zone_center_lat"]),
                                float(row["zone_center_lon"]),
                            ),
                        )
                    )

            LOGGER.debug("Finished to create zones")

            zone_by_id = {zone.id: zone for zone in Zone._zones}

            LOGGER.debug("Set adjacent zones")
            csv_file_path = "data/zone_neighborhoods_by_extended_distance.csv"
            with open(csv_file_path, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    zone_id = int(row["zone_id"])

                    if zone_id not in zone_by_id:
                        continue

                    zone = zone_by_id[zone_id]

                    for i in range(1, 21):
                        zone.adjacent_zones_dict[i].extend(
                            list(
                                filter(
                                    lambda x: x in zone_by_id,
                                    map(
                                        lambda x: int(x),
                                        filter(
                                            lambda x: x != "",
                                            row[f"{i}"].strip("][").split(", "),
                                        ),
                                    ),
                                )
                            )
                        )

        return Zone._zones

    def __init__(self, id: int, central_location: Location) -> None:
        self.id: int = id
        self.central_location: Location = central_location
        self.adjacent_zones_dict: dict[int, list[int]] = {i: [] for i in range(1, 21)}

    # distance in meters
    def find_adjacent_zone_ids(self, distance: int) -> list[int]:
        zones = []
        for i in range(1, (distance // 1000) + 1):
            zones.extend(self.adjacent_zones_dict[i])

        return zones
