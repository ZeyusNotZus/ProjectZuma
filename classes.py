import enum
from typing import Protocol, Sequence

from entities import Bullet, Crosshair, Enemy, Player
from configs import MAP_TYPE
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

class UpdateHandler(Protocol):
    def update(self) -> None: ...

class DrawHandler(Protocol):
    def draw(self) -> None: ...

