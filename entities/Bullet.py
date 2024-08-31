import pygame as pg

import colors
from constants import WORLD_HEIGHT, WORLD_WIDTH
from util.common import to_pygame_rect


class Bullet(pg.sprite.Sprite):
    WIDTH, HEIGHT = 40, 10

    def __init__(self, pos, velocity):
        pg.sprite.Sprite.__init__(self)

        self.x, self.y = pos
        self.dx, self.dy = velocity

        self.image = pg.Surface([self.WIDTH, self.HEIGHT], pg.SRCALPHA)
        self.image.fill(colors.player)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, dt):
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

        # delete bullet when passed map boundaries
        if not 0 < self.rect.centerx < WORLD_WIDTH or not 0 < self.rect.centery < WORLD_HEIGHT:
            self.kill()

    def draw(self, screen):
        pg.draw.rect(screen, colors.player, to_pygame_rect(self.rect, WORLD_HEIGHT))
