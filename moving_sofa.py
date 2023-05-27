import pygame

pygame.init()

from sofa import Sofa
from pygame.math import Vector2
from polygon import Polygon
from genetic_sofa import mutate_polygon, generate_regular


# Settings
WIDTH = 800
HEIGHT = 600
FPS = 0
SOFA_COLOR = (255, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# walls are tuples of start and end points
walls = [
    (Vector2(0, 0), Vector2(400, 0)),
    (Vector2(0, 100), Vector2(300, 100)),
    (Vector2(400, 0), Vector2(400, 400)),
    (Vector2(300, 100), Vector2(300, 400)),
]


# Create sofa object
sofa_shape = Polygon(
    [Vector2(0, 0), Vector2(0, 50), Vector2(25, -25), Vector2(50, 50), Vector2(50, 0)]
)  # Rectangular shape
print(sofa_shape.is_self_intersecting())
# sofa = Sofa(Vector2(25,25), sofa_shape, walls)


def calculate_fitness(sofa: Sofa):
    distance_travlled_x = sofa.pos.x - 100
    distance_travlled_y = sofa.pos.y - 50
    manhattan_distance = abs(distance_travlled_x) + abs(distance_travlled_y)
    manhattan_distance = min(manhattan_distance, 590)

    area = sofa.polygon.area()
    return area, manhattan_distance


AREA_WEIGHT = 0.1
DISTANCE_WEIGHT = 1

GENERATION_SIZE = 15
MUTATION_RATE = 0.2
MAX_MUTATION = 10
SOFA_EDGES = 15

# Let sofas be a list of sofas that are regular polygons around a center point
sofas = []
for _ in range(GENERATION_SIZE):
    center = Vector2(100, 50)
    points = generate_regular(Vector2(0, 0), SOFA_EDGES, 50)
    sofa = Sofa(center, Polygon(points), walls)
    sofas.append(sofa)


counter = 0
generation_counter = 0
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for sofa in sofas:
        # move until the sofa reaches the goal
        if sofa.polygon.get_center().y + sofa.pos.y < 400:
            sofa.steer(1, 1, 1)

    # ---- Drawing ----
    screen.fill((255, 255, 255))
    for wall in walls:
        pygame.draw.line(screen, (0, 0, 0), wall[0], wall[1], 2)  # Draw walls

    # Draw sofa shape at sofa position
    for sofa in sofas:
        lines = sofa.create_lines()
        for line in lines:
            pygame.draw.line(screen, SOFA_COLOR, line[0], line[1], 2)
        # draw a circle at the center of the sofa
        pygame.draw.circle(screen, (0, 0, 0), (int(sofa.pos.x), int(sofa.pos.y)), 2)

    pygame.display.flip()
    clock.tick(FPS)

    counter += 1
    if counter == 700:
        # set all angles to 0 by rotating the polygon -self.angle degrees
        for sofa in sofas:
            sofa.polygon.rotate(-sofa.polygon.turned_angle)

        # Remove sofas that have a negative area or a manhattan distance < 500
        for sofa in sofas:
            area, distance = calculate_fitness(sofa)
            if area < 0 or distance < 500:
                sofas.remove(sofa)

        # sort sofas by fitness
        sofas.sort(
            key=lambda x: calculate_fitness(x)[0] * AREA_WEIGHT
            + calculate_fitness(x)[1] * DISTANCE_WEIGHT,
            reverse=True,
        )

        new_sofas = [
            Sofa(Vector2(100, 50), Polygon(sofas[i].polygon.points), walls)
            for i in range(5)
        ]
        # create new sofas by mutating the best sofas
        new_sofas.extend(
            Sofa(
                Vector2(100, 50),
                Polygon(
                    mutate_polygon(sofas[i].polygon.points, MUTATION_RATE, MAX_MUTATION)
                ),
                walls,
            )
            for i in range(GENERATION_SIZE - 5)
        )
        sofas = new_sofas
        counter = 0
        generation_counter += 1
        print(
            "Generation: ",
            generation_counter,
            "with best area of",
            calculate_fitness(sofas[0])[0],
        )


pygame.quit()
