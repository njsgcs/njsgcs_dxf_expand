from typing import Dict, List, Any
import networkx as nx
import matplotlib.pyplot as plt
def get_compoment_graph(component_arc_map: Dict[str,list],component_id_map):
    graph = nx.Graph()  # 创建一个空图
    newcomponent_id_map = {}
    new_node=0
    new_old_node_map = {}
    for edge, nodes in component_arc_map.items():
       
       
        
        
        key=','.join(map(str,list(nodes[0]))) 
        if key not in new_old_node_map:
                
                new_old_node_map[key] = new_node
                node_pair_0=new_node
                newcomponent_id_map[new_node] = []
                for node in list(nodes[0]):

                 newcomponent_id_map[new_node].append(component_id_map[node])
                new_node+=1
        else :
                node_pair_0=new_old_node_map[key]     
               
        
        
        key=','.join(map(str,list(nodes[1]))) 
        if key not in new_old_node_map:
                
                new_old_node_map[key] = new_node
                node_pair_1=new_node
                newcomponent_id_map[new_node] = []
                for node in list(nodes[1]):

                 newcomponent_id_map[new_node].append(component_id_map[node])
                new_node+=1
        else :
                node_pair_1=new_old_node_map[key]     
            
        graph.add_edge(  node_pair_0, node_pair_1, name=edge)  # 将边的 name 属性设置为 value
    start_id=-1
    for node in newcomponent_id_map:
     
     component_edges=[ edge for component in newcomponent_id_map[node] for edge in component["component_edges"]]
     component_points= [ point for component in newcomponent_id_map[node] for point in component["component_points"]]        
     newcomponent_id_map[node]= {"component_edges":component_edges,"component_points":component_points}
     if  start_id==-1 :
            x_coords = [point[0] for point in component_points]
            y_coords = [point[1] for point in component_points]
            z_coords = [point[2] for point in component_points]
            
            # 计算各维度的范围
            width = max(x_coords) - min(x_coords)
            height = max(y_coords) - min(y_coords)
            depth = max(z_coords) - min(z_coords)
            if depth<width and depth<height:
                start_id=node
    
    pos = nx.spring_layout(graph)  # 定义节点布局
    plt.clf()
    nx.draw(graph, pos, with_labels=True, node_size=50, node_color='lightblue', font_size=20, font_weight='bold')

    plt.show()
    return graph,newcomponent_id_map,start_id