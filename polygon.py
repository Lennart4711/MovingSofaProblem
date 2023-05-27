import math

from pygame.math import Vector2
from geometry import intersect


class Polygon:
    def __init__(self, points, angle=0) -> None:
        self.points = points
        self.turned_angle = angle

    def get_center(self):
        x = 0
        y = 0
        for point in self.points:
            x += point[0]
            y += point[1]
        return Vector2(x / len(self.points), y / len(self.points))

    def is_self_intersecting(self):
        n = len(self.points)
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            for j in range(i + 2, n):
                p3 = self.points[j]
                p4 = self.points[(j + 1) % n]
                if intersect(p1, p2, p3, p4):
                    return True
        return False

    def rotate(self, angle_degrees):
        self.turned_angle += angle_degrees
        angle_radians = math.radians(angle_degrees)
        center = self.get_center()

        rotated_points = []
        for point in self.points:
            # Translate the point to the origin by subtracting the center coordinates
            translated_point = point - center

            # Rotate the translated point around the origin
            rotated_x = translated_point.x * math.cos(
                angle_radians
            ) - translated_point.y * math.sin(angle_radians)
            rotated_y = translated_point.x * math.sin(
                angle_radians
            ) + translated_point.y * math.cos(angle_radians)

            # Translate the rotated point back to the original position by adding the center coordinates
            rotated_point = Vector2(rotated_x, rotated_y) + center

            rotated_points.append(rotated_point)

        self.points = rotated_points

    def area(self):
        n = len(self.points)
        area = 0
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            area += p1.x * p2.y - p2.x * p1.y
        return abs(area) / 2

    def copy(self):
        return Polygon(self.points.copy(), self.turned_angle)
