import pygame
import sys

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WALL_THICKNESS = 10

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Hallway dimensions
hallway_width = WIDTH // 2
hallway_height = HEIGHT // 2

# Create walls
walls = [
    pygame.Rect(0, 0, WIDTH, WALL_THICKNESS),  # Top wall
    pygame.Rect(0, 0, WALL_THICKNESS, HEIGHT),  # Left wall
    pygame.Rect(WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT),  # Right wall
    pygame.Rect(0, HEIGHT - WALL_THICKNESS, WIDTH, WALL_THICKNESS),  # Bottom wall
    pygame.Rect(hallway_width - WALL_THICKNESS, 0, WALL_THICKNESS, hallway_height),  # Vertical wall
    pygame.Rect(hallway_width - WALL_THICKNESS, hallway_height, hallway_width + WALL_THICKNESS, WALL_THICKNESS),  # Horizontal wall
]

# Sofa class
class Sofa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 100))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_q]:
            self.angle += 5
            if self.angle >= 360:
                self.angle = 0
        if keys[pygame.K_e]:
            self.angle -= 5
            if self.angle < 0:
                self.angle = 355

        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotate(pygame.Surface((50, 100)), self.angle)
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=self.rect.center)

    def collide_with_walls(self):
        for wall in walls:
            if self.rect.colliderect(wall):
                return True
        return False


# Create sofa object
sofa = Sofa(WIDTH // 2, HEIGHT // 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(sofa)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Collision detection
    if sofa.collide_with_walls():
        sofa.rect.x -= 5
        sofa.rect.y -= 5

    # Render
    screen.fill(WHITE)
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
