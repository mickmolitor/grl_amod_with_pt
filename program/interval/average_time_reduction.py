from program.interval.grid_interval import GridInterval
from program.zone.zone import Zone


class AverageTimeReduction:
    def __init__(
        self,
        grid_interval: GridInterval,
        zone: Zone,
        average_time_reduction: float,
        amount_orders: int,
    ) -> None:
        self.grid_interval = grid_interval
        self.zone = zone
        self.average_time_reduction = average_time_reduction
        self.amount_orders = amount_orders

    def update(self, time_reduction: float) -> None:
        self.average_time_reduction = (
            self.average_time_reduction * self.amount_orders + time_reduction
        ) / (self.amount_orders + 1)
        self.amount_orders += 1
