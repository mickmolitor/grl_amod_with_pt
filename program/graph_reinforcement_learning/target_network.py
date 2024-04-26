import torch
from program.action.action import Action
from program.graph_reinforcement_learning.deep_q_network import DeepQNetwork
from program.interval.time import Time
from program.zone.zone import Zone


class TargetNetwork(DeepQNetwork):
    def __init__(self) -> None:
        super(TargetNetwork, self).__init__()

        # Set target networks to eval mode
        self.graph_sage.eval()
        self.dnn.eval()
    
    def get_state_value(
        self, action: Action, zone: Zone, time: Time
    ) -> float:
        # Prevent backward propagation to effect target network weights
        with torch.no_grad():
            state_value = super(TargetNetwork, self).get_state_value(action, zone, time)
        return state_value
    
    def calculate_graph_embedding(self, edge_index: tuple[list[int], list[int]], features: list[tuple[int, int, int, int, float]]) -> None:
        # Prevent backward propagation to effect target network weights
        with torch.no_grad():
            super(TargetNetwork, self).get_state_value(edge_index, features)