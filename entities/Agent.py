import random
from enum import Enum

import pygame as pg
from pygame import Rect, Vector2

import colors
from constants import SCREEN_WIDTH, WORLD_HEIGHT, WORLD_WIDTH
from data_structures.UnexploredFloorAreasSortedList import UnexploredFloorAreasSortedList, UnexploredFloorArea
from enums.AgentStates import AgentStates
from levels.LevelOne import LevelOne
from util.common import is_segments_overlapping


class Agent(pg.sprite.Sprite):
    SPEED = 600
    VIEW_DISTANCE = 150
    CLOSEST_STAIRWAY_DEFAULT_VALUE = [float('inf'), None]

    def __init__(self, level, starting_floor, looking_right=True):
        pg.sprite.Sprite.__init__(self)
        self.level: LevelOne = level
        self.starting_floor = starting_floor
        self.current_floor = starting_floor

        # initialize Agent rect, image, and velocity
        self.rect = Rect(WORLD_WIDTH / 2 + random.randint(-1500, 1500), self.level.get_y_for_floor(starting_floor), 10, 125)
        self.image = pg.Surface((10, 125))
        self.image.fill(colors.agent_searching)

        self.x = self.rect.x
        self.y = self.rect.y
        self.dx = self.SPEED if looking_right else -self.SPEED
        self.dy = 0

        # initialize states for floor clearing
        self.state = AgentStates.FLOOR_CLEARING
        self.vision_vector = Vector2(self.rect.centerx + (self.VIEW_DISTANCE if looking_right else -self.VIEW_DISTANCE), self.rect.centery)

        # initialize states for changing floors
        self.closest_stairway = self.CLOSEST_STAIRWAY_DEFAULT_VALUE

    def update(self, dt):
        if self.state == AgentStates.DONE:
            self.dx = 0
            return
        elif self.state == AgentStates.FLOOR_CLEARING:
            current_floor_unexplored_areas: UnexploredFloorAreasSortedList = self.level.unexplored_floors[
                self.current_floor - 1]
            self.move_agent_towards_closest_rect(current_floor_unexplored_areas)
            self.update_floor_unexplored_area(current_floor_unexplored_areas)

        elif self.state == AgentStates.CHANGING_FLOORS:
            stairway_rects_current_floor = self.level.stairways_rects[self.current_floor - 1]
            # if overlapping with a stairway, stop movement, and move to the target floor
            for stairway_rect in stairway_rects_current_floor:
                if is_segments_overlapping((stairway_rect.x, stairway_rect.x + stairway_rect.width), (self.x, self.x + 10)):
                    if not self.current_floor + 1 > self.level.NUMBER_OF_FLOORS:
                        self.current_floor += 1
                    else:
                        self.state = AgentStates.DONE
                        break
                    self.state = AgentStates.FLOOR_CLEARING
                    self.closest_stairway = self.CLOSEST_STAIRWAY_DEFAULT_VALUE
                    break
            # find the closest stairway
            for stairway_rect in stairway_rects_current_floor:
                stairway_distance = min(abs(self.x - stairway_rect.x), abs(self.x - stairway_rect.x + stairway_rect.width))
                if stairway_distance < self.closest_stairway[0]:
                    self.closest_stairway = [stairway_distance, stairway_rect]
            # move towards it
            self.dx = self.SPEED if self.x - self.closest_stairway[1].x < 0 else -self.SPEED
            self.vision_vector = Vector2(self.rect.centerx + (self.VIEW_DISTANCE if self.x - self.closest_stairway[1].x < 0 else -self.VIEW_DISTANCE), self.rect.centery)

        # print(current_floor_unexplored_areas.sorted_list)
        self.move(dt)

    def move(self, dt):
        # eventual decision process:
        # 1. check floor for Neo
        # 2. go to the nearest stairs
        # 3. go to next floor
        # 4. check floor for Neo
        # ** Agents on the same floor share floor discovery info **
        # ** Once an Agent sees Neo, he pauses for a second or two to radio in Neo's position. Once that happens,
        # all Agents know Neo's position and go into HUNT mode **

        self.x += self.dx * dt
        self.rect.x = self.x
        self.y = self.level.get_y_for_floor(self.current_floor)
        self.rect.y = self.y

    def move_agent_towards_closest_rect(self, current_floor_unexplored_areas):
        # LOGIC FOR MOVING PLAYER IN THE CORRECT DIRECTION
        # find the closest unexplored area, use this value to determine our vision vector
        closest_area = current_floor_unexplored_areas.find_closest_unexplored_floor_area(self.rect.centerx)
        if closest_area is None:
            # ** SWITCHING TO CHANGING_FLOORS STATE HERE **
            self.state = AgentStates.CHANGING_FLOORS
        elif self.rect.centerx > closest_area.x1:
            # move left
            self.dx = -self.SPEED
            self.vision_vector = Vector2(self.rect.centerx - self.VIEW_DISTANCE, self.rect.centery)
        elif self.rect.centerx < closest_area.x1:
            # move right
            self.dx = self.SPEED
            self.vision_vector = Vector2(self.rect.centerx + self.VIEW_DISTANCE, self.rect.centery)

    def update_floor_unexplored_area(self, current_floor_unexplored_areas):
        # LOGIC FOR UPDATING THE LEVEL'S SORTED UNEXPLORED AREA DATA STRUCTURE FOR THE CURRENT FLOOR
        # Check if vision vector overlaps with any unexplored floor areas
        # If it does, update the overlapped area to reduce its range
        for unexplored_area in current_floor_unexplored_areas.sorted_list:
            agent_x1, agent_x2 = min(self.rect.centerx, int(self.vision_vector[0])), max(self.rect.centerx,
                                                                                         int(self.vision_vector[0]))

            if agent_x1 <= unexplored_area.x1 <= agent_x2 and agent_x1 <= unexplored_area.x2 <= agent_x2:
                # area is within the vision area
                current_floor_unexplored_areas.sorted_list.remove(unexplored_area)

            # if agent does not overlap with unexplored area, skip
            if not is_segments_overlapping((unexplored_area.x1, unexplored_area.x2), (agent_x1, agent_x2)):
                continue

            if agent_x1 >= unexplored_area.x1 and agent_x2 <= unexplored_area.x2:
                # the agent has unexplored area forwards and backwards. Need to split the unexplored area into 2
                new_unexplored_area = UnexploredFloorArea(agent_x2, unexplored_area.x2)
                current_floor_unexplored_areas.sorted_list.add(new_unexplored_area)
                unexplored_area.x2 = agent_x1
                # break here because we know our vision is completely within this unexplored area and none others
                break

            if agent_x1 >= unexplored_area.x1 and agent_x2 >= unexplored_area.x2:
                unexplored_area.x2 = agent_x1
                if abs(unexplored_area.x2 - unexplored_area.x1) < 5:
                    try:
                        current_floor_unexplored_areas.sorted_list.remove(unexplored_area)
                    except ValueError as e:
                        print(e)
            elif agent_x1 <= unexplored_area.x1 and agent_x2 <= unexplored_area.x2:
                unexplored_area.x1 = agent_x2
                if abs(unexplored_area.x2 - unexplored_area.x1) < 5:
                    try:
                        current_floor_unexplored_areas.sorted_list.remove(unexplored_area)
                    except ValueError as e:
                        print(e)

    def go_to_next_floor(self):
        pass
