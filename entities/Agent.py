import random
from enum import Enum
from typing import List

import pygame as pg
from pygame import Rect, Vector2

import colors
from constants import SCREEN_WIDTH, WORLD_HEIGHT, WORLD_WIDTH
from data_structures.UnexploredAreasSortedList import UnexploredAreasSortedList, UnexploredArea
from entities.BasicPistol import BasicPistol
from entities.Bullet import Bullet
from enums.AgentStates import AgentStates
from enums.RoomClearingStates import RoomClearingStates
from levels.LevelOne import LevelOne
from levels.Room import Room
from util.common import is_segments_overlapping, to_pygame_rect


class Agent(pg.sprite.Sprite):
    SPEED = 400
    VIEW_DISTANCE = 500
    DEFAULT_X_BOUNDARIES = (0, WORLD_WIDTH)
    CLOSEST_STAIRWAY_DEFAULT_VALUE = [float('inf'), None]
    STARTING_HEALTH = 100
    HEALTH_BAR_WIDTH = 80
    DEFAULT_ROOM_CLEARING_STATE = RoomClearingStates.MOVING_TO_ROOM
    STATUS_FONT = pg.freetype.SysFont('Helvetica', 25)

    def __init__(self, level, agent_bullet_group, starting_floor, looking_right=True):
        pg.sprite.Sprite.__init__(self)
        self.level: LevelOne = level
        self.agent_bullet_group = agent_bullet_group
        self.starting_floor = starting_floor
        self.current_floor = starting_floor

        # initialize Agent rect, image, and velocity
        self.image = pg.Surface((10, 125))
        self.image.fill(colors.agent_searching)
        self.rect = self.image.get_rect()
        self.rect.x = WORLD_WIDTH / 2 + random.randint(-1500, 1500)
        self.rect.y = self.level.get_y_for_floor(starting_floor)

        self.x = self.rect.x
        self.y = self.rect.y
        self.dx = self.SPEED if looking_right else -self.SPEED
        self.dy = 0
        self.x_boundaries = self.DEFAULT_X_BOUNDARIES

        # initialize states for floor clearing
        self.state = AgentStates.FLOOR_CLEARING
        self.vision_vector = Vector2(self.rect.centerx + (self.VIEW_DISTANCE if looking_right else -self.VIEW_DISTANCE),
                                     self.rect.centery)

        # initialize states for changing floors
        self.closest_stairway = self.CLOSEST_STAIRWAY_DEFAULT_VALUE
        self.health = self.STARTING_HEALTH

        # initialize states for room clearing
        self.room_clearing_state = self.DEFAULT_ROOM_CLEARING_STATE
        self.in_room = False
        self.room = None
        self.current_room_unexplored_areas: UnexploredAreasSortedList | None = None

        self.weapon = BasicPistol(agent_bullet_group)

    def update(self, dt):
        if self.state == AgentStates.DONE:
            self.dx = 0
            return

        # There is a hierarchy of states the Agent can be in
        # 1. AgentStates: general states that encompass all major actions the Agent can do
        # 2. RoomClearingStates: states specific for when the Agent is in AgentStates.ROOM_CLEARING mode
        #
        # The logic below should form a closed loop, where each state leads towards transitioning into another state,
        # ultimately trying to find Neo and hunt him down

        # ---- FLOOR CLEARING ----
        elif self.state == AgentStates.FLOOR_CLEARING:
            current_floor_unexplored_areas: UnexploredAreasSortedList = self.level.unexplored_floors_areas[
                self.current_floor - 1]
            self.move_agent_towards_closest_unexplored_floor_area(current_floor_unexplored_areas)
            current_floor_unexplored_areas.update_unexplored_area(self)

        # ---- ROOM CLEARING ----
        elif self.state == AgentStates.ROOM_CLEARING:
            if self.room_clearing_state == RoomClearingStates.MOVING_TO_ROOM:
                floor_rooms = self.level.floors_rooms[self.current_floor - 1]
                self.move_agent_towards_closest_room(floor_rooms)
            elif self.room_clearing_state == RoomClearingStates.CLEARING_ROOM:
                self.move_agent_towards_closest_unexplored_room_area(self.current_room_unexplored_areas)
                self.current_room_unexplored_areas.update_unexplored_area(self)
            elif self.room_clearing_state == RoomClearingStates.LEAVING_ROOM:
                self.move_agent_towards_current_room_door()

        # ---- CHANGING FLOORS ----
        elif self.state == AgentStates.CHANGING_FLOORS:
            stairway_rects_current_floor = self.level.stairways_rects[self.current_floor - 1]
            self.handle_move_up_floor_if_in_stairway(stairway_rects_current_floor)
            self.move_towards_closest_stairway(stairway_rects_current_floor)

        elif self.state == AgentStates.HUNTING_NEO:
            # if self.is_neo_in_vision():
            #     self.report_neo_position()
            # if self.is_neo_in_range():
            #     self.fire()
            self.move_towards_last_neo_position()

        # print(current_floor_unexplored_areas.sorted_list)
        self.move(dt)

    # def move_towards_last_neo_position(self):
    #     if self.target_floor != self.current_floor:
    #         self.

    def handle_move_up_floor_if_in_stairway(self, stairway_rects_current_floor):
        # if overlapping with a stairway, stop movement, and move to the target floor
        for stairway_rect in stairway_rects_current_floor:
            if is_segments_overlapping((stairway_rect.x, stairway_rect.x + stairway_rect.width),
                                       (self.x, self.x + 10)):
                if not self.current_floor + 1 > self.level.NUMBER_OF_FLOORS:
                    self.current_floor += 1
                else:
                    self.state = AgentStates.DONE
                    break
                self.state = AgentStates.FLOOR_CLEARING
                self.closest_stairway = self.CLOSEST_STAIRWAY_DEFAULT_VALUE
                break

    def move_towards_closest_stairway(self, stairway_rects_current_floor):
        # find the closest stairway
        for stairway_rect in stairway_rects_current_floor:
            stairway_distance = min(abs(self.x - stairway_rect.x),
                                    abs(self.x - stairway_rect.x + stairway_rect.width))
            if stairway_distance < self.closest_stairway[0]:
                self.closest_stairway = [stairway_distance, stairway_rect]
        # move towards it
        self.move_agent_towards_x_pos(self.closest_stairway[1].x)

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

        # enforce boundaries
        if self.rect.left < self.x_boundaries[0]:
            self.rect.left = self.x_boundaries[0]
            self.x = self.rect.x
        if self.rect.right > self.x_boundaries[1]:
            self.rect.right = self.x_boundaries[1]
            self.x = self.rect.x

    def move_agent_towards_closest_unexplored_floor_area(self, current_unexplored_areas):
        # LOGIC FOR MOVING PLAYER IN THE CORRECT DIRECTION
        # find the closest unexplored area, use this value to determine our vision vector
        closest_area = current_unexplored_areas.find_closest_unexplored_area(self.rect.centerx)
        if closest_area is None:
            # ** SWITCHING TO ROOM_CLEARING STATE HERE **
            self.state = AgentStates.ROOM_CLEARING
        else:
            self.move_agent_towards_x_pos(closest_area.x1)

    def move_agent_towards_closest_room(self, floor_rooms: List[Room]):
        # find the closest floor room
        closest_room = (float('inf'), None, -1)  # distance, room, index
        for i, room in enumerate(floor_rooms):
            if room.fully_explored or (type(room.assigned_agent) == Agent and room.assigned_agent != self):
                continue
            distance_to_room = abs(self.rect.centerx - room.door_rect.centerx)
            if distance_to_room < closest_room[0]:
                closest_room = (distance_to_room, room, i)
        if closest_room[1] is None:
            # ** SWITCHING TO CHANGING_FLOORS STATE HERE **
            self.state = AgentStates.CHANGING_FLOORS
            return
        closest_room[1].assigned_agent = self
        # check if agent is in front of a door, if so, enter the room
        if is_segments_overlapping(
                (self.rect.x, self.rect.x + self.rect.width),
                (closest_room[1].door_rect.x, closest_room[1].door_rect.x + closest_room[1].door_rect.width)
        ):
            self.enter_room(room=closest_room[1], room_index=closest_room[2])

        self.move_agent_towards_x_pos(closest_room[1].door_rect.centerx)

    def move_agent_towards_closest_unexplored_room_area(self, current_unexplored_areas):
        # LOGIC FOR MOVING PLAYER IN THE CORRECT DIRECTION
        # find the closest unexplored area, use this value to determine our vision vector
        closest_area = current_unexplored_areas.find_closest_unexplored_area(self.rect.centerx)
        if closest_area is None:
            # ** SWITCHING TO ROOM_CLEARING STATE HERE **
            self.room_clearing_state = RoomClearingStates.LEAVING_ROOM
            self.room.fully_explored = True
        else:
            self.move_agent_towards_x_pos(closest_area.x1)

    def move_agent_towards_current_room_door(self):
        if is_segments_overlapping((self.rect.x, self.rect.x + self.rect.width), (self.room.door_rect.x, self.room.door_rect.x + self.room.door_rect.width)):
            self.exit_room()
        else:
            self.move_agent_towards_x_pos(self.room.door_rect.centerx)

    def move_agent_towards_x_pos(self, x):
        if self.rect.centerx > x:
            # move left
            self.dx = -self.SPEED
            self.vision_vector = Vector2(self.rect.centerx - self.VIEW_DISTANCE, self.rect.centery)
        elif self.rect.centerx < x:
            # move right
            self.dx = self.SPEED
            self.vision_vector = Vector2(self.rect.centerx + self.VIEW_DISTANCE, self.rect.centery)

    def enter_room(self, room, room_index):
        self.in_room = True
        self.room = room
        self.set_boundaries((self.room.room_rect.left, self.room.room_rect.right))
        self.room_clearing_state = RoomClearingStates.CLEARING_ROOM
        self.current_room_unexplored_areas = self.level.unexplored_rooms_areas[self.current_floor - 1][room_index]

    def exit_room(self):
        self.room_clearing_state = self.DEFAULT_ROOM_CLEARING_STATE
        self.in_room = False
        self.room = None
        self.current_room_unexplored_areas: UnexploredAreasSortedList | None = None
        self.set_boundaries(self.DEFAULT_X_BOUNDARIES)

    def draw(self, screen):
        pg.draw.rect(screen, colors.agent_searching, to_pygame_rect(self.rect, WORLD_HEIGHT))
        # draw health bar
        health_bar_width = self.HEALTH_BAR_WIDTH * (self.health / self.STARTING_HEALTH)
        health_bar_rect = Rect(self.rect.x - health_bar_width / 2, self.rect.bottom + 10,
                               health_bar_width + self.rect.width, 5)
        pg.draw.rect(screen, colors.agent_hunting, to_pygame_rect(health_bar_rect, WORLD_HEIGHT))
        if self.weapon.reloading:
            self.STATUS_FONT.render_to(
                screen,
                (self.rect.x - self.STATUS_FONT.get_rect('Reloading').width / 2, self.rect.y + 20),
                'Reloading',
                (255, 255, 255)
            )

    def fire(self, right=True):
        bullet = Bullet((self.rect.centerx, self.rect.centery), (3000 * (1 if right else -1), 0))
        self.weapon.fire()
        self.agent_bullet_group.add(bullet)


    def set_boundaries(self, new_boundaries):
        self.x_boundaries = new_boundaries

    def handle_damage_taken(self, damage):
        self.health -= damage
        if self.health < 0:
            self.kill()
