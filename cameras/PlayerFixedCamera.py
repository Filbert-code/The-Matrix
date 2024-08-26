import pygame as pg

from constants import SCREEN_HEIGHT


class PlayerFixedCamera:
    def __init__(self, screen, world_surface, starting_scale, min_max_scale):
        self._screen = screen
        self._world = world_surface
        self.min_scale, self.max_scale = min_max_scale
        # TODO: throw an error if this scale is not between the min and max
        self.scale = starting_scale

        self._world_width, self._world_height = self._world.get_width(), self._world.get_height()

        self.window_width = None
        self.window_height = None
        self.left = None
        self.top = None

    def update(self, player_pos):
        # update window width/height based on the scale
        self.window_width = self._world_width / self.scale
        self.window_height = SCREEN_HEIGHT / self.scale
        if self.window_width > self._world_width:
            self.window_width = self._world_width
        if self.window_height > self._world_height:
            self.window_height = self._world_height

        # update window position(left,top) to center on the player
        player_x, player_y = player_pos
        self.left = player_x - self.window_width / 2
        self.top = player_y - self.window_height / 2
        if self.left < 0:
            self.left = 0
        elif self.left > self._world_width - self.window_width:
            self.left = self._world_width - self.window_width
        if self.top < 0:
            self.top = 0
        elif self.top > self._world_height - self.window_height:
            self.top = self._world_height - self.window_height

    def draw(self):
        subsurface = self._world.subsurface(self.left, self.top, self.window_width, self.window_height)
        self._screen.blit(
            pg.transform.scale(subsurface, (self._world_width, SCREEN_HEIGHT)),
            (0, 0)
        )

    def zoom_in(self):
        # TODO: abstract out the zoom delta to let the user configure a zoom speed for the cam
        if self.scale > self.min_scale:
            self.scale *= 0.95

    def zoom_out(self):
        if self.scale < self.max_scale:
            self.scale *= 1.05

    def get_camera_rect(self):
        return pg.Rect(self.left, self.top, self.window_width, self.window_height)

    def convert_camera_to_world_coord(self, camera_coord):
        scaled_pos = (camera_coord[0] / self.scale, camera_coord[1] / self.scale)
        mouse_pos_pymunk_coord = (scaled_pos[0] + self.left, scaled_pos[1] + self.top)
        return mouse_pos_pymunk_coord