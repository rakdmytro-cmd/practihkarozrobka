import pygame

class Button:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.clicked = False
        self.hover = False

    def handle_event(self, event, mouse_pos):
        self.clicked = False
        self.hover = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP and self.hover:
            self.clicked = True

    def draw(self, surface):
        color = (200, 200, 200) if self.hover else (150, 150, 150)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255,255,0), self.rect, 2)

        text_surf = self.font.render(self.text, True, (0,0,0))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))