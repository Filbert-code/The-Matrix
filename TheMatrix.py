import pygame as pg

from cameras.PlayerFollowCamera import PlayerFollowCamera
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from entities.Neo import Neo
from enums.GameState import GameState
from pygame import Rect

from levels.LevelOne import LevelOne
from util.common import to_pygame_rect


class TheMatrix:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.world = pg.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2))
        self.level = LevelOne()
        self.neo = Neo(self.level)
        self.camera = PlayerFollowCamera(
            self.screen,
            self.world,
            self.neo,
            starting_scale=1.1,
            min_max_scale=(0.5, 6)
        )
        self.clock = pg.time.Clock()
        self.state = GameState.MAIN_MENU
        # delta time in seconds since last frame, used for frame rate-independent physics
        self.dt = 0
        self.running = True

    def start_game_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000
        pg.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            # mouse wheel events
            if event.type == pg.MOUSEWHEEL:
                if event.y == 1:
                    self.camera.zoom_out()
                elif event.y == -1:
                    self.camera.zoom_in()
            # keyboard events
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[pg.K_w]:  # goes up a floor
                    floor_stairways_rects = self.level.get_current_floor_stairways_rects()
                    for stairway in floor_stairways_rects:
                        if self.neo.rect.colliderect(stairway):
                            self.level.floor_up()
                            break
                if keys[pg.K_s]:  # goes down a floor
                    floor_stairways_rects = self.level.get_current_floor_stairways_rects()
                    for stairway in floor_stairways_rects:
                        if self.neo.rect.colliderect(stairway):
                            self.level.floor_down()
                            break
                if keys[pg.K_e]:
                    self.camera.trigger_zoom_in_transition()
                if keys[pg.K_q]:
                    self.camera.trigger_zoom_in_transition(False)

    def update(self):
        self.neo.update(self.dt)
        self.camera.update(self.neo, self.dt)

    def draw(self):
        self.world.set_clip(self.camera.get_camera_rect())
        # draw background
        self.world.fill("purple")
        # insert drawing code here
        self.level.draw(self.world)
        self.neo.draw(self.world)

        self.camera.draw(self.world)
        self.world.set_clip(None)

        # draw the buffer to the screen
        pg.display.flip()
