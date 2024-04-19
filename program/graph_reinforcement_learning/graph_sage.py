import torch.nn as nn
import torch_geometric.nn as nn_geo

class GraphSAGE(nn.Sequential):
    def __init__(self):
        super(GraphSAGE, self).__init__(
            nn_geo.SAGEConv(5, 10, aggr="add"), nn.ReLU(), nn_geo.SAGEConv(10, 20, aggr="add"), nn.ReLU()
        )

# class ModGraphSAGE(torch.nn.Module):
#     def __init__(self):
#         super(ModGraphSAGE, self).__init__()
#         self.sage1 = SAGEConv(5, 10, aggr="add")
#         self.sage2 = SAGEConv(10, 20, aggr="add")

        
#         self.linear1 = Linear(7 + 7 + 20 * 2, 100)
#         self.linear2 = Linear(100, 100)
#         self.linear3 = Linear(100, 1)

#     # state_features: [origin zone id, current time, # of orders in origin, # of available orders in origin last interval,
#     #                   # of idle vehicles in origin, # of occupied vehicles in origin]
#     # action_features: [destination zone id, travel time, # of orders in destination, # of available orders in destination last interval,
#     #                   # of idle vehicles in destination, # of occupied vehicles in destination]
#     def forward(self, data: Data, state_features: Tensor, action_features: Tensor):
#         # Forward pass through GraphSAGE
#         x = self.sage1(data.x, data.edge_index)
#         x = F.relu(x)
#         x = self.sage2(x, data.edge_index)
#         x = F.relu(x)

#         # Combine SAGEConv output with other features
#         combined_features = torch.cat(
#             [state_features, action_features, x], dim=1
#         )

#         # Forward pass through DNN
#         x = self.linear1(combined_features)
#         x = F.relu(x)
#         x = self.linear2(combined_features)
#         x = F.relu(x)
        
#         return self.linear3(combined_features)
