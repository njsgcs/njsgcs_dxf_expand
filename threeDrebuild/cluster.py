import math

class Cluster:
    def __init__(self, lines=None):
        if lines is None:
            lines = []
        self.lines = lines.copy()
        self.min_x = math.inf
        self.max_x = -math.inf
        self.min_y = math.inf
        self.max_y = -math.inf

        if self.lines:
            self.update_bounds()

    def update_bounds(self):
        self.min_x = min([line[0] for line in self.lines] + [line[2] for line in self.lines])
        self.max_x = max([line[0] for line in self.lines] + [line[2] for line in self.lines])
        self.min_y = min([line[1] for line in self.lines] + [line[3] for line in self.lines])
        self.max_y = max([line[1] for line in self.lines] + [line[3] for line in self.lines])

    @property
    def length_x(self):
        return round(self.max_x - self.min_x, 1)

    @property
    def length_y(self):
        return round(self.max_y - self.min_y, 1)
    

def cluster_lines(lines, expand_distance=5):
    clusters = []
    remaining_lines = lines.copy()

    while remaining_lines:
        seed = remaining_lines.pop(0)
        current_cluster = Cluster([seed])
        current_cluster.update_bounds()

        changed = True

        while changed:
            changed = False
            expanded_min_x = current_cluster.min_x - expand_distance
            expanded_max_x = current_cluster.max_x + expand_distance
            expanded_min_y = current_cluster.min_y - expand_distance
            expanded_max_y = current_cluster.max_y + expand_distance

            to_add = []

            for line in list(remaining_lines):
                x1, y1, x2, y2, line_id, line_type = line
                in_bound = (
                    (expanded_min_x <= x1 <= expanded_max_x and expanded_min_y <= y1 <= expanded_max_y) or
                    (expanded_min_x <= x2 <= expanded_max_x and expanded_min_y <= y2 <= expanded_max_y)
                )

                if in_bound:
                    to_add.append(line)
                    changed = True

            for line in to_add:
                current_cluster.lines.append(line)
                remaining_lines.remove(line)

            current_cluster.update_bounds()

        # 合并完全覆盖的聚类
        for i in range(len(clusters)):
            cluster = clusters[i]
            if (
                current_cluster.min_x <= cluster.min_x and
                current_cluster.min_y <= cluster.min_y and
                current_cluster.max_x >= cluster.max_x and
                current_cluster.max_y >= cluster.max_y
            ):
                current_cluster.lines.extend(cluster.lines)
                clusters.pop(i)
                break

        clusters.append(current_cluster)

    return clusters