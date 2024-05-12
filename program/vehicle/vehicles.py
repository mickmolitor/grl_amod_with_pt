import csv
from program.vehicle.vehicle import Vehicle
from program.grid.grid import Grid
from program.location.location import Location


# Singleton class containing all the vehicles
class Vehicles:
    _vehicles: list[Vehicle] = None

    def get_vehicles() -> list[Vehicle]:
        if Vehicles._vehicles == None:
            Vehicles._vehicles = []
            with open("input_data/vehicles.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    id = int(row["vehicle_id"])
                    location = Location(float(row["lat"]), float(row["lon"]))
                    Vehicles._vehicles.append(Vehicle(location, id=id))

        return Vehicles._vehicles

    def export_vehicles() -> None:
        vehicles = Vehicles.get_vehicles()
        with open("input_data/vehicles.csv", mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(["vehicle_id", "lat", "lon"])
            for vehicle in vehicles:
                writer.writerow(
                    [
                        vehicle.id,
                        vehicle.current_position.lat,
                        vehicle.current_position.lon,
                    ]
                )
    
    def raze_vehicles():
        Vehicles._vehicles = None
