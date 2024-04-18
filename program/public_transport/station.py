from program.location.location import Location
from program.utils import IdProvider

ID_PROVIDER = IdProvider()

class Station:
    def __init__(self, id: int, position: Location, name: str) -> None:
        self.id = id
        self.position = position
        self.name = name