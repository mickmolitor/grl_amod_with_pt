import math
from program.graph_reinforcement_learning.deep_state_network import DeepStateNetwork
import torch.optim as optim

class MainNetwork(DeepStateNetwork):

    def __init__(self) -> None:
        super(MainNetwork, self).__init__()
        
        # Set main networks to train mode
        self.graph_sage.train()
        self.dnn.train()

        # Optimizer
        self.optimizer_dnn = optim.Adam(self.dnn.parameters(), lr=3 * math.exp(-4))
        self.optimizer_gnn = optim.Adam(
            self.graph_sage.parameters(), lr=3 * math.exp(-4)
        )
    
    def optimizer_zero_grad(self) -> None:
        self.optimizer_dnn.zero_grad()
        self.optimizer_gnn.zero_grad()
    
    def optimizer_step(self) -> None:
        self.optimizer_dnn.step()
        self.optimizer_gnn.step()