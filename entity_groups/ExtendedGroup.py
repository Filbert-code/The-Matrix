import pygame as pg

import colors
from constants import WORLD_HEIGHT
from util.common import to_pygame_coords, to_pygame_rect


class ExtendedGroup(pg.sprite.Group):

    def handle_event(self, event):
        for spr in self.sprites():
            # Check if the sprite has a `handle_event` method.
            if hasattr(spr, 'handle_event'):
               spr.handle_event(event)

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            # self.spritedict[spr] = surface_blit(spr.image, spr.rect)
            pg.draw.rect(surface, colors.agent_searching, to_pygame_rect(spr.rect, WORLD_HEIGHT))
        self.lostsprites = []