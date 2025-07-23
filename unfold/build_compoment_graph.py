from typing import Dict, List, Any
import networkx as nx
import matplotlib.pyplot as plt
def get_compoment_graph(component_arc_map: Dict[str,list]):
    graph = nx.Graph()  # 创建一个空图

    for edge, nodes in component_arc_map.items():
        
        
        graph.add_edge( nodes[0], nodes[1], name=edge)  # 将边的 name 属性设置为 value

    pos = nx.spring_layout(graph)  # 定义节点布局
    plt.clf()
    nx.draw(graph, pos, with_labels=True, node_size=50, node_color='lightblue', font_size=20, font_weight='bold')

    plt.show()
    return graph