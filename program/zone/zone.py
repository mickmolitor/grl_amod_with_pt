from __future__ import annotations
from program.location.location import Location

class Zone:
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
    
    def is_empty(self) -> bool:
        return self.id == 9999
