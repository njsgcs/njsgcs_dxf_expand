def is_point_on_line_segment(px, py, x1, y1, x2, y2, epsilon=0.2):
    cross_product = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
    is_point_on_line=True
    if abs(cross_product) > epsilon:
         is_point_on_line=False

    dot_product = (px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)
    if dot_product < 0:
        is_point_on_line= False

    squared_length = (x2 - x1) ** 2 + (y2 - y1) ** 2
    if is_point_on_line:is_point_on_line=dot_product <= squared_length+0.2
    return is_point_on_line,cross_product,dot_product,squared_length

def make_map(lines, points):
    """
    创建一个映射，将线段上的点连接到对应的线段ID和类型。
    
    参数:
        lines (List[List]): 线段列表，每个线段由 [x1, y1, x2, y2, line_id, type_] 定义
            - (x1, y1): 线段起点坐标
            - (x2, y2): 线段终点坐标
            - line_id: 线段的唯一标识符
            - type_: 线段类型
        points (List[Tuple[float, float]]): 点列表，每个点为 (px, py) 坐标
        
    返回:
        Dict[str, Dict]: 一个字典，键是格式为 "x1,y1,x2,y2" 的字符串，值包含 line_id 和 type
            - key: 格式为 "x1,y1,x2,y2" 的字符串，表示线段的两个端点坐标
            - value: 包含以下键值对的字典：
                - 'lineid': 线段的唯一标识符
                - 'type': 线段类型
        
    说明:
        - 遍历所有线段和所有点，找到在线段上的点
        - 对于每个线段上的点，创建一个从该点到线段终点的映射
        - 然后连接所有相关的点对，创建线段
        - 最终返回的映射用于确定给定点是否在特定线段上
    """
    map_obj = {}  # 初始化一个空字典来存储映射关系
    
    # 遍历所有线段
    for x1, y1, x2, y2, line_id, type_ in lines:
        relevant_points = []  # 存储在线段上的点
 
        # 检查每个点是否在线段上
        for px, py in points:
            is_point_on_line,cross_product,dot_product,squared_length=is_point_on_line_segment(px, py, x1, y1, x2, y2)
            if px==133.7 and py==117.9:
                if(x1==103.7 and y1==117.9 and x2==133.7 and y2==117.9):
            
                 pass
            if is_point_on_line:
                # 如果点在线段上，将其添加到相关点列表中
                pxf = round(px, 1)  # 将点坐标四舍五入到一位小数
                pyf = round(py, 1)
                relevant_points.append((pxf, pyf))  # 添加点到相关点列表
                
                # 创建一个从该点到其本身的映射（表示一个点）
                key = f"{pxf},{pyf},{pxf},{pyf}"
                if type_ == 0:  # 只有当线段类型为0时才添加
                    map_obj[key] = {'lineid': line_id, 'type': type_}
     
        # 连接相关点对
        for i in range(len(relevant_points)):
            for j in range(i + 1, len(relevant_points)):
                # 获取两个相关点
                p1x, p1y = relevant_points[i]
                p2x, p2y = relevant_points[j]
                
       
                
                # 创建两个方向的映射（点1到点2和点2到点1）
                key1 = f"{p1x},{p1y},{p2x},{p2y}"
                key2 = f"{p2x},{p2y},{p1x},{p1y}"
                
                # 添加映射到字典中
                map_obj[key1] = {'lineid': line_id, 'type': type_}
                map_obj[key2] = {'lineid': line_id, 'type': type_}
    
    return map_obj  # 返回创建的映射字典

seen_line_pairs = set()

lines3d = []

def draw_lines(x1, y1, z1, x2, y2, z2, line_id, type_, color, view_id):
    if [x1, y1, z1] == [x2, y2, z2]:
        return
    # if type_==1:
    #     pass
    key = ",".join(f"{v:.1f}" for v in [x1, y1, z1, x2, y2, z2])
    if key not in seen_line_pairs:
        #print(f"线段: 起点 ({x1:.1f}, {y1:.1f}, {z1:.1f}), 终点 ({x2:.1f}, {y2:.1f}, {z2:.1f}),type: {type_}, line_id: {line_id}")
        seen_line_pairs.add(key)
        lines3d.append([x1, y1, z1, x2, y2, z2, line_id, type_, color, view_id])
    

def format_key(x1, y1, x2, y2):
    return f"{x1:.1f},{y1:.1f},{x2:.1f},{y2:.1f}"

