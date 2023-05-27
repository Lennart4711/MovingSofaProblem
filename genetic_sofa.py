import math
import random
from pygame.math import Vector2


def generate_regular(c, n, r):
    angle_increment = 2 * math.pi / n
    points = []
    for i in range(n):
        angle = i * angle_increment
        distance = r
        x = c.x + distance * math.cos(angle)
        y = c.y + distance * math.sin(angle)
        points.append(Vector2(x, y))
    return points


# a function that generates a list of n points around a center point
def generate_points(c, n, r):
    angle_increment = 2 * math.pi / n
    points = []
    for i in range(n):
        angle = i * angle_increment
        distance = random.uniform(0, r)
        x = c.x + distance * math.cos(angle)
        y = c.y + distance * math.sin(angle)
        points.append(Vector2(x, y))
    return points


def mutate_polygon(polygon, mutation_rate, max_mutation):
    mutated_polygon = []
    for point in polygon:
        if random.random() < mutation_rate:
            mutated_x = point.x + random.uniform(-max_mutation, max_mutation)
            mutated_y = point.y + random.uniform(-max_mutation, max_mutation)
            mutated_point = Vector2(mutated_x, mutated_y)
            mutated_polygon.append(mutated_point)
        else:
            mutated_polygon.append(point)
    return mutated_polygon
