import pygame
import sys
import os
from player import Player
from ui import Button
from hud import HUD
from inventory import Inventory

pygame.init()

# --- BASE RESOLUTION ---
BASE_WIDTH, BASE_HEIGHT = 800, 450
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("практична робота №14–15")
base_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

# --- FONT ---
font_path = os.path.join(ASSETS, "Roboto_Condensed-Black.ttf")
font = pygame.font.Font(font_path, 24)

# --- BACKGROUND ---
background = pygame.image.load(os.path.join(ASSETS, "bg.jpg")).convert()
background = pygame.transform.scale(background, (BASE_WIDTH, BASE_HEIGHT))

platform_img = pygame.image.load(os.path.join(ASSETS, "platform.png")).convert_alpha()

platforms = [
    pygame.Rect(100, 350, 200, 40),
    pygame.Rect(400, 300, 200, 40),
    pygame.Rect(650, 250, 120, 40)
]

# ===== STATES =====
MAIN_MENU = "MAIN_MENU"
GAME = "GAME"
PAUSE = "PAUSE"
INVENTORY = "INVENTORY"

state = MAIN_MENU

player = Player(100, 200)
hud = HUD(font)
inventory = Inventory(font)

# --- MENU BUTTONS ---
btn_play = Button(300, 150, 200, 50, "Грати", font)
btn_exit = Button(300, 230, 200, 50, "Вийти", font)

menu_buttons = [btn_play, btn_exit]
menu_index = 0

pause_buttons = [
    Button(300, 150, 200, 50, "Продовжити", font),
    Button(300, 220, 200, 50, "В меню", font),
    Button(300, 290, 200, 50, "Вийти", font)
]
pause_index = 0


def reset_game():
    hud.reset()
    player.rect.topleft = (100, 200)


# ================== MAIN LOOP ==================
running = True
while running:
    dt = clock.tick(60) / 1000

    mouse_x, mouse_y = pygame.mouse.get_pos()
    scale_x = BASE_WIDTH / WINDOW_WIDTH
    scale_y = BASE_HEIGHT / WINDOW_HEIGHT
    mouse_base = (mouse_x * scale_x, mouse_y * scale_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ================== MAIN MENU ==================
        if state == MAIN_MENU:

            # Mouse
            for b in menu_buttons:
                b.handle_event(event, mouse_base)

            if btn_play.clicked:
                reset_game()
                state = GAME

            if btn_exit.clicked:
                running = False

            # Keyboard
            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_DOWN, pygame.K_TAB):
                    menu_index = (menu_index + 1) % len(menu_buttons)

                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(menu_buttons)

                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if menu_index == 0:
                        reset_game()
                        state = GAME
                    if menu_index == 1:
                        running = False

        # ================== GAME ==================
        elif state == GAME:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = PAUSE
                if event.key == pygame.K_y:
                    inventory.open()
                    state = INVENTORY
                if event.key == pygame.K_h:
                    hud.change_hp(-10)
                if event.key == pygame.K_j:
                    hud.change_hp(10)
                if event.key == pygame.K_SPACE:
                    hud.add_score(1)

        # ================== PAUSE ==================
        elif state == PAUSE:

            for b in pause_buttons:
                b.handle_event(event, mouse_base)

            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_DOWN, pygame.K_TAB):
                    pause_index = (pause_index + 1) % len(pause_buttons)

                if event.key == pygame.K_UP:
                    pause_index = (pause_index - 1) % len(pause_buttons)

                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if pause_index == 0:
                        state = GAME
                    if pause_index == 1:
                        state = MAIN_MENU
                    if pause_index == 2:
                        running = False

                if event.key == pygame.K_ESCAPE:
                    state = GAME

        # ================== INVENTORY ==================
        elif state == INVENTORY:
            inventory.handle_event(event, mouse_base)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                inventory.close()

    # ================== UPDATE ==================
    if state == GAME:
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.apply_gravity()
        player.move_and_collide(platforms)
        player.update_state()
        player.update_animation()
        hud.update(dt)

    if state == INVENTORY:
        inventory.update(dt)
        if inventory.is_closed():
            state = GAME

    # ================== DRAW ==================
    base_surface.blit(background, (0, 0))

    if state in (GAME, PAUSE, INVENTORY):
        for p in platforms:
            scaled_platform = pygame.transform.scale(platform_img, (p.width, p.height))
            base_surface.blit(scaled_platform, p.topleft)

        player.draw(base_surface, font)
        hud.draw(base_surface)

    if state == MAIN_MENU:
        for i, b in enumerate(menu_buttons):
            if i == menu_index:
                pygame.draw.rect(base_surface, (255, 255, 0),
                                 b.rect.inflate(6, 6), 3)
            b.draw(base_surface)

    if state == PAUSE:
        overlay = pygame.Surface((BASE_WIDTH, BASE_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        base_surface.blit(overlay, (0, 0))

        for i, b in enumerate(pause_buttons):
            if i == pause_index:
                pygame.draw.rect(base_surface, (255, 255, 0),
                                 b.rect.inflate(6, 6), 3)
            b.draw(base_surface)

    if state == INVENTORY:
        inventory.draw(base_surface)

    scaled = pygame.transform.scale(base_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled, (0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()