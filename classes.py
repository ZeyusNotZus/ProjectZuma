import pyxel
import enum
from typing import Protocol, Sequence

from dataclasses import dataclass
from enum import Enum, auto

from entities import Bullet, Crosshair, Enemy, Player, SimpleEnemy
from configs import MAP_TYPE, MAP_2, GAME_THEME, PyxelColor


class GameState(Enum):
    START_MENU = auto()
    LEADERBOARD = auto()
    PREPARATION = auto()
    WAVE_ACTIVE = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class ModelData(Protocol):
    @property
    def exp(self) -> int:
        ...

    @property
    def player(self) -> Player:
       ...

    @property
    def enemies(self) -> Sequence[Enemy]:
        ...

    @property
    def bullets(self) -> Sequence[Bullet]:
        ...
    
    @property
    def crosshair(self) -> Crosshair:
        ...

    @property
    def map_data(self) -> MAP_TYPE:
        ...

    @property
    def lives(self) -> int:
        ...

    @property
    def state(self) -> GameState:
        ...

    @property
    def current_wave(self) -> int:
        ...

class UpdateHandler(Protocol):
    def update(self) -> None: ...

class DrawHandler(Protocol):
    def draw(self) -> None: ...


@dataclass
class Wave:
    base_enemy_count: int   # IN FRAMES 30 = 1 sec,,,, 60 = 2 secs
    base_enemy_speed: float


@dataclass
class MapDef:
    grid: list[list[str]]
    waves: list[Wave]
    allowed_enemies: list[type[Enemy]]
    allowed_colors: list[PyxelColor]



DEFAULT_MAP = MapDef(
    grid = MAP_2,
    waves = [Wave(5, 60), Wave(10, 45), Wave(15, 30)],
    allowed_enemies=[SimpleEnemy],
    allowed_colors=GAME_THEME,
)


class GameMode(Enum):
    CAMPAIGN = auto()
    ENDLESS = auto()


class Drawable(Protocol):
    def draw_info() -> dict[str, int]:
        ...