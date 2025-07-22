import networkx as nx
import matplotlib.pyplot as plt
import math
from typing import Dict, List, Any

def get_graph(lines, arcs):
    
    G_without_arcs = nx.Graph()
    centermap: Dict[str, List[Any]] = {}
    # 添加线条到图中
    for line in lines:
        start_point = (round(line.StartPoint[0], 1), round(line.StartPoint[1], 1))  # 保留一位小数
        end_point = (round(line.EndPoint[0], 1), round(line.EndPoint[1], 1))
       
        G_without_arcs.add_edge(start_point, end_point)
    # 添加圆弧到图中
    for arc in arcs:
        center = arc.Center
        normal = arc.Normal  # 假设 arc 有 Normal 属性表示法线方向

        # 判断法线方向并构造 center_key
        if round(normal[0], 1) == 0 and round(normal[1], 1) == 0 and round(normal[2], 1) == 1:
            # 法线方向为 Z，使用 X 和 Y 构造 key
            center_key = f"({round(center[0], 1)}, {round(center[1], 1)})Z"

        elif round(normal[0], 1) == 0 and round(normal[1], 1) == 1 and round(normal[2], 1) == 0:
            # 法线方向为 Y，使用 X 和 Z 构造 key
            center_key = f"({round(center[0], 1)}, {round(center[2], 1)})Y"

        elif round(normal[0], 1) == 1 and round(normal[1], 1) == 0 and round(normal[2], 1) == 0:
            # 法线方向为 X，使用 Y 和 Z 构造 key
            center_key = f"({round(center[1], 1)}, {round(center[2], 1)})X"


        # 将 arc 添加到 centermap 中对应的集合中
        if center_key not in centermap:
            centermap[center_key] = []
        centermap[center_key].append(arc)
        # 这里可以添加更多逻辑来处理圆弧的离散化，并将中间点加入图中
      
   
    return G_without_arcs,centermap