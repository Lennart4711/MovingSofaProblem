from pygame.math import Vector2


def lines_intersect(line1, line2) -> bool:
    A = line1[0]
    B = line1[1]
    C = line2[0]
    D = line2[1]
    return intersect(A, B, C, D)

def ccw(p1: Vector2, p2: Vector2, p3: Vector2) -> bool:
    return (p3.y - p1.y) * (p2.x - p1.x) > (p2.y - p1.y) * (p3.x - p1.x)

def intersect(A: Vector2, B: Vector2, C: Vector2, D: Vector2) -> bool:
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
