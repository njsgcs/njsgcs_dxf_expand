from pyautocad import  APoint
from typing import List,Any
class Arc3D:
    def __init__(self, arc,start_point: APoint|Any, end_point: APoint|Any, view_id,start_angle, end_angle):
        self.center = arc.center
        self.radius = arc.radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.normal = arc.normal
        self.view_id = view_id

        # 计算起点和终点
        self.start_point = start_point
        self.end_point = end_point
