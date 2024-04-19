import torch.nn as nn

class DeepNeuralNetwork(nn.Sequential):
    def __init__(self):
        # State features + action features + 2 * graph embedding features
        super(DeepNeuralNetwork, self).__init__(
            nn.Linear(7 + 7 + 20 * 2, 100), nn.ReLU(), nn.Linear(100, 100), nn.ReLU(), nn.Linear(100, 1)
        )