import pygame as pg


class LevelOne:
    floor_height = 175

    def __init__(self):
        self.width = 1920
        self.height = 2160

    def update(self):
        pass

    def draw(self, screen):
        for i in range(0, self.height, self.floor_height + 100):
            pg.draw.rect(screen, (255, 255, 255), (50, i + 20, self.width - 100, self.floor_height))
