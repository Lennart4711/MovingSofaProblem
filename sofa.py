import pygame
from pygame.math import Vector2 # type: ignore
from polygon import Polygon
from geometry import lines_intersect

MOVEMENT_SPEED = 2
ROTATION_SPEED = 2

# Sofa class, polygon is a list of points that represents the shape of the sofa
class Sofa(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, polygon: Polygon, walls: list):
        self.pos: Vector2 = pos
        self.polygon: Polygon = polygon
        self.walls = walls


    def update(self):
        pos_before = self.pos.copy()
        polygon_before = self.polygon.copy()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(0, -MOVEMENT_SPEED)
        if keys[pygame.K_s]:
            self.move(0, MOVEMENT_SPEED)
        if keys[pygame.K_a]:
            self.move(-MOVEMENT_SPEED, 0)
        if keys[pygame.K_d]:
            self.move(MOVEMENT_SPEED, 0)
        if keys[pygame.K_q]:
            self.rotate(-ROTATION_SPEED)
        if keys[pygame.K_e]:
            self.rotate(ROTATION_SPEED)

        # Check for collisions
        if self.intersects_wall():
            self.pos = pos_before
            self.polygon = polygon_before
    def steer(self, x,y, angle):
        pos_before_x_movement = self.pos.copy()
        polygon_before_x_movement = self.polygon.copy()
        self.move(x,0)
        if self.intersects_wall():
            self.pos = pos_before_x_movement
            self.polygon = polygon_before_x_movement
        pos_before_y_movement = self.pos.copy()
        polygon_before_y_movement = self.polygon.copy()
        self.move(0,y)
        if self.intersects_wall():
            self.pos = pos_before_y_movement
            self.polygon = polygon_before_y_movement
        pos_before_rotation = self.pos.copy()
        polygon_before_rotation = self.polygon.copy()
        self.rotate(angle)
        if self.intersects_wall():
            self.pos = pos_before_rotation
            self.polygon = polygon_before_rotation




    def move(self, x, y):   
        self.pos.x += x
        self.pos.y += y

    def rotate(self, angle):
        self.polygon.rotate(angle)

    def create_lines(self):
        points = self.polygon.points
        num_points = len(points)
        return [
            (points[i] + self.pos, points[(i + 1) % num_points] + self.pos)
            for i in range(num_points)
        ]
        
    def intersects_wall(self) -> bool:
        for wall in self.walls:
            for line in self.create_lines():
                if lines_intersect(line, wall):
                    return True
        return False