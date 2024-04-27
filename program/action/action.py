from program.utils import IdProvider

ID_PROVIDER = IdProvider()

class Action:
    from program.order.route import Route

    def __init__(self, route: Route) -> None:
        self.id = ID_PROVIDER.get_id()
        self.route = route

    def is_idling(self) -> bool:
        return self.route is None

    def is_route(self) -> bool:
        return not self.route is None

    def __str__(self):
        return f"{f'Route {self.route.id}' if self.is_route() else 'Idling'}"
