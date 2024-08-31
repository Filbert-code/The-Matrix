import pygame as pg
from pygame import Rect

import colors
from constants import SCREEN_WIDTH, WORLD_HEIGHT, WORLD_WIDTH
from util.common import to_pygame_rect


class Neo:
    SPEED = 1000
    DEFAULT_X_BOUNDARIES = (0, WORLD_WIDTH)

    def __init__(self, level):
        self.level = level
        self.rect = Rect(SCREEN_WIDTH // 2, level.get_current_floor_y(), 10, 125)
        self.x = self.rect.x
        self.y = self.rect.y
        self.dx = 0
        self.dy = 0

        self.in_room = False
        self.room = None

        self.x_boundaries = self.DEFAULT_X_BOUNDARIES

    def update(self, dt):
        self.move(dt)

    def draw(self, screen):
        # draw Neo as a rectangle with the given rect
        pg.draw.rect(screen, colors.player, to_pygame_rect(self.rect, WORLD_HEIGHT))

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

        # enforce boundaries
        if self.rect.left < self.x_boundaries[0]:
            self.rect.left = self.x_boundaries[0]
            self.x = self.rect.x
        if self.rect.right > self.x_boundaries[1]:
            self.rect.right = self.x_boundaries[1]
            self.x = self.rect.x

    def enter_room(self, room):
        self.in_room = True
        self.room = room
        self.set_boundaries((room.room_rect.left, room.room_rect.right))

    def exit_room(self):
        self.in_room = False
        self.room = None
        self.set_boundaries(self.DEFAULT_X_BOUNDARIES)

    def set_boundaries(self, new_boundaries):
        self.x_boundaries = new_boundaries
