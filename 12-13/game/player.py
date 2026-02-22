import pygame
import time
from common.constants import *

class Player:
    def __init__(self, pid, x, y):
        self.id = pid
        self.rect = pygame.Rect(x, y, 40, 40)

        self.vx = 0
        self.vy = 0

        self.hp = MAX_HP
        self.alive = True

        self.last_attack = 0
        self.respawn_timer = 0

        self.state = "IDLE"

    def apply_input(self, mx, my):
        if not self.alive:
            return

        self.vx = mx * MOVE_SPEED
        self.vy = my * MOVE_SPEED

    def update_state(self):
        if not self.alive:
            self.state = "DEAD"
        elif self.vx != 0 or self.vy != 0:
            self.state = "RUN"
        else:
            self.state = "IDLE"

    def can_attack(self):
        return time.time() - self.last_attack >= ATTACK_COOLDOWN

    def do_attack(self):
        self.last_attack = time.time()