from configs import PyxelColor, GAME_THEME, ENEMY_SPRITES, TILE_SIZE, GAME_HEIGHT, GAME_WIDTH
import pyxel
import math
from random import Random

class Ally:
    def __init__(self, x: float, y: float, cooldown: int = 0, w: int = 16, h: int = 16):
        self._x = x
        self._y = y
        self._w = w  # size of sprite is 16x16
        self._h = h
        self._shoot_cooldown = cooldown
        self._last_shot = -100

        ...

    def can_shoot(self) -> bool:
        return pyxel.frame_count - self._last_shot >= self._shoot_cooldown
    
    def cooldown(self):
        self._last_shot = pyxel.frame_count

    def update(self):
        ...

    def draw_info(self) -> dict[str, int]:
        ...

class Enemy:
    def __init__(self, tile_x: int, tile_y: int, color: PyxelColor, speed: float = 1.0):
        self._tile_x = tile_x
        self._tile_y = tile_y
        self._color = color
        self._speed = speed
        self._w = TILE_SIZE
        self._h = TILE_SIZE
        self._last_dir = None # prevents enemy from backtracking

    # pixel position of enemy
    @property
    def _x(self) -> float:
        return self._tile_x * self._w
        
    @property
    def _y(self) -> float:
        return self._tile_y * self._h
    
    # width and height 
    @property
    def w(self) -> int:
        return self._w
        
    @property
    def h(self) -> int:
        return self._h

    @property
    def color(self) -> PyxelColor:
        return self._color
    
    # position in matrix
    @property
    def tile_x(self) -> int:
        return self._tile_x

    @property
    def tile_y(self) -> int:
        return self._tile_y

    @property
    def last_dir(self) -> tuple[int, int] | None:
        return self._last_dir
    
    def update(self):
        ...

    def move_tile(self, dx: int, dy: int):
        self._tile_x += dx
        self._tile_y += dy
        self._last_dir = (dx, dy)

    def draw_info(self) -> dict[str, int]:
        ...
    
class Bullet:
    def __init__(self, x: float, y: float, angle: float, color: PyxelColor, size: int = 5, speed: float = 1.908):
        self._x = x
        self._y = y
        self._speed = speed
        self._w = 8
        self._h = 8
        self._color = color
        self._size = size
        self._vx = self._speed * math.cos(angle)
        self._vy = self._speed * math.sin(angle)


    @property
    def x(self) -> float:
        return self._x
        
    @property
    def y(self) -> float:
        return self._y
    
    @property
    def color(self) -> PyxelColor:
        return self._color
    
    @property
    def size(self) -> int:
        return self._size
    
    def update(self):
        self._x += self._vx
        self._y += self._vy

    def draw_info(self) -> dict[str, int]:
        # pyxel.circ(self._x, self._y, self._size, self._color.value)
        return {
            "circ": True,
            "circ_x": self._x,
            "circ_y": self._y,
            "circ_rad": self._size,
            "circ_col": self._color.value,
            "blt": False,
            "x": 0,
            "y": 0,
            "img": 0,
            "u": 0,
            "v": 0,
            "w": 0,
            "h": 0,
            "colkey": 0 
        }

