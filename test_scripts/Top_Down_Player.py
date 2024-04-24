import pygame
import sys

class Player:
    def __init__(self, x, y, sprite_path, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(sprite_path)
        self.rect = self.image.get_rect()

    def move(self, keys, width, height):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Boundary checking
        if self.x < 0:
            self.x = 0
        elif self.x > width - self.rect.width:
            self.x = width - self.rect.width
        if self.y < 0:
            self.y = 0
        elif self.y > height - self.rect.height:
            self.y = height - self.rect.height

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Pygame")

# Player attributes
player_speed = 5
player_sprite_path = "Green_man.png"
player = Player(WIDTH, HEIGHT // 2, player_sprite_path, player_speed)

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill((255, 255, 255))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    player.move(keys, WIDTH, HEIGHT)

    # Draw player
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
