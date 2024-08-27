import pygame as pg
from pygame import Rect

from constants import SCREEN_WIDTH
from util.common import to_pygame_rect


class Neo:
    SPEED = 1000

    def __init__(self, level):
        self.level = level
        self.rect = Rect(SCREEN_WIDTH // 2, level.get_current_floor_y(), 10, 100)
        self.x = self.rect.x
        self.y = self.rect.y
        self.dx = 0
        self.dy = 0

    def update(self, dt):
        self.move(dt)

    def draw(self, screen):
        # draw Neo as a rectangle with the given rect
        pg.draw.rect(screen, (0, 0, 0), to_pygame_rect(self.rect, self.level.HEIGHT))

    def move(self, dt):
        self.dx = 0
        self.dy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.dx = -Neo.SPEED
        if keys[pg.K_d]:
            self.dx = Neo.SPEED
        # if keys[pg.K_w]:
        #     self.dy = -Neo.SPEED
        # if keys[pg.K_s]:
        #     self.dy = Neo.SPEED
        self.x += self.dx * dt
        self.rect.x = self.x
        self.y = self.level.get_current_floor_y()
        self.rect.y = self.y
