import pygame
import random
import os

# НАЛАШТУВАННЯ
WIDTH, HEIGHT = 800, 600
FPS = 60

WORLD_WIDTH, WORLD_HEIGHT = 3000, 3000
PLAYER_SPEED = 250

BG_COLOR = (40, 40, 60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Практична робота №7–8")
    clock = pygame.time.Clock()

    # ЗАВАНТАЖЕННЯ СПРАЙТІВ (Урок 29)
    BASE_DIR = os.path.dirname(__file__)
    IMG_DIR = os.path.join(BASE_DIR, "img")

    walk_right = [
        pygame.image.load(os.path.join(IMG_DIR, "player1.png")).convert_alpha(),
        pygame.image.load(os.path.join(IMG_DIR, "player2.png")).convert_alpha(),
        pygame.image.load(os.path.join(IMG_DIR, "player3.png")).convert_alpha(),
    ]

    tree_img = pygame.image.load(os.path.join(IMG_DIR, "tree.png")).convert_alpha()

    PLAYER_W, PLAYER_H = walk_right[0].get_size()

    # ГРАВЕЦЬ (СВІТОВІ КООРДИНАТИ)
    player_world_x = WORLD_WIDTH // 2
    player_world_y = WORLD_HEIGHT // 2
    player_rect = pygame.Rect(player_world_x, player_world_y, PLAYER_W, PLAYER_H)

    # АНІМАЦІЯ
    current_frame = 0.0
    animation_speed = 0.15
    is_moving = False
    facing_right = True

    # ДЕКОРАЦІЇ
    trees = []
    for _ in range(50):
        x = random.randint(0, WORLD_WIDTH)
        y = random.randint(0, WORLD_HEIGHT)
        trees.append(pygame.Rect(x, y, tree_img.get_width(), tree_img.get_height()))

    # ІГРОВИЙ ЦИКЛ
    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        # ПОДІЇ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # КЕРУВАННЯ
        keys = pygame.key.get_pressed()
        dx = dy = 0
        is_moving = False

        current_speed = PLAYER_SPEED
        current_anim_speed = animation_speed

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            current_speed *= 1.0
            current_anim_speed *= 1.5

        if keys[pygame.K_LEFT]:
            dx -= current_speed * dt
            facing_right = False
            is_moving = True
        if keys[pygame.K_RIGHT]:
            dx += current_speed * dt
            facing_right = True
            is_moving = True
        if keys[pygame.K_UP]:
            dy -= current_speed * dt
            is_moving = True
        if keys[pygame.K_DOWN]:
            dy += current_speed * dt
            is_moving = True

        player_world_x += dx
        player_world_y += dy

        # МЕЖІ СВІТУ
        player_world_x = max(0, min(WORLD_WIDTH - PLAYER_W, player_world_x))
        player_world_y = max(0, min(WORLD_HEIGHT - PLAYER_H, player_world_y))

        player_rect.x = player_world_x
        player_rect.y = player_world_y

        # АНІМАЦІЯ (Модуль 1 + 2)
        if is_moving:
            current_frame += current_anim_speed
            if current_frame >= len(walk_right):
                current_frame = 0
        else:
            current_frame = 0

        player_img = walk_right[int(current_frame)]

        # ВІДЗЕРКАЛЕННЯ
        if not facing_right:
            player_img = pygame.transform.flip(player_img, True, False)

        # КАМЕРА
        offset_x = player_world_x - WIDTH // 2
        offset_y = player_world_y - HEIGHT // 2

        offset_x = max(0, min(WORLD_WIDTH - WIDTH, offset_x))
        offset_y = max(0, min(WORLD_HEIGHT - HEIGHT, offset_y))

        # МАЛЮВАННЯ
        screen.fill(BG_COLOR)

        for tree in trees:
            screen.blit(
                tree_img,
                (tree.x - offset_x, tree.y - offset_y)
            )

        screen.blit(
            player_img,
            (player_world_x - offset_x, player_world_y - offset_y)
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()