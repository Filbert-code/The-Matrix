import time

import pygame as pg

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, WORLD_WIDTH, WORLD_HEIGHT
from util.common import to_pygame_rect


class PlayerFollowCamera:
    def __init__(self, screen, world_surface, player, starting_scale, min_max_scale):
        self._screen = screen
        self._world = world_surface
        self.min_scale, self.max_scale = min_max_scale
        # TODO: throw an error if this scale is not between the min and max
        self.scale = starting_scale

        self._world_width, self._world_height = self._world.get_width(), self._world.get_height()

        self.window_width = SCREEN_WIDTH / self.scale
        self.window_height = SCREEN_HEIGHT / self.scale
        self.left = player.rect.x - self.window_width / 2
        self.top = WORLD_HEIGHT - player.rect.y - self.window_height / 2

        self.camera_speed_x = 1500
        self.camera_speed_y = 500

        self.transition_start_time = time.time()
        self.timer_duration = 0
        self.timer = 0
        self.transition_speed = 0.5

    def update(self, neo, dt):
        # run a scale transition
        if time.time() - self.transition_start_time < self.timer_duration:
            self.scale += dt * self.transition_speed

        # update window width/height based on the scale
        self.window_width = SCREEN_WIDTH / self.scale
        self.window_height = SCREEN_HEIGHT / self.scale
        if self.window_width > self._world_width:
            self.window_width = self._world_width
        if self.window_height > self._world_height:
            self.window_height = self._world_height

        # update window position(left,top) to center on the player
        player_x, player_y = (neo.rect.x, neo.rect.y)
        # self.left = player_x - self.window_width / 2
        # self.top = WORLD_HEIGHT - player_y - self.window_height / 2
        if abs(self.left - (neo.rect.left - self.window_width / 2)) < 20:
            self.left = neo.rect.left - self.window_width / 2
        else:
            if self.left < neo.rect.left - self.window_width / 2:
                self.left += dt * self.camera_speed_x
            else:
                self.left -= dt * self.camera_speed_x
        if abs(self.top - (WORLD_HEIGHT - neo.rect.top - self.window_height / 2)) < 20:
            self.top = WORLD_HEIGHT - neo.rect.top - self.window_height / 2
        else:
            if self.top < WORLD_HEIGHT - neo.rect.top - self.window_height / 2:
                self.top += dt * self.camera_speed_y
            else:
                self.top -= dt * self.camera_speed_y

        # enforce boundaries logic
        if self.left < 0:
            self.left = 0
        elif self.left > self._world_width - self.window_width:
            self.left = self._world_width - self.window_width
        if self.top < 0:
            self.top = 0
        elif self.top > self._world_height - self.window_height:
            self.top = self._world_height - self.window_height

    def draw(self, screen):
        subsurface = self._world.subsurface(self.left, self.top, self.window_width, self.window_height)
        self._screen.blit(
            pg.transform.scale(subsurface, (SCREEN_WIDTH, SCREEN_HEIGHT)),
            (0, 0)
        )

    def zoom_in(self):
        # TODO: abstract out the zoom delta to let the user configure a zoom speed for the cam
        if self.scale > self.min_scale:
            self.scale *= 0.95

    def zoom_out(self):
        if self.scale < self.max_scale:
            self.scale *= 1.05

    def trigger_zoom_in_transition(self, zoom_in=True):
        self.transition_start_time = time.time()
        self.timer_duration = 2
        self.timer = 0
        self.transition_speed = 0.75 if zoom_in else -0.75

    def get_camera_rect(self):
        return pg.Rect(self.left, self.top, self.window_width, self.window_height)

    def convert_camera_to_world_coord(self, camera_coord):
        scaled_pos = (camera_coord[0] / self.scale, camera_coord[1] / self.scale)
        mouse_pos_pymunk_coord = (scaled_pos[0] + self.left, scaled_pos[1] + self.top)
        return mouse_pos_pymunk_coord