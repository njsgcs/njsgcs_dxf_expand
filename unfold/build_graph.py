import networkx as nx
import matplotlib.pyplot as plt
import math
from typing import Dict, List, Any
from interferce import *
def get_graph(lines, arcs: List[Arc3D]):

    G_without_arcs = nx.Graph()
    center_SEpair_map: Dict[str,  List[Any]] = {}
    center_arc_map: Dict[str,  Any] = {}
    # 添加线条到图中
    for line in lines:
        
        start_point = (round(line.StartPoint[0], 1), round(line.StartPoint[1], 1), round(line.StartPoint[2], 1))  # 保留一位小数
        end_point = (round(line.EndPoint[0], 1), round(line.EndPoint[1], 1), round(line.EndPoint[2], 1))
        if(start_point!=end_point):
          
         G_without_arcs.add_edge(start_point, end_point)
         
    # 添加圆弧到图中
    for arc in arcs:
        center = arc.center
        normal = arc.normal  # 假设 arc 有 Normal 属性表示法线方向

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
        if center_key not in center_SEpair_map:
            center_SEpair_map[center_key] = []
            center_arc_map[center_key] = arc
        center_SEpair_map[center_key].append([arc.start_point, arc.end_point])
        # 这里可以添加更多逻辑来处理圆弧的离散化，并将中间点加入图中
      
    for center_key in center_SEpair_map:
        sepairs = center_SEpair_map[center_key]

        seen = set()
        unique_sepairs = []

        for sepair in sepairs:
            start, end = sepair
            # 将 APoint 转换为元组，并保留一位小数
            start_tuple = tuple(round(x, 1) for x in (start.x, start.y, start.z))
            end_tuple = tuple(round(x, 1) for x in (end.x, end.y, end.z))
            key = frozenset((start_tuple, end_tuple))

            if key not in seen:
                seen.add(key)
                unique_sepairs.append(sepair)

        center_SEpair_map[center_key] = unique_sepairs
    return G_without_arcs,center_SEpair_map,center_arc_map