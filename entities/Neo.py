import pygame as pg


class Neo:
    SPEED = 1000

    def __init__(self, rect):
        self.rect = rect
        self.x = self.rect.x
        self.y = self.rect.y
        self.dx = 0
        self.dy = 0

    def update(self, dt):
        self.move(dt)

    def draw(self, screen):
        # draw Neo as a rectangle with the given rect
        pg.draw.rect(screen, (0, 0, 0), self.rect)

    def move(self, dt):
        self.dx = 0
        self.dy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.dx = -Neo.SPEED
        if keys[pg.K_d]:
            self.dx = Neo.SPEED
        if keys[pg.K_w]:
            self.dy = -Neo.SPEED
        if keys[pg.K_s]:
            self.dy = Neo.SPEED
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.rect.x = self.x
        self.rect.y = self.y
