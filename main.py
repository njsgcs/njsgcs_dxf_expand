delete=False

from threeDrebuild import ThreeDRebuilder


builder = ThreeDRebuilder(delete)
l_a_c,height_diff= builder.run()
lines, arcs, circles = l_a_c

import unfold.build_graph
import importlib
importlib.reload(unfold.build_graph)
from unfold.build_graph import get_graph
G_without_arcs,center_SEpair_map,center_arc_map=get_graph(lines,arcs)

import unfold.build_compoment
import importlib
importlib.reload(unfold.build_compoment)
from unfold.build_compoment import get_component

component_arc_map,component_id_map,start_id=get_component(G_without_arcs,center_SEpair_map)

import unfold.build_compoment_graph
import importlib
importlib.reload(unfold.build_compoment_graph)
from unfold.build_compoment_graph import get_compoment_graph
graph=get_compoment_graph(component_arc_map)


import numpy as np
from  unfold.unfold_arc import UnfoldProcessor

print("其中 1 是红色，2 是黄色，3 是绿色，4 是蓝色，5 是紫色，6 是青色，7 是灰色，8 是白色")
visited = set()
last_transform = np.eye(4)  # 初始变换矩阵

processor = UnfoldProcessor( lines,arcs, circles,center_arc_map, component_id_map,delete)
processor.dfs(graph, start_id, visited, last_transform)
processor.drawlines(height_diff)
input("按回车键退出")