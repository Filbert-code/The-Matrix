import pygame as pg
from pygame import Rect

import colors
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_HEIGHT
from data_structures.UnexploredFloorAreasSortedList import UnexploredFloorAreasSortedList
from util.common import to_pygame_rect


class LevelOne:
    FLOOR_HEIGHT = 175
    STAIRWAY_WIDTH = 100
    STARTING_FLOOR = 6
    NUMBER_OF_FLOORS = 8
    WIDTH = SCREEN_WIDTH * 2
    HEIGHT = SCREEN_HEIGHT * 2
    BUILDING_HORIZONTAL_PADDING = 50

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

        # this data structure gets updated from the Agent update function
        self.unexplored_floors = [UnexploredFloorAreasSortedList(self.WIDTH, None, self.BUILDING_HORIZONTAL_PADDING) for _ in range(self.NUMBER_OF_FLOORS)]

    def update(self, agents):
        # TODO: update this appropriately
        # for agent in agents:
        #     # TODO: Update this to cumulatively sum up the floor explored area
        #     self.unexplored_floors[agent.current_floor - 1] = agent.current_floor_explored_start_end_x
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

    def get_y_for_floor(self, floor_num):
        return self.floors_rects[floor_num - 1].y

    def draw(self, screen):
        for floor_rect in self.floors_rects:
            pg.draw.rect(screen, colors.building, to_pygame_rect(floor_rect, self.HEIGHT))
        # draw area explored by agents
        for floor_index, unexplored_floor_area_sorted_list in enumerate(self.unexplored_floors):
            for unexplored_floor_area in unexplored_floor_area_sorted_list.sorted_list:
                x1, x2 = unexplored_floor_area.x1, unexplored_floor_area.x2
                pg.draw.rect(
                    screen,
                    colors.unexplored_regions,
                    to_pygame_rect(Rect(x1, self.floors_rects[floor_index].y, abs(x2 - x1), self.FLOOR_HEIGHT),
                                   WORLD_HEIGHT)
                )
        for stairways in self.stairways_rects:
            for stairway in stairways:
                pg.draw.rect(screen, colors.stairways, to_pygame_rect(stairway, self.HEIGHT))


