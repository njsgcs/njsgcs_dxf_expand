from pyautocad import Autocad, APoint
import math

def get_lines():
    acad = Autocad()
    doc = acad.doc
    model_space = doc.ModelSpace
    
    inputlines = []
    lineId = 0
    lineMap = {}  # 用于映射 lineId 到实体对象（可选功能）

    def round_coords(*coords):
        return [round(coord, 1) for coord in coords]

    for obj in model_space:
        try:
            if obj.ObjectName == "AcDbLine":
                # LINE
                sp = obj.StartPoint
                ep = obj.EndPoint
                x1, y1, x2, y2 = round_coords(sp[0], sp[1], ep[0], ep[1])
                line = [x1, y1, x2, y2, lineId, 0]
                inputlines.append(line)
                lineMap[lineId] = obj
                lineId += 1

            elif obj.ObjectName == "AcDbArc":
                # ARC
                center = obj.Center
                radius = obj.Radius
                start_angle = obj.StartAngle
                end_angle = obj.EndAngle

                # 起点和终点坐标
                sx = center[0] + radius * math.cos(start_angle)
                sy = center[1] + radius * math.sin(start_angle)
                ex = center[0] + radius * math.cos(end_angle)
                ey = center[1] + radius * math.sin(end_angle)

                x1, y1, x2, y2 = round_coords(sx, sy, ex, ey)
                line = [x1, y1, x2, y2, lineId, 1]
                inputlines.append(line)
                lineMap[lineId] = obj
                lineId += 1

            elif obj.ObjectName == "AcDbCircle":
                # CIRCLE
                center = obj.Center
                radius = obj.Radius
                # 圆的外接矩形对角坐标
                sx = center[0] - radius
                sy = center[1] - radius
                ex = center[0] + radius
                ey = center[1] + radius

                x1, y1, x2, y2 = round_coords(sx, sy, ex, ey)
                line = [x1, y1, x2, y2, lineId, 2]
                inputlines.append(line)
                lineMap[lineId] = obj
                lineId += 1

            elif obj.ObjectName == "AcDbSpline":
                # SPLINE（取首尾控制点）
                control_points = obj.ControlPoints
                if control_points and len(control_points) >= 4:
                    # 假设控制点是按 x1, y1, x2, y2, ... 排列的一维元组
                    # 每两个值为一个点
                    points = [(control_points[i], control_points[i+1]) for i in range(0, len(control_points), 3)]
                    if len(points) >= 2:
                        start = points[0]
                        end = points[-1]
                        x1, y1 = round_coords(start[0], start[1])
                        x2, y2 = round_coords(end[0], end[1])
                        line = [x1, y1, x2, y2, lineId, 0]#type设为3会在key=lambda x: -int(x['type']) if isinstance(x['type'], (int, float)) 
                                                 #   else float('-inf'))把弧线顶替掉
                        inputlines.append(line)
                        lineMap[lineId] = obj
                        lineId += 1
            else:
                print(f"其他对象: {obj.ObjectName}")
        except Exception as e:
            print(f"处理对象失败: {obj.ObjectName}, 错误: {e}")

    return inputlines, lineMap,acad