
import csv
from program.grid.grid import Grid
from program.zone.zone import Zone


def create_zone_graph() -> None:
    grid = Grid.get_instance()

    # ordered by zone id -> smaller id -> larger id -> weight
    adjacent_zones_dict: dict[Zone: dict[Zone: float]] = {}

    for i in range(len(grid.cells)):
        for j in range(len(grid.cells[i])):
            if grid.cells[i][j].is_empty():
                continue
            # Check right and downer adjacent cell if there is another zone
            if i < len(grid.cells) - 1 and grid.cells[i][j].zone != grid.cells[i + 1][j].zone:
                if not grid.cells[i + 1][j].is_empty():
                    c_zone = grid.cells[i][j].zone
                    o_zone = grid.cells[i + 1][j].zone
                    
                    if c_zone.id < o_zone.id:
                        if c_zone.id not in adjacent_zones_dict:
                            adjacent_zones_dict[c_zone.id] = {}
                        adjacent_zones_dict[c_zone.id][o_zone.id] = c_zone.central_location.distance_to(o_zone.central_location)
                    else:
                        if o_zone.id not in adjacent_zones_dict:
                            adjacent_zones_dict[o_zone.id] = {}
                        adjacent_zones_dict[o_zone.id][c_zone.id] = c_zone.central_location.distance_to(o_zone.central_location)
            
            elif j < len(grid.cells[i]) - 1 and grid.cells[i][j].zone != grid.cells[i][j + 1].zone:
                if not grid.cells[i][j + 1].is_empty(): 
                    c_zone = grid.cells[i][j].zone
                    o_zone = grid.cells[i][j + 1].zone
                    
                    if c_zone.id < o_zone.id:
                        if c_zone.id not in adjacent_zones_dict:
                            adjacent_zones_dict[c_zone.id] = {}
                        adjacent_zones_dict[c_zone.id][o_zone.id] = c_zone.central_location.distance_to(o_zone.central_location)
                    else:
                        if o_zone.id not in adjacent_zones_dict:
                            adjacent_zones_dict[o_zone.id] = {}
                        adjacent_zones_dict[o_zone.id][c_zone.id] = c_zone.central_location.distance_to(o_zone.central_location)
    
    adjacent_zones_list: list[tuple[int, int, float]] = []

    for zone1_id in adjacent_zones_dict:
        for zone2_id in adjacent_zones_dict[zone1_id]:
            adjacent_zones_list.append((zone1_id, zone2_id, adjacent_zones_dict[zone1_id][zone2_id]))
    
    with open("data/zone_graph.csv", mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["zone1_id", "zone2_id", "weight"])

        for tup in adjacent_zones_list:
            writer.writerow(tup)

def fix_zone_graph():
    fixed = []
    zones = Zone.get_zones()
    with open("data/zone_graph.csv", mode="r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["weight"] == "XXX":
                zone1 = list(filter(lambda x: x.id == int(row["zone1_id"]), zones))[0]
                zone2 = list(filter(lambda x: x.id == int(row["zone2_id"]), zones))[0]
                weight = zone1.central_location.distance_to(zone2.central_location)
                fixed.append((zone1.id, zone2.id, weight))
            else:
                fixed.append((int(row["zone1_id"]), int(row["zone2_id"]), float(row["weight"])))
    
    with open("data/zone_graph.csv", mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["zone1_id", "zone2_id", "weight"])

        for tup in fixed:
            writer.writerow(tup)
