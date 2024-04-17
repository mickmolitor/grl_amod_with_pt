import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Verwenden Sie Agg als Backend, kein GUI-Fenster wird benötigt
import matplotlib.pyplot as plt


def visualize_zone_graph():
    # Daten laden
    zones_df = pd.read_csv('data/zones.csv')
    zone_graph_df = pd.read_csv('data/zone_graph.csv')

    # Erstellen des Graphen
    G = nx.Graph()
    # Fügen Sie Knoten hinzu
    for index, row in zones_df.iterrows():
        if int(row["zone_id"]) == 9999:
            continue
        G.add_node(int(row['zone_id']), pos=(row['zone_center_lon'], row['zone_center_lat']))

    # Fügen Sie Kanten hinzu
    for index, row in zone_graph_df.iterrows():
        G.add_edge(row['zone1_id'], row['zone2_id'])

    # Positionen der Knoten für die Visualisierung
    pos = nx.get_node_attributes(G, 'pos')

    # Zeichnen des Graphen
    plt.figure(figsize=(20, 16), dpi=300)  # Größe des Bildes festlegen
    nx.draw(G, pos, node_size=50, node_color='blue', with_labels=True, font_size=12)
    plt.title('Visualisierung des Zonengraphen')
    plt.savefig("figures/zone_graph.png")
