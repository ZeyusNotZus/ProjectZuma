import pyxel
import math
import random

TILE_SIZE: int = 16
SCREEN_WIDTH: int = 256
SCREEN_HEIGHT: int = 128

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

    def draw(self):
        ...

class Enemy:
    def __init__(self, tile_x: int, tile_y: int, color: int, speed: float = 1.0):
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
    def color(self) -> int:
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

    def draw(self):
        ...
    
class Bullet:
    def __init__(self, x: float, y: float, angle: float, color: int, size: int = 5, speed: float = 1.908):
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
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y
    
    @property
    def color(self):
        return self._color
    
    @property
    def size(self):
        return self._size
    
    def update(self):
        self._x += self._vx
        self._y += self._vy

    def draw(self):
        pyxel.circ(self._x, self._y, self._size, self._color)

class Player:
    def __init__(self, x: float, y: float, cooldown: float = 33.33, w: int = 16, h: int = 16):
        self._x = x
        self._y = y
        self._w = w  # size of sprite is 16x16
        self._h = h
        self._shoot_cooldown = cooldown
        self._last_shot = -self._shoot_cooldown
        self._loaded_bullet: int = self.get_bullet()

    def can_shoot(self) -> bool:
        return pyxel.frame_count - self._last_shot >= self._shoot_cooldown
    
    def cooldown(self):
        self._last_shot = pyxel.frame_count
    
    def get_bullet(self) -> int:
        bullet_color: int = random.choice([1, 2, 7, 8, 9, 12])
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
            self._x = max(0, min(SCREEN_WIDTH - self._w, self._x))
                
        if dy != 0:
            self._y += dy
            # bounds
            self._y = max(0, min(SCREEN_HEIGHT - self._h, self._y))

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


    def draw(self):
        sprite_map = {
        1: 0,
        2: 16,
        7: 32,
        8: 48,
        9: 64,
        12: 80 
        }

        sprite = sprite_map.get(self._loaded_bullet, 0)

        pyxel.blt(
            self._x, self._y, 0,
            sprite, 0,
            self._w, self._h, 0
        )

class SimpleEnemy(Enemy):
    def __init__(self, x: int, y: int, color: int, speed: float = 1.0):
        super().__init__(x, y, color, speed)

    def draw(self):
        simple_enemy_sprites: dict[int, int] = {
            1 : 0,
            2 : 16,
            7 : 32,
            8 : 48,
            9 : 64,
            12 : 80
            }
        
        sprite = simple_enemy_sprites[self._color]

        pyxel.blt(
            self._x, self._y, 0,
            sprite, 16,
            self._w, self._h, 0
        )

class Crosshair:
    def __init__(self, x: float, y: float, w: int = 16, h: int = 16):
        self._x = pyxel.mouse_x
        self._y = pyxel.mouse_y
        self._w = w  # size of sprite is 16x16
        self._h = h
    
    def draw(self):
        pyxel.blt(
            pyxel.mouse_x, pyxel.mouse_y, 0,
            0, 48,
            self._w, self._h, 0
        )