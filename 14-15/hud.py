import pygame

class HUD:
    def __init__(self, font):
        self.font = font
        self.hp_max = 100
        self.hp = 100
        self.score = 0
        self.time = 0

        self.cached_score = None
        self.cached_time = None
        self.score_surf = None
        self.time_surf = None

    def reset(self):
        self.hp = self.hp_max
        self.score = 0
        self.time = 0

    def update(self, dt):
        self.time += dt

    def change_hp(self, value):
        self.hp = max(0, min(self.hp_max, self.hp + value))

    def add_score(self, val):
        self.score += val

    def draw(self, surface):
        # HP BAR
        #pygame.draw.rect(surface, (100,0,0), (20,20,200,20))
        #pygame.draw.rect(surface, (255,0,0),
        #                 (20,20,200*(self.hp/self.hp_max),20))

        # SCORE кеш
        if self.score != self.cached_score:
            self.cached_score = self.score
            self.score_surf = self.font.render(f"Score: {self.score}", True, (255,255,255))

        surface.blit(self.score_surf, (20, 50))

        # TIME кеш
        minutes = int(self.time)//60
        seconds = int(self.time)%60
        time_str = f"{minutes:02}:{seconds:02}"

        if time_str != self.cached_time:
            self.cached_time = time_str
            self.time_surf = self.font.render(time_str, True, (255,255,255))

        surface.blit(self.time_surf, (700, 20))