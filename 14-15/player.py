import pygame
import os
from animations import Animation

GRAVITY = 0.8
JUMP_POWER = -15
MOVE_SPEED = 6

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")


class Player:
    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 64, 64)
        self.facing_right = True
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.state = "IDLE"
        self.debug = False

        # ===== ЗАВАНТАЖЕННЯ ФОТО =====
        idle_frames = [
            pygame.image.load(os.path.join(ASSETS, "idle_0.png")).convert_alpha()
        ]

        run_frames = [
            pygame.image.load(os.path.join(ASSETS, "run_01.png")).convert_alpha(),
            pygame.image.load(os.path.join(ASSETS, "run_11.png")).convert_alpha()
        ]

        jump_frames = [
            pygame.image.load(os.path.join(ASSETS, "jump_0.png")).convert_alpha(),
            pygame.image.load(os.path.join(ASSETS, "jump_1.png")).convert_alpha()
        ]

        self.animations = {
            "IDLE": Animation(idle_frames, 30),
            "RUN": Animation(run_frames, 10),
            "JUMP": Animation(jump_frames, 30)
        }

    # INPUT
    def handle_input(self, keys):
        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x = -MOVE_SPEED
            self.facing_right = False

        if keys[pygame.K_RIGHT]:
            self.vel_x = MOVE_SPEED
            self.facing_right = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER

    # GRAVITY
    def apply_gravity(self):
        self.vel_y += GRAVITY

    # COLLISION (X → Y)
    def move_and_collide(self, colliders):

        # ---- X ----
        self.rect.x += self.vel_x
        for rect in colliders:
            if self.rect.colliderect(rect):
                if self.vel_x > 0:
                    self.rect.right = rect.left
                elif self.vel_x < 0:
                    self.rect.left = rect.right

        # ---- Y ----
        self.rect.y += self.vel_y
        self.on_ground = False

        for rect in colliders:
            if self.rect.colliderect(rect):
                if self.vel_y > 0:
                    self.rect.bottom = rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = rect.bottom
                    self.vel_y = 0

    # STATE MACHINE
    def update_state(self):
        if not self.on_ground:
            self.state = "JUMP"
        elif self.vel_x != 0:
            self.state = "RUN"
        else:
            self.state = "IDLE"

    def update_animation(self):
        self.animations[self.state].update()

    def draw(self, screen, font):
        frame = self.animations[self.state].get_frame()

        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(frame, self.rect)

        if self.debug:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 2)
            text = font.render(self.state, True, (255, 255, 255))
            screen.blit(text, (10, 10))

        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
