from program.location.location import Location
from program.location.zone import Zone
from program.utils import IdProvider

ID_PROVIDER = IdProvider()

class GridCell:
    def __init__(self, center: Location, zone: Zone) -> None:
        self.id = ID_PROVIDER.get_id()
        self.center = center
        self.zone = zone

    def is_empty(self) -> bool:
        return self.zone.id == 9999