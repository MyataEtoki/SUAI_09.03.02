import matplotlib.pyplot as plt
from tests.metro_parser import load_metro_map
import networkx as nx

def draw_metro_map(metro_data, filename="metro_map.png"):
    G = nx.Graph()
    color_map = {}
    colors = [
        'yellow', 'blue', 'red', 'green', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan'
    ]

    for idx, line in enumerate(metro_data['lines']):
        color_map[line['name']] = colors[idx % len(colors)]

    for line in metro_data['lines']:
        stations = [station if isinstance(station, str) else station.get(
            'name', '') for station in line['stations']]
        for i in range(len(stations) - 1):
            G.add_edge(stations[i], stations[i+1],
                       color=color_map[line['name']])

    edge_colors = [G[u][v]['color'] for u, v in G.edges()]

    pos = nx.kamada_kawai_layout(G)
    plt.figure(figsize=(19, 9))
    nx.draw(
        G, pos, with_labels=True, node_size=200, node_color='lightblue',
        font_size=5, font_weight='bold', edge_color=edge_colors, width=2
    )
    plt.title("Metro Map (by Line Color)")
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == "__main__":
    graph = load_metro_map("metro.json")
    draw_metro_map(graph, "metro-map.png")