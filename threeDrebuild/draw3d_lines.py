from pyautocad import Autocad, APoint
import math
from interferce import Arc3D, Line3D, Circle3D
# 绘制3D模型
def draw_3d_model(acad : Autocad,line3d, line_map,  cluster_min_x_r, cluster_min_y_t,delete):
    lines=[]
    arcs=[]
    circles=[]
    for line in line3d:
        # 解构线条数据
        x1, y1, z1, x2, y2, z2, line_id, line_type, color, view_id = line
      
        if line_type == 0:
            # 绘制直线
            start_point = APoint(x1, y1, z1)
            end_point = APoint(x2, y2, z2)
            Line=acad.model.AddLine(start_point, end_point)
            lines.append(Line3D(Line))
            if delete:
               
                    Line.Delete()
        elif line_type == 1:
            # 绘制圆弧
            entity = line_map.get(line_id)
            
            if entity and hasattr(entity, 'StartAngle') and hasattr(entity, 'EndAngle'):
                arc_entity = entity
              
                
                angle_delta = (arc_entity.EndAngle - arc_entity.StartAngle) * 180 / math.pi
                
                center = arc_entity.center
                radius = arc_entity.radius
                #print("Center:" + str(center))
                
              #  print("EndAngle:" + str(arc_entity.EndAngle* 180 / math.pi) + " StartAngle:" + str(arc_entity.StartAngle* 180 / math.pi) + " angle_delta:" + str(angle_delta))
                center = tuple(round(coord, 1) for coord in center)
                radius = round(radius, 1)
                
                if view_id == 2:
                    center_x = center[0] - cluster_min_x_r
                    center_y = center[1]
                    start_x = round(center_x + radius * math.cos(arc_entity.StartAngle), 1)
                    start_y = round(center_y + radius * math.sin(arc_entity.StartAngle), 1)
                    end_x = round(center_x + radius * math.cos(arc_entity.EndAngle), 1)
                    end_y = round(center_y + radius * math.sin(arc_entity.EndAngle), 1)

                    normal = APoint(1.0, 0.0, 0.0)
                    if ((start_x == z1 and start_y == y1 and end_x == z2 and end_y == y2)
                        or (start_x == z2 and start_y == y2 and end_x == z1 and end_y == y1)):
                        center_point = APoint(x1,center_y,center_x)
                        end_anggle = -arc_entity.StartAngle+math.pi/2
                        start_anggle = -arc_entity.EndAngle+math.pi/2
                        arc = acad.model.AddArc(center_point, radius,  start_anggle, end_anggle)
                        arc.Normal = normal
                        
                        Aarc= Arc3D(arc,APoint(x1, start_y, start_x),APoint(x1, end_y, end_x),view_id, start_anggle, end_anggle)
                        arcs.append(Aarc)
                        if delete:
                            arc.Delete()
                elif view_id == 0:
                    center_x = center[0]
                    center_y = center[1]
                    start_x = round(center_x + radius * math.cos(arc_entity.StartAngle), 1)
                    start_y = round(center_y + radius * math.sin(arc_entity.StartAngle), 1)
                    end_x = round(center_x + radius * math.cos(arc_entity.EndAngle), 1)
                    end_y = round(center_y + radius * math.sin(arc_entity.EndAngle), 1)
                    normal = APoint(0.0, 0.0, 1.0)
                    if ((start_x == x1 and start_y == y1 and end_x == x2 and end_y == y2)
                        or (start_x == x2 and start_y == y2 and end_x == x1 and end_y == y1)):
                        center_point = APoint(center_x, center_y,z1)
                        arc = acad.model.AddArc(center_point, radius, arc_entity.StartAngle, arc_entity.EndAngle)
                        arc.Normal = normal
                        Aarc= Arc3D(arc,APoint(start_x, start_y, z1),APoint(end_x, end_y, z1),view_id, arc_entity.StartAngle, arc_entity.EndAngle)
                        arcs.append(Aarc)
                        if delete:
                            arc.Delete()
                elif view_id == 1:
                    normal = APoint(0.0, 1.0, 0.0)
                    center_x = center[0]
                    center_y = center[1] - cluster_min_y_t
                    start_x = round(center_x + radius * math.cos(arc_entity.StartAngle), 1)
                    start_y = round(center_y + radius * math.sin(arc_entity.StartAngle), 1)
                    end_x = round(center_x + radius * math.cos(arc_entity.EndAngle), 1)
                    end_y = round(center_y + radius * math.sin(arc_entity.EndAngle), 1)
                    if ((start_x == x1 and start_y == z1 and end_x == x2 and end_y == z2)
                        or (start_x == x2 and start_y == z2 and end_x == x1 and end_y == z1)):
                        center_point = APoint(center_x, y1,center_y)
                        start_anggle = arc_entity.StartAngle+math.pi/2
                        end_anggle = arc_entity.EndAngle+math.pi/2
                        arc = acad.model.AddArc(center_point, radius, start_anggle, end_anggle)
                       
                        arc.Normal = normal
                        Aarc= Arc3D(arc,APoint(start_x, y1,start_y),APoint(end_x, y1,end_y),view_id, start_anggle, end_anggle)
                        arcs.append(Aarc)
                        if delete:
                            arc.Delete()
        elif line_type == 2:
            # 绘制圆+
            entity = line_map.get(line_id)
            if entity and hasattr(entity, 'center') and hasattr(entity, 'radius'):
                circle_entity = entity
                center = circle_entity.center
                radius = circle_entity.radius
                
                if view_id == 0:
                    normal = APoint(0.0, 0.0, 1.0)
                    center_point = APoint(center[0], center[1],z1)
                    circle=acad.model.AddCircle(center_point, radius)
                    circle.normal = normal
                    circles.append(Circle3D(circle))
                    if delete:
                           circle.Delete()
                elif view_id == 1:
                    normal = APoint(0.0, 1.0, 0.0)
                    center_x = center[0]
                    center_y = center[1] - cluster_min_y_t
                    center_point = APoint(center_x,y1,center_y)
                    circle=acad.model.AddCircle(center_point, radius)
                    circle.normal = normal
                    circles.append(Circle3D(circle))
                    if delete:
                           circle.Delete()
                elif view_id == 2:
                    normal = APoint(1.0, 0.0, 0.0)
                    center_x = center[0] - cluster_min_x_r
                    center_y = center[1]
                    center_point = APoint(x1,center_y,center_x)
                    circle=acad.model.AddCircle(center_point, radius)
                    circle.normal = normal
                    circles.append(Circle3D(circle))
                    if delete:
                           circle.Delete()
    return lines,arcs,circles