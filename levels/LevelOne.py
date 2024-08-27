import pygame as pg
from pygame import Rect

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from util.common import to_pygame_rect


class LevelOne:
    FLOOR_HEIGHT = 175
    STAIRWAY_WIDTH = 100
    STARTING_FLOOR = 1
    NUMBER_OF_FLOORS = 10
    WIDTH = SCREEN_WIDTH * 2
    HEIGHT = SCREEN_HEIGHT * 2

    def __init__(self):
        self.current_player_floor = self.STARTING_FLOOR
        # self.current_player_floor_y = (self.current_player_floor * (self.FLOOR_HEIGHT + 120))

        self.stairways_x_positions = [300, self.WIDTH - 300]
        # list of lists of stairway rects, each list contains all the stairways for a floor
        self.stairways_rects = []

        self.floors_rects = []
        for i in range(0, (self.FLOOR_HEIGHT + 100) * self.NUMBER_OF_FLOORS, self.FLOOR_HEIGHT + 100):
            self.floors_rects.append(Rect(50, i + 20, self.WIDTH - 100, self.FLOOR_HEIGHT))
            floor_stairways_rects = []
            for x in self.stairways_x_positions:
                floor_stairways_rects.append(Rect(x, i + 20, self.STAIRWAY_WIDTH, self.FLOOR_HEIGHT))
            self.stairways_rects.append(floor_stairways_rects)

    def update(self):
        pass

    def get_current_floor_stairways_rects(self):
        return self.stairways_rects[self.current_player_floor - 1]

    def floor_up(self):
        if self.current_player_floor < self.NUMBER_OF_FLOORS:
            self.current_player_floor += 1

    def floor_down(self):
        if self.current_player_floor > 1:
            self.current_player_floor -= 1

    def get_current_floor_y(self):
        return self.floors_rects[self.current_player_floor - 1].y

    def draw(self, screen):
        for floor_rect in self.floors_rects:
            pg.draw.rect(screen, (255, 255, 255), to_pygame_rect(floor_rect, self.HEIGHT))
        for stairways in self.stairways_rects:
            for stairway in stairways:
                pg.draw.rect(screen, (111, 111, 111), to_pygame_rect(stairway, self.HEIGHT))