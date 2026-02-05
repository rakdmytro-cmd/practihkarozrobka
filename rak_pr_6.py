import pygame

# НАЛАШТУВАННЯ
WIDTH, HEIGHT = 800, 600
FPS = 60

BG_COLOR = (30, 30, 40)
PLAYER_COLOR = (80, 200, 120)

PLAYER_SIZE = 50
PLAYER_SPEED = 250  # px / sec


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Практичне №6")
    clock = pygame.time.Clock()

    # ОБ'ЄКТ
    player = pygame.Rect(100, 100, PLAYER_SIZE, PLAYER_SIZE)

    running = True
    while running:
        #  ЧАС 
        dt = clock.tick(FPS) / 1000  # секунди між кадрами

        #  ПОДІЇ 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ЛОГІКА 
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= int(PLAYER_SPEED * dt)
        if keys[pygame.K_RIGHT]:
            player.x += int(PLAYER_SPEED * dt)
        if keys[pygame.K_UP]:
            player.y -= int(PLAYER_SPEED * dt)
        if keys[pygame.K_DOWN]:
            player.y += int(PLAYER_SPEED * dt)

        # Обмеження руху в межах екрану
        player.x = max(0, min(WIDTH - player.width, player.x))
        player.y = max(0, min(HEIGHT - player.height, player.y))

        #  МАЛЮВАННЯ 
        screen.fill(BG_COLOR) 
        pygame.draw.rect(screen, PLAYER_COLOR, player)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()