import pygame as pg

from cameras.PlayerFixedCamera import PlayerFixedCamera
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from entities.Neo import Neo
from enums.GameState import GameState
from pygame import Rect

from levels.LevelOne import LevelOne


class TheMatrix:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.world = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 2))
        self.camera = PlayerFixedCamera(
            self.screen,
            self.world,
            starting_scale=1.1,
            min_max_scale=(1, 6)
        )
        self.clock = pg.time.Clock()
        self.state = GameState.MAIN_MENU
        # delta time in seconds since last frame, used for frame rate-independent physics
        self.dt = 0
        self.running = True

        self.neo = Neo(Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 100))
        self.level = LevelOne()

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
            if event.type == pg.MOUSEWHEEL:
                if event.y == 1:
                    self.camera.zoom_out()
                elif event.y == -1:
                    self.camera.zoom_in()

    def update(self):
        self.neo.update(self.dt)
        self.camera.update((self.neo.x, self.neo.y))

    def draw(self):
        self.world.set_clip(self.camera.get_camera_rect())
        # draw background
        self.world.fill("purple")
        # insert drawing code here
        self.level.draw(self.world)
        self.neo.draw(self.world)

        self.camera.draw()
        self.world.set_clip(None)

        # draw the buffer to the screen
        pg.display.flip()
