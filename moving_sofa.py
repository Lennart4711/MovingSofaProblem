import pygame
pygame.init()

from sofa import Sofa
from pygame.math import Vector2
from polygon import Polygon
from genetic_sofa import generate_points, mutate_polygon


# Settings
WIDTH = 800
HEIGHT = 600
FPS = 0
SOFA_COLOR = (255, 0, 0)
AREA_WEIGHT = 1
DISTANCE_WEIGHT = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# walls are tuples of start and end points
walls = [
    (Vector2(0,0), Vector2(400,0)),
    (Vector2(0,100), Vector2(300,100)),
    (Vector2(400,0), Vector2(400,400)),
    (Vector2(300,100), Vector2(300,400)),
]



# Create sofa object
sofa_shape = Polygon([Vector2(0, 0), Vector2(0, 50), Vector2(25,-25),Vector2(50, 50),  Vector2(50,0)])  # Rectangular shape
print(sofa_shape.is_self_intersecting())
#sofa = Sofa(Vector2(25,25), sofa_shape, walls)

def new_generation(n: int):
    sofas = []
    for i in range(n):
        generated_polygon = generate_points(Vector2(0,0), 15, 100)
        sofa = Sofa(Vector2(100,50), Polygon(generated_polygon), walls)
        while sofa.polygon.is_self_intersecting() or sofa.intersects_wall():
            generated_polygon = generate_points(Vector2(0,0), 15, 100)
            sofa = Sofa(Vector2(100,50), Polygon(generated_polygon), walls)
        sofas.append(sofa)
    return sofas

def calculate_fitness(sofa: Sofa):
    # Distance to goal (350, 400)
    distance = Vector2(350, 400).distance_to(sofa.polygon.get_center() + sofa.pos)
    # Area of sofa
    area = sofa.polygon.area()
    return (area * AREA_WEIGHT) / (distance * DISTANCE_WEIGHT)


GENERATION_SIZE = 15
MUTATION_RATE = 0.3
MAX_MUTATION = 0.5
sofas = new_generation(GENERATION_SIZE)

counter = 0
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for sofa in sofas:
        # if y coordinate of center of sofa is less than 400, move sofa down
        if sofa.polygon.get_center().y + sofa.pos.y < 400:
            sofa.steer(1,1,1)

    screen.fill((255, 255, 255))
    for wall in walls:
        pygame.draw.line(screen, (0, 0, 0), wall[0], wall[1], 2)  # Draw walls

    # Draw sofa shape at sofa position
    for sofa in sofas:
        points = sofa.polygon.points
        num_points = len(points)
        for i in range(num_points):
            start = points[i]
            end = points[(i + 1) % num_points]
            pygame.draw.line(screen, SOFA_COLOR, (start[0] + sofa.pos.x, start[1] + sofa.pos.y), (end[0] + sofa.pos.x, end[1] + sofa.pos.y), 2)
        
        center = sofa.polygon.get_center()
        pygame.draw.circle(screen, (0, 0, 0), (int(center.x + sofa.pos.x), int(center.y + sofa.pos.y)), 2)

    pygame.display.flip()
    clock.tick(FPS)

    if counter == 700:
        new_shapes = new_generation(GENERATION_SIZE)
        
pygame.quit()
