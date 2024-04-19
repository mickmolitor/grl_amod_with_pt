from __future__ import annotations
from program.interval.time import Time
from program.zone.zone import Zone
from params.program_params import ProgramParams
from program.utils import IdProvider
from program.location.location import Location

ID_PROVIDER = IdProvider()


class Order:
    def __init__(
        self, dispatch_time: Time, start: Location, end: Location, zone: Zone
    ) -> None:
        self.id = ID_PROVIDER.get_id()
        self.dispatch_time = dispatch_time
        self.start = start
        self.end = end
        self.zone = zone
        # Initialized as not dispatched
        self.expires = None
        self.direct_connection = None

    def dispatch(self) -> None:
        self.expires = ProgramParams.ORDER_EXPIRY_DURATION

        # Init fastest connection with walking speed
        fastest_connection = (
            [],
            self.start.distance_to(self.end) / ProgramParams.WALKING_SPEED,
        )
        from public_transport.fastest_station_connection_network import (
            FastestStationConnectionNetwork,
        )

        fastest_connection_network = FastestStationConnectionNetwork.get_instance()

        # 1. Get the closest start and end station for each line
        from public_transport.station import Station

        origins: list[Station] = []
        destinations: list[Station] = []
        for line in fastest_connection_network.lines:
            origins.append(line.get_closest_station(self.start))
            destinations.append(line.get_closest_station(self.end))

        # 2. Find the most fastest connection without any autonomous on-demand services
        for origin in origins:
            for destination in destinations:
                if origin == destination:
                    continue
                connection = fastest_connection_network.get_fastest_connection(
                    origin, destination
                )
                walking_time = (
                    self.start.distance_to(origin.position)
                    + destination.position.distance_to(self.end)
                ) / ProgramParams.WALKING_SPEED
                # include entry, exit and waiting time
                other_time = (
                    2 * ProgramParams.PUBLIC_TRANSPORT_ENTRY_EXIT_TIME
                    + ProgramParams.PUBLIC_TRANSPORT_WAITING_TIME(self.dispatch_time)
                )
                total_additional_time = walking_time + other_time
                if fastest_connection[1] > total_additional_time + connection[1]:
                    fastest_connection = (
                        connection[0],
                        connection[1] + total_additional_time,
                    )

        self.direct_connection: tuple[list[Station], float] = fastest_connection
