import networkx as nx
import matplotlib.pyplot as plt
from IPython.display import display

def get_component(G_without_arcs: nx.Graph):
    components = list(nx.connected_components(G_without_arcs))
    display(f"图中共有 {len(components)} 个连通分量")

    plt.clf()
    nx.draw(G_without_arcs, with_labels=True, node_size=10, font_size=8)
    plt.show()