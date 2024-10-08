from pygame import Rect

import colors
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FONTS_DIRECTORY, WORLD_WIDTH
import pygame as pg
import pygame.freetype


class Hud:
    pg.freetype.init()
    GAME_FONT = pg.freetype.Font(f"{FONTS_DIRECTORY}/Mobsters.ttf", 65)

    def __init__(self, neo, level):
        self.neo = neo
        self.level = level

    def draw(self, screen):
        self.GAME_FONT.render_to(screen, (SCREEN_WIDTH - 155, 10), "FLOOR " + str(self.level.current_player_floor), colors.ui_font_color)
        ammo_text = 'RELOADING...' if self.neo.weapon.reloading else f"{self.neo.weapon.bullets_remaining} / {self.neo.weapon.MAGAZINE_SIZE}"
        self.GAME_FONT.render_to(screen, (50, SCREEN_HEIGHT - 100), ammo_text, colors.ui_font_color)
