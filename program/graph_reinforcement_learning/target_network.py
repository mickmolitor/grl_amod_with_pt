from program.graph_reinforcement_learning.deep_q_network import DeepQNetwork


class TargetNetwork(DeepQNetwork):
    def __init__(self) -> None:
        super(TargetNetwork, self).__init__()

        # Set target networks to eval mode
        self.graph_sage.eval()
        self.dnn.eval()