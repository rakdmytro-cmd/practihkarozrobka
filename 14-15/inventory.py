import pygame

class Inventory:
    def __init__(self, font):
        self.font = font
        self.cols = 6
        self.rows = 4
        self.slots = [None]*24
        self.selected = None

        self.open_progress = 0
        self.opening = False
        self.closing = False

        # тест предмет
        self.slots[0] = {"id":"Potion", "count":3}

    def open(self):
        self.opening = True
        self.closing = False

    def close(self):
        self.closing = True
        self.opening = False

    def is_closed(self):
        return self.open_progress <= 0 and self.closing

    def update(self, dt):
        speed = 3
        if self.opening:
            self.open_progress += speed*dt
            if self.open_progress >= 1:
                self.open_progress = 1
        if self.closing:
            self.open_progress -= speed*dt
            if self.open_progress <= 0:
                self.open_progress = 0

    def handle_event(self, event, mouse):
        if event.type == pygame.MOUSEBUTTONUP:
            for i, rect in enumerate(self.get_slot_rects()):
                if rect.collidepoint(mouse):
                    self.selected = i

    def get_slot_rects(self):
        rects = []
        start_x = 200
        start_y = 100 + (1-self.open_progress)*300
        size = 60

        for r in range(self.rows):
            for c in range(self.cols):
                rects.append(
                    pygame.Rect(start_x+c*70,
                                start_y+r*70,
                                size,size))
        return rects

    def draw(self, surface):
        if self.open_progress <= 0:
            return

        panel = pygame.Surface((500,400), pygame.SRCALPHA)
        panel.fill((40,40,40,200))
        surface.blit(panel,(150,50+(1-self.open_progress)*300))

        rects = self.get_slot_rects()
        mouse = pygame.mouse.get_pos()

        for i, rect in enumerate(rects):
            pygame.draw.rect(surface,(120,120,120),rect,2)

            if i == self.selected:
                pygame.draw.rect(surface,(255,255,0),rect,3)

            if self.slots[i]:
                txt = self.font.render(str(self.slots[i]["count"]),True,(255,255,255))
                surface.blit(txt,(rect.x+5,rect.y+5))

            # TOOLTIP
            if rect.collidepoint(mouse) and self.slots[i]:
                tip = self.font.render(
                    f'{self.slots[i]["id"]} x{self.slots[i]["count"]}',
                    True,(255,255,255))
                pygame.draw.rect(surface,(0,0,0),(mouse[0],mouse[1],150,30))
                surface.blit(tip,(mouse[0]+5,mouse[1]+5))