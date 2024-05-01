from __future__ import annotations
import os
import torch

from program.action.action import Action
from program.action.vehicle_action_pair import VehicleActionPair
from program.graph_reinforcement_learning.main_network import MainNetwork
from program.graph_reinforcement_learning.target_network import TargetNetwork
from program.graph_reinforcement_learning.temporal_difference_loss import (
    TemporalDifferenceLoss,
)
from program.interval.time import Time
from program.zone.zone import Zone
from program.logger import LOGGER

from params.program_params import ProgramParams
from program.zone.zone_graph import ZoneGraph
from program.zone.zones import Zones


class StateValueNetworks:
    _state_value_networks = None

    def get_instance() -> StateValueNetworks:
        if StateValueNetworks._state_value_networks == None:
            StateValueNetworks._state_value_networks = StateValueNetworks()
        return StateValueNetworks._state_value_networks

    def __init__(self) -> None:
        self.main_net = MainNetwork()
        self.target_net = TargetNetwork()
        self.loss_fn = TemporalDifferenceLoss()

        self.iteration = 0

    def get_target_state_value(self, action: Action, zone: Zone, time: Time) -> float:
        return self.target_net.get_state_value(action, zone, time)

    def initialize_iteration(self) -> None:
        from program.state.state import State
        self.main_net.clear()
        self.target_net.clear()

        if self.iteration % ProgramParams.MAIN_AND_TARGET_NET_SYNC_ITERATIONS == 0:
            LOGGER.debug("Transfer weights from main to target network")
            self.target_net.load_GNN_state_dict(self.main_net.get_GNN_state_dict())
            self.target_net.load_DNN_state_dict(self.main_net.get_DNN_state_dict())

        self.main_net.optimizer_zero_grad()
        state = State.get_state()
        zone_graph = ZoneGraph.get_instance()
        zone_to_features = {}
        # Update zone graph
        for zone in Zones.get_zones():
            if zone.is_empty():
                continue
            current_orders = state.get_current_order_quota(zone)
            last_orders = state.get_last_order_quota(zone)
            idle = state.get_idle_vehicle_quota(zone)
            occupied = state.get_occupied_vehicle_quota(zone)
            average_reduction = state.average_time_reduction_per_interval_per_zone[state.current_interval][zone].average_time_reduction
            zone_to_features[zone] = ZoneGraph.Feature(
                current_orders, last_orders, occupied, idle, average_reduction
            )
        zone_graph.update_features(zone_to_features)
        self.main_net.calculate_graph_embedding(
            zone_graph.get_edge_index(), zone_graph.get_feature_index()
        )
        self.target_net.calculate_graph_embedding(
            zone_graph.get_edge_index(), zone_graph.get_feature_index()
        )

    # We want a list of action tuples here since the error function is calculated in each iteration for all changes
    def adjust_state_values(
        self, action_reward_tuples: list[tuple[Zone, VehicleActionPair, float]]
    ) -> None:
        from program.state.state import State
        
        # Only update network weights if there are vehicle action matches
        if len(action_reward_tuples) > 0:
            # Calculate main values
            for tup in action_reward_tuples:
                self.main_net.get_state_value(tup[1].action, tup[0], State.get_state().current_time)

            td_values = []
            for tup in action_reward_tuples:
                td_values.append(
                    {
                        "reward": tup[2],
                        "main_value": self.main_net.get_state_value_by_action_id(
                            tup[1].action.id
                        ),
                        "target_value": self.target_net.get_state_value_by_action_id(
                            tup[1].action.id
                        ),
                        "discount_value": ProgramParams.DISCOUNT_FACTOR(
                            tup[1].get_total_vehicle_travel_time_in_seconds()
                        ),
                    }
                )

            LOGGER.debug("Backward propagation and optimization")
            # Backward and optimize
            self.main_net.optimizer_zero_grad()
            # Compute loss
            loss = self.loss_fn(td_values)
            LOGGER.debug(f"Temporal difference error: {float(loss)}")
            loss.backward()
            self.main_net.optimizer_step()

        self.iteration += 1

    def import_weights(self) -> None:
        # Main networks
        if os.path.exists("training_data/main_net_GNN_state_dict.pth"):
            self.main_net.load_GNN_state_dict(
                torch.load("training_data/main_net_GNN_state_dict.pth")
            )
        if os.path.exists("training_data/main_net_DNN_state_dict.pth"):
            self.main_net.load_DNN_state_dict(
                torch.load("training_data/main_net_DNN_state_dict.pth")
            )

        # Target networks
        if os.path.exists("training_data/target_net_GNN_state_dict.pth"):
            self.target_net.load_GNN_state_dict(
                torch.load("training_data/target_net_GNN_state_dict.pth")
            )
        elif os.path.exists("training_data/main_net_GNN_state_dict.pth"):
            self.target_net.load_GNN_state_dict(
                torch.load("training_data/main_net_GNN_state_dict.pth")
            )
        if os.path.exists("training_data/target_net_DNN_state_dict.pth"):
            self.target_net.load_DNN_state_dict(
                torch.load("training_data/target_net_DNN_state_dict.pth")
            )
        elif os.path.exists("training_data/main_net_DNN_state_dict.pth"):
            self.target_net.load_DNN_state_dict(
                torch.load("training_data/main_net_DNN_state_dict.pth")
            )

    def export_weights(self) -> None:
        # Main networks
        torch.save(
            self.main_net.get_GNN_state_dict(),
            "training_data/main_net_GNN_state_dict.pth",
        )
        torch.save(
            self.main_net.get_DNN_state_dict(),
            "training_data/main_net_DNN_state_dict.pth",
        )

        # Target networks
        torch.save(
            self.target_net.get_GNN_state_dict(),
            "training_data/target_net_GNN_state_dict.pth",
        )
        torch.save(
            self.target_net.get_DNN_state_dict(),
            "training_data/target_net_DNN_state_dict.pth",
        )

    def raze_weights() -> None:
        # Delete files with weights
        if os.path.exists("training_data/main_net_DNN_state_dict.pth"):
            os.remove("training_data/main_net_DNN_state_dict.pth")
        if os.path.exists("training_data/main_net_GNN_state_dict.pth"):
            os.remove("training_data/main_net_GNN_state_dict.pth")
        if os.path.exists("training_data/target_net_DNN_state_dict.pth"):
            os.remove("training_data/target_net_DNN_state_dict.pth")
        if os.path.exists("training_data/target_net_GNN_state_dict.pth"):
            os.remove("training_data/target_net_GNN_state_dict.pth")
