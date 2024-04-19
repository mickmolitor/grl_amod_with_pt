from torch_geometric.data import Data
from torch_geometric.nn import SAGEConv
from torch_geometric.utils import to_undirected
import torch

def test_graph_sage():
    if torch.cuda.is_available():
        device = torch.device('cpu')
        print("Using GPU:", torch.cuda.get_device_name(0))
    else:
        device = torch.device('cpu')
        print("GPU not available, using CPU instead.")
    # Kanten des Graphen (ungerichtet)
    edge_index = torch.tensor([[0, 1, 3, 3],
                               [1, 2, 1, 0]], dtype=torch.long, device=device)  # move to device
    edge_index = to_undirected(edge_index)

    # Erstellen eines PyG Datenobjekts
    data = Data(edge_index=edge_index)

    # Feature-Matrix
    x = torch.tensor([[1, 2], [3, 4], [5, 6], [2, 3]], dtype=torch.float, device=device)  # move to device

    # Datenobjekt Update
    data.x = x

    # SAGEConv Schicht
    conv = SAGEConv(2, 2, aggr="add").to(device)  # move model to device

    # Optimizer
    optimizer = torch.optim.Adam(conv.parameters(), lr=0.01)
    loss_fn = torch.nn.MSELoss()

    # Trainingszyklus
    for epoch in range(100):
        optimizer.zero_grad()
        out = conv(data.x, data.edge_index)
        target = torch.tensor([[0.5, 1.0], [1.5, 2.0], [2.5, 3.0], [3, 2]], dtype=torch.float, device=device)  # move to device
        loss = loss_fn(out, target)
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0 or epoch == 99:  # print every 10 epochs and last epoch
            print(f'Epoch {epoch+1}: Loss = {loss.item()}')
            if epoch == 99:
                print(out)
                print(out[2][1].item())