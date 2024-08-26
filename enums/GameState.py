from enum import Enum


class GameState(Enum):
    MAIN_MENU = 0
    IN_MATRIX = 1
    PAUSE = 2
    OUT_OF_MATRIX = 3
