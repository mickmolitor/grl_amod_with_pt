from __future__ import annotations
import csv
from program.location.location import Location
from program.logger import LOGGER
from program.public_transport.station import Station

# Singleton class containing the global fastest station connections
class FastestStationConnectionNetwork:
    _connection_network: FastestStationConnectionNetwork = None

    def get_instance():
        if FastestStationConnectionNetwork._connection_network == None:
            LOGGER.debug("Starting to create fastest connection network")

            line_id_to_station_id: dict[int, list[int]] = {}
            id_to_station_dict: dict[int, Station] = {}

            with open("data/continuous_subway_data.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    line_id = row["line"]
                    station_name = row["station_name"]
                    lat = float(row["LAT"])
                    long = float(row["LONG"])
                    station_id = int(row["ID"])

                    if station_id not in id_to_station_dict:
                        id_to_station_dict[station_id] = Station(station_id, Location(lat, long), station_name)
                    if line_id not in line_id_to_station_id:
                        line_id_to_station_id[line_id] = []
                    line_id_to_station_id[line_id].append(station_id)
            
            from program.public_transport.line import Line
            lines = []
            for line_id in line_id_to_station_id:
                lines.append(Line(list(map(lambda station_id: id_to_station_dict[station_id], line_id_to_station_id[line_id])), line_id))
            stations = list(sorted(id_to_station_dict.values(), key=lambda x: x.id))

            fastest_connections: list[tuple[int, int, list[Station], float]] = []

            with open("data/shortest_paths.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    start_id = int(row["start_station"])
                    end_id = int(row["end_station"])
                    connections = list(map(lambda x: id_to_station_dict[int(x)], row["connection"].split(" -> ")[0].strip("][").split(", ")))
                    travel_time = float(row["connection"].split(" -> ")[1])
                    fastest_connections.append((start_id, end_id, connections, travel_time))

            FastestStationConnectionNetwork._connection_network = FastestStationConnectionNetwork(fastest_connections, stations, lines)
            LOGGER.debug("Finished to create fastest connection network")

        return FastestStationConnectionNetwork._connection_network

    def __init__(self, fastest_connections: list[tuple[Station, Station, list[Station], float]], stations: list[Station], lines) -> None:

        from program.public_transport.line import Line
        self.lines: list[Line] = lines
        self.stations = stations

        self.connection_network: dict[int, dict[int, tuple[list[Station], float]]] = {}
        for connection in fastest_connections:
            start_id = connection[0] if connection[0] <= connection[1] else connection[1]
            end_id = connection[1] if connection[0] <= connection[1] else connection[0]

            if start_id not in self.connection_network:
                self.connection_network[start_id] = {}

            self.connection_network[start_id][end_id] = (connection[2], connection[3])

    # Returns: tuple[List of stations, transit time]
    def get_fastest_connection(self, start: Station, end: Station) -> tuple[list[Station], float]:
        start_id = start.id if start.id <= end.id else end.id
        end_id = end.id if start.id <= end.id else start.id

        return self.connection_network[start_id][end_id]