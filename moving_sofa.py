import math
import pygame
from pygame.math import Vector2
pygame.init()


# Settings
WIDTH = 800
HEIGHT = 600
FPS = 60
SOFA_COLOR = (255, 0, 0)
MOVEMENT_SPEED = 2
ROTATION_SPEED = 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# walls are tuples of start and end points
walls = [
    (Vector2(0,0), Vector2(400,0)),
    (Vector2(0,100), Vector2(300,100)),
    (Vector2(400,0), Vector2(400,300)),
    (Vector2(300,100), Vector2(300,300)),
]

class Polygon:
    def __init__(self, points) -> None:
        self.points = points

    def get_center(self):
        x = 0
        y = 0
        for point in self.points:
            x += point[0]
            y += point[1]
        return Vector2(x/len(self.points), y/len(self.points))
    
    # rotate the polygon around its center
    
    def rotate(self, angle_degrees):
        center = self.get_center()
        angle_radians = math.radians(angle_degrees)
        rotated_points = []
        for point in self.points:
            # Translate the point to the origin by subtracting the center coordinates
            translated_point = point - center

            # Rotate the translated point around the origin
            rotated_x = translated_point.x * math.cos(angle_radians) - translated_point.y * math.sin(angle_radians)
            rotated_y = translated_point.x * math.sin(angle_radians) + translated_point.y * math.cos(angle_radians)

            # Translate the rotated point back to the original position by adding the center coordinates
            rotated_point = Vector2(rotated_x, rotated_y) + center

            rotated_points.append(rotated_point)

        self.points = rotated_points

    def copy(self):
        return Polygon(self.points.copy())


# Sofa class, polygon is a list of points that represents the shape of the sofa
class Sofa(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, polygon: Polygon):
        self.pos: Vector2 = pos
        self.polygon: Polygon = polygon


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
            self.rotate(ROTATION_SPEED)
        if keys[pygame.K_e]:
            self.rotate(-ROTATION_SPEED)

        # Check for collisions
        if self.collides():
            self.pos = pos_before
            self.polygon = polygon_before
    
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
        
    def collides(self):
        for wall in walls:
            for line in self.create_lines():
                if lines_intersect(line, wall):
                    return True
        return False
    

def lines_intersect(line1, line2) -> bool:
    A = line1[0]
    B = line1[1]
    C = line2[0]
    D = line2[1]
    return intersect(A, B, C, D)

def ccw(p1: Vector2, p2: Vector2, p3: Vector2) -> bool:
    return (p3.y - p1.y) * (p2.x - p1.x) > (p2.y - p1.y) * (p3.x - p1.x)

def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def is_polygon_self_intersecting(points):
    n = len(points)
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        for j in range(i + 2, n):
            p3 = points[j]
            p4 = points[(j + 1) % n]
            if intersect(p1, p2, p3, p4):
                return True
    return False


# Create sofa object
sofa_shape = Polygon([Vector2(0, 0), Vector2(0, 50), Vector2(50, 50), Vector2(25,-25), Vector2(50,0)])  # Rectangular shape
sofa = Sofa(Vector2(25,25), sofa_shape)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    sofa.update()

    # Render
    screen.fill((255, 255, 255))
    for wall in walls:
        pygame.draw.line(screen, (0, 0, 0), wall[0], wall[1], 2)  # Draw walls

    # Draw sofa shape at sofa position
    points = sofa.polygon.points
    num_points = len(points)
    for i in range(num_points):
        start = points[i]
        end = points[(i + 1) % num_points]
        pygame.draw.line(screen, SOFA_COLOR, (start[0] + sofa.pos.x, start[1] + sofa.pos.y), (end[0] + sofa.pos.x, end[1] + sofa.pos.y), 2)
    
    # draw a circle at the center of the sofa
    center = sofa.polygon.get_center()
    pygame.draw.circle(screen, (0, 0, 0), (int(center.x + sofa.pos.x), int(center.y + sofa.pos.y)), 2)

    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
