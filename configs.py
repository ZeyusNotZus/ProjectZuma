from enum import Enum


##### VIEW #######

SCREEN_WIDTH: int = 256
SCREEN_HEIGHT: int = 176
GAME_WIDTH: int = 256
GAME_HEIGHT: int = 128
TILE_SIZE: int = 16
GRID_WIDTH: int = GAME_WIDTH // TILE_SIZE
GRID_HEIGHT: int = GAME_HEIGHT // TILE_SIZE



 ####### MAP ###########
type MAP_TYPE = list[list[str]]
# W - Wall, S - Spawn, P - Path, E - End, . - floor

MAP_1 = [
    ['S', 'P', '.', 'P', 'P', 'P', '.', '.'],
    ['.', 'P', 'P', 'P', '.', 'P', 'P', '.'],
    ['.', '.', '.', '.', '.', '.', 'P', '.'],
    ['.', 'P', 'P', 'P', 'P', 'P', 'P', '.'],
    ['.', 'P', '.', '.', '.', '.', '.', '.'],
    ['.', 'P', 'P', 'P', '.', 'P', 'E', '.'],
    ['.', '.', '.', 'P', '.', 'P', '.', '.'],
    ['.', '.', '.', 'P', 'P', 'P', '.', '.'],
]

MAP_2 = [
    ['S', 'P', '.', 'P', 'P', 'P', '.', '.', 'P', 'P', 'P', '.', '.', '.', '.', '.'],
    ['.', 'P', 'P', 'P', '.', 'P', 'P', '.', 'P', '.', 'P', '.', 'P', 'P', 'P', 'E'],
    ['.', '.', '.', '.', '.', '.', 'P', '.', 'P', '.', 'P', '.', 'P', '.', '.', '.'],
    ['.', 'P', 'P', 'P', 'P', 'P', 'P', '.', 'P', '.', 'P', '.', 'P', '.', '.', '.'],
    ['.', 'P', '.', '.', '.', '.', '.', '.', 'P', '.', 'P', '.', 'P', '.', '.', '.'],
    ['.', 'P', 'P', 'P', '.', 'P', 'P', 'P', 'P', '.', 'P', '.', 'P', '.', '.', '.'],
    ['.', '.', '.', 'P', '.', 'P', '.', '.', '.', '.', 'P', 'P', 'P', '.', '.', '.'],
    ['.', '.', '.', 'P', 'P', 'P', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
]


####### SPRITES ###########
class PyxelColor(Enum):
    BLACK   = 0
    DARKBLUE = 1
    DARKPURPLE = 2
    DARKGREEN = 3
    BROWN = 4
    DARKGRAY = 5
    LIGHTGRAY = 6
    WHITE = 7
    RED = 8
    ORANGE = 9
    YELLOW = 10
    GREEN = 11
    BLUE = 12
    PURPLE = 13
    PINK = 14
    PEACH = 15

GAME_THEME: list[PyxelColor] = [PyxelColor.DARKBLUE, PyxelColor.DARKPURPLE, PyxelColor.WHITE, PyxelColor.RED, PyxelColor.ORANGE, PyxelColor.BLUE]


ENEMY_SPRITES: dict[int, int] = {
                                1 : 0,
                                2 : 16,
                                7 : 32,
                                8 : 48,
                                9 : 64,
                                12 : 80
                                }

SPAWN_INTERVAL: int = 60 