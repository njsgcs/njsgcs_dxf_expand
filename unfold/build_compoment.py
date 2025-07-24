import networkx as nx
import matplotlib.pyplot as plt
from typing import TypedDict,Dict, List, Any
class ComponentInfo(TypedDict):
    component_edges: List[Any]   # 可以根据你的实际类型更具体，如 List[Tuple[Any, Any]]
    component_points: List[Any] 
def get_component(G_without_arcs: nx.Graph, center_SEpair_map: Dict[str, List[Any]]):
    components = list(nx.connected_components(G_without_arcs))
    component_arc_map: Dict[str, list] = {}

    component_id_map: Dict[int,ComponentInfo] = {}
   
    
    for i, component in enumerate(components):
        component_points = [ node for node in component]  # 转为 set 提升查找效率
        component_edges = [ edge for edge in G_without_arcs.edges() if edge[0] in component_points and edge[1] in component_points]
        s_sepairs_count = 0
        e_sepairs_count = 0
        component_id_map[i] ={"component_edges":component_edges,"component_points":component_points}
        for key, sepairs in center_SEpair_map.items():
           
            
            for sepair in sepairs:
                start, end = sepair[0], sepair[1]
                for component_point in component_points:
                    if abs(start[0] - component_point[0]) <= 0.2 and abs(start[1] - component_point[1]) <= 0.2 and abs(start[2] - component_point[2]) <= 0.2:
                        # start 在 component_point 的误差范围内
                       if key not in component_arc_map:
                               component_arc_map[key] = [set(),set()]
                       component_arc_map[key][0].add(i)
                       s_sepairs_count += 1
                       
                    elif abs(end[0] - component_point[0]) <= 0.2 and abs(end[1] - component_point[1]) <= 0.2 and abs(end[2] - component_point[2]) <= 0.2:
                        # end 在 component_point 的误差范围内
                       if key not in component_arc_map:
                               component_arc_map[key] = [set(),set()]
                       component_arc_map[key][1].add(i)
                       e_sepairs_count += 1
                       
            
                            
                  
                    
           # print(f"这个component命中了sepair里的{sepairs_count}条线")
            # if(sepairs_count==0):
            #     print(f"sepairs{sepairs} ")
        print(f"第 {i+1} 个连通分量有 {len(component)} 个节点，包含的起点弧有 {s_sepairs_count} 条，包含的终点弧有 {e_sepairs_count} 条")
       

                
   
    plt.clf()
    nx.draw(G_without_arcs, with_labels=True, node_size=10, font_size=8)
    plt.show()

    return component_arc_map,component_id_map