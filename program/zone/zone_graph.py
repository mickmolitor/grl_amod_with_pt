from __future__ import annotations
from collections import namedtuple
import csv

from program.zone.zone import Zone


class ZoneGraph:
    Feature = namedtuple(
        "Feature",
        [
            "num_orders_now",
            "num_orders_before",
            "num_occupied",
            "num_idle",
            "average_time_reduction",
        ],
    )

    _zone_graph: ZoneGraph = None

    def get_instance() -> ZoneGraph:
        if ZoneGraph._zone_graph == None:
            current_index = 0
            edge_list = []
            zone_to_node = {}
            with open("data/zone_graph.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    zone1_id = int(row["zone1_id"])
                    if not zone1_id in zone_to_node:
                        zone_to_node[zone1_id] = current_index
                        current_index += 1
                    zone2_id = int(row["zone2_id"])
                    if not zone2_id in zone_to_node:
                        zone_to_node[zone2_id] = current_index
                        current_index += 1

                    edge_list.append((zone_to_node[zone1_id], zone_to_node[zone2_id]))

            ZoneGraph._zone_graph = ZoneGraph(edge_list, zone_to_node)
        return ZoneGraph._zone_graph

    def __init__(
        self, edge_list: list[tuple[int, int]], zone_to_node: dict[int, int]
    ) -> None:
        self.edge_list = edge_list
        self.zone_to_node = zone_to_node
        self.features: list[ZoneGraph.Feature] = [
            ZoneGraph.Feature(0, 0, 0, 0, 0) for i in range(len(zone_to_node))
        ]

    def update_features(self, zone_to_feature: dict[Zone, ZoneGraph.Feature]) -> None:
        for zone in zone_to_feature:
            self.features[self.zone_to_node[zone.id]] = zone_to_feature[zone]

    def get_edge_index(self) -> list[tuple[int, int]]:
        start_nodes = []
        end_nodes = []
        for tup in self.edge_list:
            start_nodes.append(tup[0])
            end_nodes.append(tup[1])
        return (start_nodes, end_nodes)

    def get_feature_index(self) -> list[tuple[int, int, int, int, float]]:
        feature_matrix = []
        for feature in self.features:
            feature_matrix.append(
                (
                    feature.num_orders_now,
                    feature.num_orders_before,
                    feature.num_occupied,
                    feature.num_idle,
                    feature.average_time_reduction,
                )
            )
        return feature_matrix
    
    def get_feature(self, zone: Zone) -> ZoneGraph.Feature:
        return self.features[self.zone_to_node[zone.id]]

    def get_node_id(self, zone: Zone) -> int:
        return self.zone_to_node[zone.id]
