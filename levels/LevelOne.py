import pygame as pg
from pygame import Rect

import colors
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH, FONTS_DIRECTORY
from data_structures.UnexploredFloorAreasSortedList import UnexploredFloorAreasSortedList
from data_structures.UnexploredRoomAreasSortedList import UnexploredRoomAreasSortedList
from levels.Room import Room
from util.common import to_pygame_rect, to_pygame_coords
import pygame.freetype


class LevelOne:
    FLOOR_HEIGHT = 175
    STAIRWAY_WIDTH = 100
    DOOR_WIDTH = 85
    STARTING_FLOOR = 6
    NUMBER_OF_FLOORS = 8
    WIDTH = SCREEN_WIDTH * 2
    HEIGHT = SCREEN_HEIGHT * 2
    BUILDING_HORIZONTAL_PADDING = 50
    pg.freetype.init()
    DOOR_NUMBER_FONT = pg.freetype.SysFont('Helvetica', 40)

    def __init__(self):
        self.current_player_floor = self.STARTING_FLOOR
        # self.current_player_floor_y = (self.current_player_floor * (self.FLOOR_HEIGHT + 120))

        self.stairways_x_positions = [300, self.WIDTH - 300]
        # list of lists of stairway rects, each list contains all the stairways for a floor
        self.stairways_rects = []
        # list of lists of floor rooms, each list contains all the rooms for a floor
        self.floors_rooms = []

        self.floors_rects = []
        for i, floor_y in enumerate(range(0, (self.FLOOR_HEIGHT + 100) * self.NUMBER_OF_FLOORS, self.FLOOR_HEIGHT + 100)):
            self.floors_rects.append(Rect(50, floor_y + 20, self.WIDTH - 100, self.FLOOR_HEIGHT))
            floor_stairways_rects = []
            for x in self.stairways_x_positions:
                floor_stairways_rects.append(Rect(x, floor_y + 20, self.STAIRWAY_WIDTH, self.FLOOR_HEIGHT))
            self.stairways_rects.append(floor_stairways_rects)
            floor_rooms = []
            for k, room_door_x in enumerate(range(self.BUILDING_HORIZONTAL_PADDING + self.STAIRWAY_WIDTH + 500, WORLD_WIDTH - self.BUILDING_HORIZONTAL_PADDING - self.STAIRWAY_WIDTH - 500, 1000)):
                room_door_rect = Rect(room_door_x, floor_y + 20, self.DOOR_WIDTH, self.FLOOR_HEIGHT - 25)
                room_rect = Rect(room_door_x - 50, floor_y + 20, 800, self.FLOOR_HEIGHT)
                floor_rooms.append(
                    Room(door_rect=room_door_rect, room_rect=room_rect, room_number=int(f'{i + 1}0{k + 1}'))
                )
            self.floors_rooms.append(floor_rooms)

        # this data structure gets updated from the Agent update function
        self.unexplored_floors_areas = [UnexploredFloorAreasSortedList(self.WIDTH, None, self.BUILDING_HORIZONTAL_PADDING) for _ in range(self.NUMBER_OF_FLOORS)]
        self.unexplored_rooms_areas = []
        for floor_rooms_list in self.floors_rooms:
            unexplored_rooms_for_floor = [UnexploredRoomAreasSortedList(room.room_rect, None) for room in floor_rooms_list]
            self.unexplored_rooms_areas.append(unexplored_rooms_for_floor)

    def update(self, agents):
        # TODO: update this appropriately
        # for agent in agents:
        #     # TODO: Update this to cumulatively sum up the floor explored area
        #     self.unexplored_floors[agent.current_floor - 1] = agent.current_floor_explored_start_end_x
        pass

    def get_current_floor_stairways_rects(self):
        return self.stairways_rects[self.current_player_floor - 1]

    def get_current_floor_rooms(self):
        return self.floors_rooms[self.current_player_floor - 1]

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

    def draw(self, screen, neo):
        for floor_rect in self.floors_rects:
            pg.draw.rect(screen, colors.building, to_pygame_rect(floor_rect, self.HEIGHT))
        # draw room areas unexplored by agents
        for floor_index, unexplored_rooms_in_floor in enumerate(self.unexplored_rooms_areas):
            for unexplored_room_area_sorted_list in unexplored_rooms_in_floor:
                for unexplored_room_area in unexplored_room_area_sorted_list.sorted_list:
                    x1, x2 = unexplored_room_area.x1, unexplored_room_area.x2
                    pg.draw.rect(
                        screen,
                        colors.unexplored_room_regions,
                        to_pygame_rect(Rect(x1, self.floors_rects[floor_index].y, abs(x2 - x1), self.FLOOR_HEIGHT),
                                       WORLD_HEIGHT)
                    )
        # draw floor areas unexplored by agents
        for floor_index, unexplored_floor_area_sorted_list in enumerate(self.unexplored_floors_areas):
            for unexplored_floor_area in unexplored_floor_area_sorted_list.sorted_list:
                x1, x2 = unexplored_floor_area.x1, unexplored_floor_area.x2
                pg.draw.rect(
                    screen,
                    colors.unexplored_floor_regions,
                    to_pygame_rect(Rect(x1, self.floors_rects[floor_index].y, abs(x2 - x1), self.FLOOR_HEIGHT),
                                   WORLD_HEIGHT)
                )
        for stairways in self.stairways_rects:
            for stairway in stairways:
                pg.draw.rect(screen, colors.stairways, to_pygame_rect(stairway, self.HEIGHT))
        for rooms in self.floors_rooms:
            for room in rooms:
                # draw the room
                if neo.in_room and neo.room == room:
                    pg.draw.rect(screen, colors.room_interior, to_pygame_rect(room.room_rect, self.HEIGHT))
                # draw the door
                shadow_rect = Rect(room.door_rect.left, room.door_rect.top - 1, room.door_rect.width + 4, room.door_rect.height)
                pg.draw.rect(screen, colors.doors_shadow, to_pygame_rect(shadow_rect, self.HEIGHT))
                pg.draw.rect(screen, colors.doors, to_pygame_rect(room.door_rect, self.HEIGHT))
                pg.draw.circle(screen, 'black', to_pygame_coords((room.door_rect.right - self.DOOR_WIDTH / 6, room.door_rect.centery), WORLD_HEIGHT), 4)
                door_number_pos = to_pygame_rect(room.door_rect, self.HEIGHT).midtop
                self.DOOR_NUMBER_FONT.render_to(screen, (door_number_pos[0] - self.DOOR_NUMBER_FONT.get_rect('101').width / 2, door_number_pos[1] + 20), str(room.room_number), (255, 255, 255))

