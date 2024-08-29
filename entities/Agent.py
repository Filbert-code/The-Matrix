import pygame as pg
from pygame import Rect

import colors
from constants import SCREEN_WIDTH, WORLD_HEIGHT
from util.common import to_pygame_rect


class Agent(pg.sprite.Sprite):
    SPEED = 1000

    def __init__(self, level, pos):
        pg.sprite.Sprite.__init__(self)
        self.level = level
        self.rect = Rect(pos[0], pos[1], 10, 125)
        self.image = pg.Surface((10, 125))
        self.image.fill(colors.agent)
        self.x = self.rect.x
        self.y = self.rect.y
        self.dx = 100
        self.dy = 0

    def update(self, dt):
        self.move(dt)

    def move(self, dt):
        self.x += self.dx * dt
        self.rect.x = self.x
        # self.y = self.level.get_current_floor_y()
        self.rect.y = self.y

    # def draw(self, screen):
    #     # draw Neo as a rectangle with the given rect
    #     pg.draw.rect(screen, colors.player, to_pygame_rect(self.rect, WORLD_HEIGHT))