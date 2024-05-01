from program.interval.time import Time
from program.utils import IdProvider

ID_PROVIDER = IdProvider()

# Intervals work inclusive -> 12:33:22 part of 12:33
class GridInterval:
    def __init__(self, start: Time, end: Time) -> None:
        self.id = ID_PROVIDER.get_id()
        self.start = start
        self.end = end