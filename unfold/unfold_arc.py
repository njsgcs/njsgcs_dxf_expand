from collections import deque
import networkx as nx
import transforms3d
import numpy as np
from interferce import *
from pyautocad import Autocad, APoint

class UnfoldProcessor:
    def __init__(self , lines, arcs, circles, center_arc_map, component_id_map,delete):
        acad= Autocad(create_if_not_exists=True)
        self.acad = acad
        self.lines = lines
        self.arcs = arcs
        self.circles = circles
        self.delete=delete
        self.center_arc_map = center_arc_map
        self.component_id_map = component_id_map
        self.draw_lines=set({})
        self.draw_circles=set({})
    # 定义一个函数transform_edge，用于转换边
    def translation_matrix(self,translation):
        mat = np.eye(4)
        mat[:3, 3] = translation
        return mat
    def rotation_matrix_from_axis_angle(self,axis, angle):
        # 使用 transforms3d 创建 3x3 旋转变换矩阵
        R = transforms3d.axangles.axangle2mat(axis, angle)
        # 将其扩展为 4x4 齐次变换矩阵
        mat = np.eye(4)
        mat[:3, :3] = R
        return mat
    def transform_edge(self,edge_name, last_transform,component_points):
        arc:Arc3D = self.center_arc_map[edge_name]
        center = np.array(arc.center)  # 将 center 转换为 numpy 数组
        normal = np.array(arc.normal)  # 将 normal 转换为 numpy 数组
        start_point = arc.start_point
        start_point_in_component = start_point in component_points

        rangle = arc.end_angle-arc.start_angle if  start_point_in_component else arc.start_angle-arc.end_angle # 旋转
        start_angle = arc.start_angle if start_point_in_component else arc.end_angle
        end_angle = arc.end_angle if start_point_in_component else arc.start_angle
        if start_point_in_component:
            print(f"in,      {start_angle*180/np.pi}      {end_angle*180/np.pi}     {rangle*180/np.pi}")
        else:
            print(f"not_in,  {start_angle*180/np.pi}      {end_angle*180/np.pi}     {rangle*180/np.pi}")
        # 创建绕法向量在中心点的旋转变换矩阵
        nomal_name=edge_name[-1]
    # print(f"normal: {nomal_name}")
        if nomal_name=="Z": rangle=- rangle
        rotation_matrix = self.rotation_matrix_from_axis_angle(normal, rangle)
        
        center_translation_matrix =self.translation_matrix(center)
        
        center_inverse_translation_matrix =self.translation_matrix(-center)
        # 组合变换：先平移到原点，旋转，再平移回中心
        new_transform = np.dot(center_translation_matrix, np.dot(rotation_matrix,center_inverse_translation_matrix))

        # 将新的变换矩阵与之前的变换矩阵组合
        final_transform = np.dot(last_transform, new_transform)

        return final_transform
    def excuse_transform(self,node,component_points, component_edges ,last_transform):
        z_translation_matrix =self.translation_matrix([0, 0, 50])
        z_last_transform = np.dot(z_translation_matrix, last_transform)
        min_x, min_y,min_z = np.min(component_points, axis=0)
        max_x, max_y,max_z = np.max(component_points, axis=0) 
        circle_in_component = []
        for circle in self.circles:
            if min_x <= circle.center[0] <= max_x and min_y <= circle.center[1] <= max_y and min_z <= circle.center[2] <= max_z:
                circle_in_component.append(circle)
        for circle in circle_in_component:
            center=circle.center
            radius=circle.radius
            normal=circle.normal
            center_homogeneous=np.append(center,1)
            transform_center=np.dot(z_last_transform, center_homogeneous)
            transform_center=transform_center[:3]
            x,y,z=transform_center.tolist()
            normal_homogeneous=np.append(normal,0)
            transform_normal=np.dot(z_last_transform, normal_homogeneous)
            transform_normal=transform_normal[:3]
        
            
            transformed_circle=self.acad.model.AddCircle(APoint(x, y, z), radius)
          
            normal_x,normal_y,normal_z=transform_normal.tolist()
            transformed_circle.normal=APoint(normal_x,normal_y,normal_z)
            if self.delete:
                transformed_circle.Delete()
            self.draw_circles.add(((x, y, 0), radius))


        for edge in component_edges:
            # 获取边的两个顶点
            u, v = edge
            u_homogeneous = np.append(u, 1)
            v_homogeneous = np.append(v, 1)
            
            transform_u=np.dot(z_last_transform, u_homogeneous)
            transform_v=np.dot(z_last_transform, v_homogeneous)
        
            transform_u = transform_u[:3]
            transform_v = transform_v[:3]

            x1, y1, z1 = transform_u.tolist()
            x2, y2, z2 = transform_v.tolist()
            #其中 1 是红色，2 是黄色，3 是绿色，4 是蓝色，5 是紫色，6 是青色，7 是灰色，8 是白色
            line=self.acad.model.AddLine(APoint(x1, y1, z1), APoint(x2, y2, z2))
            line.color=node
            if self.delete:
                line.Delete()
            self.draw_lines.add(((x1 , y1, 0), (x2, y2, 0)))



        pass
    def dfs(self,graph: nx.Graph, node, visited, last_transform):
        # 访问当前节点
        print(node)
        visited.add(node)
        component_edges=self.component_id_map[node]["component_edges"]
        component_points=self.component_id_map[node]["component_points"]
        self.excuse_transform(node,component_points, component_edges, last_transform)
        # 遍历邻居节点
        for neighbor in graph[node]:
            if neighbor not in visited:
                edge_data = graph.get_edge_data(node, neighbor)
                edge_name = edge_data.get('name', 'No name')
                print(f"Edge: {node} -> {neighbor}, Name: {edge_name}")
                
                # 变换边并更新 last_transform
                new_transform = self.transform_edge(edge_name, last_transform,
                component_points                          )
            
                
                # 递归访问邻居节点
                self.dfs(graph, neighbor, visited, new_transform)
    def drawlines(self,height_diff):
        acad = self.acad
        distance=3*height_diff
        for line in self.draw_lines:
            start_point,end_point  = line
            
            acad.model.AddLine(APoint(start_point[0], start_point[1]+distance, start_point[2]), APoint(end_point[0], end_point[1]+distance, end_point[2]))
        for circle in self.draw_circles:
            center,  radius = circle
          
            acad.model.AddCircle(APoint(center[0], center[1]+distance, center[2]), radius)
   