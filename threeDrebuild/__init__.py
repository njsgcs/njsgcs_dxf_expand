# threeDrebuild.py 或新建一个主类文件

from .connect import get_lines
from .cluster import cluster_lines
from .create_3d_point import generate_3d_points
from .threedv_3dline import generate_3d_lines
from .draw3d_lines import draw_3d_model


class ThreeDRebuilder:
    def __init__(self, delete):
        self.expand_distance = 5
        self.lines = None
        self.line_map = None
        self.acad = None
        self.clusters = None
        self.result = None
        self.line3d = None
        self.cluster_min_x_r = None
        self.cluster_min_y_t = None
        self.cluster_max_y_t = None
        self.cluster_min_y_f = None
        self.delete=delete

    def load_lines(self):
        """从 DXF 加载线段"""
        self.lines, self.line_map, self.acad = get_lines()

    def perform_clustering(self):
        """对线段进行聚类"""
        if self.lines is None:
            raise ValueError("Lines not loaded. Call load_lines() first.")
        self.clusters = cluster_lines(self.lines, expand_distance=self.expand_distance)

    def generate_3d_points(self):
        """生成 3D 点集合"""
        if self.clusters is None:
            raise ValueError("Clusters not generated. Call perform_clustering() first.")
        self.result = generate_3d_points(self.clusters)

    def generate_3d_lines(self):
        """生成 3D 线段"""
        if self.result is None:
            raise ValueError("3D points not generated. Call generate_3d_points() first.")
        self.line3d = generate_3d_lines(
            self.result["points_3d"],
            self.result["front_lines"],
            self.result["top_lines"],
            self.result["right_lines"],
            self.result["front_points"],
            self.result["top_points"],
            self.result["right_points"]
        )

    def get_min_coords(self):
        """获取聚类的最小坐标"""
        if self.result is None:
            raise ValueError("3D points data not found. Call generate_3d_points() first.")
        self.cluster_min_x_r = self.result.get("right_cluster_min_x")
        self.cluster_min_y_t = self.result.get("top_cluster_min_y")
        self.cluster_max_y_t = self.result.get("top_cluster_max_y")
        self.cluster_min_y_f = self.result.get("front_cluster_min_y")
    def draw_model(self):
        """绘制 3D 模型"""
        if self.acad is None or self.line3d is None:
            raise ValueError("Acad or line3d not ready. Check dependencies.")
        return draw_3d_model(
            self.acad,
            self.line3d,
            self.line_map,
            self.cluster_min_x_r,
            self.cluster_min_y_t,
            self.delete
        )

    def run(self):
        """一键运行整个流程"""
        self.load_lines()
        self.perform_clustering()
        self.generate_3d_points()
        self.generate_3d_lines()
        self.get_min_coords()


        # 获取高度差并处理 None 情况
        height_diff = None
        if self.cluster_max_y_t is not None and self.cluster_min_y_f is not None:
            height_diff = self.cluster_max_y_t - self.cluster_min_y_f
        else:
            # 可根据业务需要设置默认值或抛出异常
            height_diff = 0  
        return self.draw_model(),height_diff