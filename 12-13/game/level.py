import pygame
import random
from common.constants import WIDTH, HEIGHT

colliders = [
    pygame.Rect(200, 150, 200, 30),
    pygame.Rect(450, 350, 200, 30),
]

spawnpoints = [
    (100, 100),
    (700, 500),
]

def get_spawn():
    return random.choice(spawnpoints)