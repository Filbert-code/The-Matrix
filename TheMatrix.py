import math

import pygame as pg
from pygame.sprite import Group

import colors
from cameras.PlayerFollowCamera import PlayerFollowCamera
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH
from entities.Agent import Agent
from entities.Bullet import Bullet
from entities.Neo import Neo
from entity_groups.ExtendedGroup import ExtendedGroup
from enums.GameState import GameState
from pygame import Rect, Vector2

from hud.Hud import Hud
from levels.LevelOne import LevelOne
from util.common import to_pygame_rect, to_pygame_coords


class TheMatrix:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
        self.world = pg.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2), pg.SRCALPHA)
        self.level = LevelOne()
        self.neo = Neo(self.level)
        self.camera = PlayerFollowCamera(
            self.screen,
            self.world,
            self.neo,
            starting_scale=0.5,
            min_max_scale=(0.5, 6)
        )
        self.clock = pg.time.Clock()
        self.state = GameState.MAIN_MENU
        # delta time in seconds since last frame, used for frame rate-independent physics
        self.dt = 0
        self.running = True
        self.hud = Hud(self.neo, self.level)

        self.bullet_group = ExtendedGroup()
        self.points_to_draw = []

        self.agents_group = ExtendedGroup()
        for i in range(4):
            self.agents_group.add(
                Agent(self.level, 1, looking_right=True if i % 2 == 0 else False)
            )

        # self.agent_smith =

    def start_game_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000
            # print(self.clock.get_fps())
        pg.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            # mouse click events
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_buttons = pg.mouse.get_pressed()
                mouse_click_pos = pg.mouse.get_pos()
                camera_x, camera_y = self.camera.get_camera_rect().topleft
                if mouse_buttons[0]:
                    # print(f'Neo: {self.neo.rect.center}')
                    # print(f'Mouse: {mouse_click_pos}')
                    neo_x, neo_y = to_pygame_rect(self.neo.rect, WORLD_HEIGHT).center
                    # angle = math.atan2((mouse_click_pos[0] - neo_x), (mouse_click_pos[1] - neo_y))
                    # bullet = Bullet((neo_x, neo_y), (4000, 0))
                    mouse_pos_world_coord = self.camera.convert_camera_to_world_coord(mouse_click_pos)
                    neo_vec = Vector2(neo_x, neo_y)
                    mouse_vec = Vector2(mouse_pos_world_coord[0], mouse_pos_world_coord[1])
                    print(f'Neo_vec: {neo_vec}, Mouse_vec: {mouse_vec}')
                    normalized_delta_vec = (mouse_vec - neo_vec).normalize()

                    bullet = Bullet((self.neo.rect.centerx, self.neo.rect.centery), (3000 * (1 if normalized_delta_vec.x > 0 else -1), 0))
                    self.bullet_group.add(bullet)
            # mouse wheel events
            if event.type == pg.MOUSEWHEEL:
                if event.y == 1:
                    self.camera.zoom_out()
                elif event.y == -1:
                    self.camera.zoom_in()
            # keyboard events
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[pg.K_w]:  # goes up a floor or enters/exits room
                    floor_stairways_rects = self.level.get_current_floor_stairways_rects()
                    for stairway in floor_stairways_rects:
                        if self.neo.rect.colliderect(stairway):
                            self.level.floor_up()
                            break
                    rooms_rects = self.level.get_current_floor_rooms()
                    for room in rooms_rects:
                        if self.neo.rect.colliderect(room.door_rect):
                            self.neo.enter_room(room)
                            break
                if keys[pg.K_s]:  # goes down a floor or enters/exits room
                    floor_stairways_rects = self.level.get_current_floor_stairways_rects()
                    for stairway in floor_stairways_rects:
                        if self.neo.rect.colliderect(stairway):
                            self.level.floor_down()
                            break
                    rooms_rects = self.level.get_current_floor_rooms()
                    for room in rooms_rects:
                        if self.neo.rect.colliderect(room.door_rect):
                            self.neo.exit_room()
                            break
                if keys[pg.K_e]:
                    self.camera.trigger_zoom_in_transition()
                if keys[pg.K_q]:
                    self.camera.trigger_zoom_in_transition(False)

    def update(self):
        self.neo.update(self.dt)
        self.bullet_group.update(self.dt)
        self.agents_group.update(self.dt)

        # check player bullets and agent collisions:
        pg.sprite.groupcollide(self.bullet_group, self.agents_group, True, True)

        self.camera.update(self.neo, self.dt)

    def draw(self):
        self.world.set_clip(self.camera.get_camera_rect())
        # draw background
        self.world.fill(colors.background)
        # draw onto the world Surface
        self.world.lock()  # optimization: locking a Surface during sequential draw calls to that surface
        self.level.draw(self.world, self.neo)
        self.neo.draw(self.world)
        self.bullet_group.draw(self.world)
        self.agents_group.draw(self.world)
        for agent in self.agents_group:
            pg.draw.line(self.world, colors.agent_searching, to_pygame_rect(agent.rect, WORLD_HEIGHT).center, (agent.vision_vector.x, WORLD_HEIGHT - agent.vision_vector.y), 2)
        self.world.unlock()
        # # draw a 10 x 10 grid
        # grid_row_num = 10
        # grid_col_num = 10
        # row_height = int(WORLD_HEIGHT / grid_row_num)
        # col_width = row_height
        # for y in range(0, WORLD_HEIGHT, row_height):
        #     pg.draw.line(self.world, colors.grid, (0, y), (WORLD_WIDTH, y), 1)
        #     for x in range(0, WORLD_WIDTH, col_width):
        #         pg.draw.line(self.world, colors.grid, (x, 0), (x, WORLD_HEIGHT), 1)

        self.camera.draw()
        self.hud.draw(self.screen)
        self.world.set_clip(None)
        # draw the buffer to the screen
        pg.display.flip()
