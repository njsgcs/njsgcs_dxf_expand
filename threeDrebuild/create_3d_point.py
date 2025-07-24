from typing import List, Tuple, Dict, Set, Optional
from collections import defaultdict


def find_most_frequent_min_xy(clusters):
    min_x_values = [c.min_x for c in clusters]
    min_y_values = [c.min_y for c in clusters]

    most_min_x = max(set(min_x_values), key=min_x_values.count)
    most_min_y = max(set(min_y_values), key=min_y_values.count)

    return {
        "mostMinX": {"value": most_min_x},
        "mostMinY": {"value": most_min_y}
    }


def generate_3d_points(clusters):
    """
    根据输入的聚类数据生成主视图、顶视图、右视图中的线段和点，并生成对应的3D点集合。

    参数:
        clusters (List[Cluster]): 包含多个聚类对象的列表，每个聚类对象应包含以下属性：
            - min_x (float): 聚类在X轴上的最小值
            - min_y (float): 聚类在Y轴上的最小值
            - lines (List[Tuple]): 线段列表，每条线段格式为 (x1, y1, x2, y2, line_id, line_type)

    返回:
        Dict[str, Union[List, Set]]: 包含以下键值对的字典：
            - "front_lines": 主视图中的线段列表，格式为 [x1, y1, x2, y2, line_id, type]
            - "top_lines": 顶视图中的线段列表，格式同上
            - "right_lines": 右视图中的线段列表，格式同上
            - "front_points": 主视图中的点列表，每个点为 (x, y) 元组
            - "top_points": 顶视图中的点列表，每个点为 (x, y) 元组
            - "right_points": 右视图中的点列表，每个点为 (x, y) 元组
            - "points_3d": 生成的3D点列表，每个点为 [x, y, z] 坐标

    说明:
        - 主视图（Front）以 most_min_x 和 most_min_y 对应的聚类为主
        - 顶视图（Top）基于主视图 X 坐标对齐，Y 坐标归零
        - 右视图（Right）基于主视图 Y 坐标对齐，X 坐标归零
        - 3D点通过主视图与顶视图的 X 相同交点生成，Z 来自顶视图 Y
    """
    stats = find_most_frequent_min_xy(clusters)
    most_min_x = stats["mostMinX"]["value"]
    most_min_y = stats["mostMinY"]["value"]

    # 筛选聚类
    most_frequent_clusters = [c for c in clusters if c.min_x == most_min_x and c.min_y == most_min_y]
    top_clusters = [c for c in clusters if c.min_x == most_min_x and c.min_y > most_min_y]
    right_clusters = [c for c in clusters if c.min_x > most_min_x and c.min_y == most_min_y]
    bottom_clusters = [c for c in clusters if c.min_x == most_min_x and c.min_y < most_min_y]
    left_clusters = [c for c in clusters if c.min_x < most_min_x and c.min_y == most_min_y]

    # 取第一个匹配的聚类
    most_frequent_cluster = most_frequent_clusters[0] if most_frequent_clusters else None
    top_cluster = top_clusters[0] if top_clusters else None
    right_cluster = right_clusters[0] if right_clusters else None
    bottom_cluster = bottom_clusters[0] if bottom_clusters else None
    left_cluster = left_clusters[0] if left_clusters else None

    # 点和线收集
    front_line_list = []
    top_line_list = []
    right_line_list = []

    front_point_set = set()
    top_point_set = set()
    right_point_set = set()

    front_point_list = []
    top_point_list = []
    right_point_list = []

    if most_frequent_cluster:
        cluster_min_y = top_cluster.min_y if top_cluster else 0

        for line in most_frequent_cluster.lines:
            x1, y1, x2, y2, line_id, line_type = line
            x1f = round(x1, 1)
            y1f = round(y1, 1)
            x2f = round(x2, 1)
            y2f = round(y2, 1)

            front_line_list.append([x1f, y1f, x2f, y2f, line_id, line_type])
            add_unique_point(x1f, y1f, front_point_set, front_point_list)
            add_unique_point(x2f, y2f, front_point_set, front_point_list)
     
    if top_cluster:
        cluster_min_y = top_cluster.min_y

        for line in top_cluster.lines:
            x1, y1, x2, y2, line_id, line_type = line
            x1f = round(x1, 1)
            y1f = round(y1 - cluster_min_y, 1)
            x2f = round(x2, 1)
            y2f = round(y2 - cluster_min_y, 1)

            top_line_list.append([x1f, y1f, x2f, y2f, line_id, line_type])
            add_unique_point(x1f, y1f, top_point_set, top_point_list)
            add_unique_point(x2f, y2f, top_point_set, top_point_list)
    left_model=False
    if right_cluster:
        cluster_min_x = right_cluster.min_x

        for line in right_cluster.lines:
            x1, y1, x2, y2, line_id, line_type = line
            x1f = round(x1 - cluster_min_x, 1)
            y1f = round(y1, 1)
            x2f = round(x2 - cluster_min_x, 1)
            y2f = round(y2, 1)

            right_line_list.append([x1f, y1f, x2f, y2f, line_id, line_type])
            add_unique_point(x1f, y1f, right_point_set, right_point_list)
            add_unique_point(x2f, y2f, right_point_set, right_point_list)
    else :
     if left_cluster:
        left_model=True
        cluster_min_x = -left_cluster.max_x

        for line in left_cluster.lines:
            x1, y1, x2, y2, line_id, line_type = line
            x1f = round(-x1 - cluster_min_x, 1)
            y1f = round(y1, 1)
            x2f = round(-x2 - cluster_min_x, 1)
            y2f = round(y2, 1)
            right_line_list.append([x1f, y1f, x2f, y2f, line_id, line_type])
            add_unique_point(x1f, y1f, right_point_set, right_point_list)
            add_unique_point(x2f, y2f, right_point_set, right_point_list)
         
    # 收集 3D 点
    point_3d_list = []
    seen_3d = set()

    for fx, fy in front_point_list:
        for tx, ty in top_point_list:
            if abs(fx - tx) < 1e-6:  # 浮点精度容差
                key = f"{fx},{fy},{ty}"
                if key not in seen_3d:
                    seen_3d.add(key)
                    point_3d_list.append([fx, fy, ty])


    print(f"主视图有 {len(front_line_list)} 条线段，{len(front_point_list)} 个点")
    print(f"顶视图有 {len(top_line_list)} 条线段，{len(top_point_list)} 个点")
    print(f"右视图有 {len(right_line_list)} 条线段，{len(right_point_list)} 个点")
    print(f"3D点生成完毕，共 {len(point_3d_list)} 个点")

    return {
        "front_lines": front_line_list,
        "top_lines": top_line_list,
        "right_lines": right_line_list,
        "front_points": front_point_list,
        "top_points": top_point_list,
        "right_points": right_point_list,
        "points_3d": point_3d_list,
         "right_cluster_min_x":right_cluster.min_x if right_cluster is not None else left_cluster.max_x if left_cluster is not None else None,
        "top_cluster_min_y":top_cluster.min_y if top_cluster is not None else None,
         "top_cluster_max_y":top_cluster.max_y if top_cluster is not None else None,
         "front_cluster_min_y":most_frequent_cluster.min_y if most_frequent_cluster is not None else None
         ,"left_model":left_model
    }


def add_unique_point(x: float, y: float, seen: Set[str], point_list: List[Tuple[float, float]]):
    key = f"{x},{y}"
    if key not in seen:
        seen.add(key)
        point_list.append((x, y))