class Player:
    def __init__(self, x: float, y: float, rng: Random, cooldown: int = 33, w: int = 16, h: int = 16):
        self._x = x
        self._y = y
        self._w = w  # size of sprite is 16x16
        self._h = h
        self._shoot_cooldown = cooldown
        self._last_shot = -self._shoot_cooldown
        self._rng = rng
        self._loaded_bullet = self.get_bullet()

    def can_shoot(self) -> bool:
        return pyxel.frame_count - self._last_shot >= self._shoot_cooldown
    
    def cooldown(self):
        self._last_shot = pyxel.frame_count
    
    def get_bullet(self) -> PyxelColor:
        bullet_color: PyxelColor = self._rng.choice(seq=GAME_THEME)
        return bullet_color

    def update(self, bullets_list: list[Bullet]):
        self._speed: float = 1.0

        dx = 0
        dy = 0

        # movement
        if pyxel.btn(pyxel.KEY_W):
            dy -= self._speed
        if pyxel.btn(pyxel.KEY_S):
            dy += self._speed
        if pyxel.btn(pyxel.KEY_A):
            dx -= self._speed
        if pyxel.btn(pyxel.KEY_D):
            dx += self._speed

        if dx != 0:
            self._x += dx
            # bounds
            self._x = max(0, min(GAME_WIDTH - self._w, self._x))
                
        if dy != 0:
            self._y += dy
            # bounds
            self._y = max(0, min(GAME_HEIGHT - self._h, self._y))

        # shooting
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.can_shoot():
                self.cooldown()
                player_center_x = self._x + self._w / 2
                player_center_y = self._y + self._h / 2

                target_x: int = pyxel.mouse_x + 8
                target_y: int = pyxel.mouse_y + 8

                angle:float = math.atan2(target_y - player_center_y, target_x - player_center_x)
                shoot_bullet = Bullet(player_center_x, player_center_y, angle, self._loaded_bullet)
                bullets_list.append(shoot_bullet)
                self._loaded_bullet = self.get_bullet()


    def draw_info(self) -> dict[str, int]:
        # pyxel.circ(self._x + self._w // 2, self._y + self._h // 2, 6, self._loaded_bullet.value)
        sprite = int((math.atan2(- pyxel.mouse_y + self._y, - pyxel.mouse_x + self._x) + 17 * math.pi / 8) / (math.pi / 4)) % 8 * 16

        # pyxel.blt(
        #     self._x, self._y, 0,
        #     sprite, 0,
        #     self._w, self._h, 0
        # )
        return {
            "circ": True,
            "circ_x": self._x + self._w // 2,
            "circ_y": self._y + self._h // 2,
            "circ_rad": 6,
            "circ_col": self._loaded_bullet.value,
            "blt": True,
            "x": self._x,
            "y": self._y,
            "img": 0,
            "u": sprite,
            "v": 0,
            "w": self._w,
            "h": self._h,
            "colkey": 0
        }

class SimpleEnemy(Enemy):
    def __init__(self, x: int, y: int, color: PyxelColor, speed: float = 1.0):
        super().__init__(x, y, color, speed)

    def draw_info(self) -> dict[str, int]:
        sprite = ENEMY_SPRITES[self._color.value]

        # pyxel.blt(
        #     self._x, self._y, 0,
        #     sprite, 16,
        #     self._w, self._h, 0
        # )

        return {
            "circ": False,
            "circ_x": 0,
            "circ_y": 0,
            "circ_rad": 0,
            "circ_col": 0,
            "blt": True,
            "x": self._x,
            "y": self._y,
            "img": 0,
            "u": sprite,
            "v": 16,
            "w": self._w,
            "h": self._h,
            "colkey": 0
        }

# class Crosshair:
#     def __init__(self, x: float, y: float, w: int = 16, h: int = 16):
#         self._x = pyxel.mouse_x
#         self._y = pyxel.mouse_y
#         self._w = w  # size of sprite is 16x16
#         self._h = h
    #---------- Since madaming unused
#     def draw(self):
#         pyxel.blt(
#             pyxel.mouse_x, pyxel.mouse_y, 0,
#             0, 48,
#             self._w, self._h, 0
#         )

class Crosshair:
    def __init__(self, x: float, y: float, w: int = 16, h: int = 16):
        self._x = pyxel.mouse_x
        self._y = pyxel.mouse_y
        self._w = w  # size of sprite is 16x16
        self._h = h
    
    def draw_info(self) -> dict[str, int]:
        # pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 0, 48, 16, 16, 0)
        return {
            "circ": False,
            "circ_x": 0,
            "circ_y": 0,
            "circ_rad": 0,
            "circ_col": 0,
            "blt": True,
            "x": pyxel.mouse_x,
            "y": pyxel.mouse_y,
            "img": 0,
            "u": 0,
            "v": 48,
            "w": 16,
            "h": 16,
            "colkey": 0 
        }

class RegeneratorEnemy(Enemy):
    MOVE_TO_REGEN: int = 5
    def __init__(self, x: int, y: int, color: PyxelColor, speed: float = 1.0):
        super().__init__(x, y, color, speed)
        self._regen_cd = 0

    def move_tile(self, dx: int, dy: int):

        super().move_tile(dx, dy)
        pass