def generate_3d_lines(point3dlist,frontlinelist, toplinelist, rightlinelist,frontpointlist, toppointlist, rightpointlist):
  
    """
    根据3D点和各视图的线段/点数据，生成并返回3D线段列表。

    参数:
        point3dlist (List[List[float]]): 3D点列表，每个点格式为 [x, y, z]
        frontlinelist (List[List[float]]): 主视图线段列表，每条线段格式为 [x1, y1, x2, y2, line_id, type]
        toplinelist (List[List[float]]): 顶视图线段列表，格式同上
        rightlinelist (List[List[float]]): 右视图线段列表，格式同上
        frontpointlist (List[Tuple[float, float]]): 主视图点列表，每个点为 (x, y)
        toppointlist (List[Tuple[float, float]]): 顶视图点列表，每个点为 (x, y)
        rightpointlist (List[Tuple[float, float]]): 右视图点列表，每个点为 (x, y)

    返回:
        List[List]: 生成的3D线段列表，每条线段格式为 [x1, y1, z1, x2, y2, z2, line_id, type, color, view_id]
            - x1, y1, z1: 起始点坐标
            - x2, y2, z2: 结束点坐标
            - line_id: 对应的原始线段ID
            - type: 线段类型
            - color: 线段颜色（固定为1）
            - view_id: 视图ID（0=主视图，1=顶视图，2=右视图）

    说明:
        - 通过主视图、顶视图、右视图中的点对齐关系，生成对应的3D线段
        - 使用 draw_lines 添加线段到全局列表 lines3d 中
        - 返回的线段包含视图信息和线段类型，便于后续渲染或导出
    """
    rightpointmap=make_map(rightlinelist, rightpointlist)
    frontpointmap=make_map(frontlinelist, frontpointlist)
    toppointmap=make_map(toplinelist, toppointlist)
  
    for x1, y1, z1 in point3dlist:
        for x2, y2, z2 in point3dlist:
            if x1 == x2 and y1 == y2 and z1 == z2:
                continue

            x1f, y1f, z1f = round(x1, 1), round(y1, 1), round(z1, 1)
            x2f, y2f, z2f = round(x2, 1), round(y2, 1), round(z2, 1)

            front_key = format_key(x1f, y1f, x2f, y2f)
            top_key = format_key(x1f, z1f, x2f, z2f)
            right_key = format_key(z1f, y1f, z2f, y2f)

            exist_in_front = frontpointmap.get(front_key)
            exist_in_top = toppointmap.get(top_key)
            exist_in_right = rightpointmap.get(right_key)
            
            if (x1f==128.9 and y1f==119.0 and z1f==28.0\
                and x2f==128.9  and y2f==119.0 and z2f==31.0)\
            or (x2f==128.9  and y2f==119.0 and z2f==31.0 \
                and x1f==128.9  and y1f==119.0 and z1f==28.0):
                pass
            if exist_in_front and exist_in_top and exist_in_right:
                frontline_id = exist_in_front['lineid']
                fronttype = exist_in_front['type']

                topline_id = exist_in_top['lineid']
                toptype = exist_in_top['type']

                rightline_id = exist_in_right['lineid']
                righttype = exist_in_right['type']
                # if exist_in_right and exist_in_right['type']==1:
                #  print(exist_in_right)
                # 创建需要绘制的命令列表，每个命令包含线段类型和绘制函数
                draw_commands = sorted([
                    # 主视图绘制命令
                    {'type': fronttype, 
                    'draw': lambda: draw_lines(x1f, y1f, z1f, x2f, y2f, z2f, 
                                                frontline_id, fronttype, 1, 0)},
                    
                    # 顶视图绘制命令
                    {'type': toptype, 
                    'draw': lambda: draw_lines(x1f, y1f, z1f, x2f, y2f, z2f, 
                                                topline_id, toptype, 1, 1)},
                    
                    # 右视图绘制命令
                    {'type': righttype, 
                    'draw': lambda: draw_lines(x1f, y1f, z1f, x2f, y2f, z2f, 
                                                rightline_id, righttype, 1, 2)}
                    
                    # 排序规则：按照线段类型降序排列
                    # 类型为数字的直接转换为整数排序
                    # 类型为非数字的排在最后
                ], key=lambda x: -int(x['type']) if isinstance(x['type'], (int, float)) 
                                                    else float('-inf'))
                for cmd in draw_commands:
                    cmd['draw']()

    return lines3d