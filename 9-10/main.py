import pygame
import os
from player import Player

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer State Machine")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# ===== ФОН =====
background = pygame.image.load(os.path.join(ASSETS, "bg.jpg")).convert()

# ===== ПЛАТФОРМА ФОТО =====
platform_img = pygame.image.load(os.path.join(ASSETS, "platform.png")).convert_alpha()

colliders = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(200, 450, 200, 20),
    pygame.Rect(500, 350, 200, 20),
]

player = Player(100, 300)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.debug = not player.debug

    keys = pygame.key.get_pressed()

    player.handle_input(keys)
    player.apply_gravity()
    player.move_and_collide(colliders)
    player.update_state()
    player.update_animation()

    # ===== DRAW =====
    screen.blit(background, (0, 0))

    for rect in colliders:
        screen.blit(platform_img, rect)

        if player.debug:
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    player.draw(screen, font)

    pygame.display.flip()

pygame.quit()
