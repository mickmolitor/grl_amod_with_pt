import csv
from program.location.location import Location
from program.logger import LOGGER
from program.zone.zone import Zone

# We have the problem that zones not all the time match some straight lines
# We define our zones as sets of smaller squares where it is super easy to
# find the fitting square in a coordinate system (2-layer binary search)
# Initial setup in static_data_generation/grid_builder.py
class Zones:
    _zones: list[Zone] = None

    def get_zones() -> list[Zone]:
        if Zones._zones == None:
            LOGGER.debug("Starting to create zones")
            Zones._zones = []

            with open("data/zones.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Zones._zones.append(
                        Zone(
                            int(row["zone_id"]),
                            Location(
                                float(row["zone_center_lat"]),
                                float(row["zone_center_lon"]),
                            ),
                        )
                    )

            LOGGER.debug("Finished to create zones")

            zone_by_id = {zone.id: zone for zone in Zones._zones}

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

        return Zones._zones
