import torch.nn as nn

class DeepNeuralNetwork(nn.Sequential):
    def __init__(self):
        # State features +  graph embedding features
        super(DeepNeuralNetwork, self).__init__(
            nn.Linear(7 + 20, 100), nn.ReLU(), nn.Linear(100, 100), nn.ReLU(), nn.Linear(100, 1)
        )