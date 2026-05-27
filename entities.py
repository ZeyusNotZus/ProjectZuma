import pyxel
import math

class Ally:

    def __init__(self, x: float, y: float, w: int = 16, h: int = 16):
        self._x = x
        self._y = y
        self._w = w  # size of sprite is 16x16
        self._h = h

    def update(self):
        ...

    def draw(self):
        ...

class Enemy:

    def __init__(self, x: float, y: float, speed: float = 1.0, w: int = 16, h: int = 16):
        self._x = x
        self._y = y
        self._speed = speed
        self._w = w  # size of sprite is 16x16
        self._h = h
        self._vx: float = 0.0
        self._vy: float = 0.0

    def update(self):
        self._x += self._vx
        self._y += self._vy

    def draw(self):
        ...
    
    def move(self, direction: int): # direction is in degrees
        self._vx = self._speed * math.cos(math.radians(direction))
        self._vy = -self._speed * math.sin(math.radians(direction))

class Bullet:
    def __init__(self, x: float, y: float, angle: float, speed: float = 3.0):
        self._x = x
        self._y = y
        self._speed = speed
        self._w = 8
        self._h = 8
        
        self._vx = self._speed * math.cos(angle)
        self._vy = self._speed * math.sin(angle)

    def update(self):
        self._x += self._vx
        self._y += self._vy

    def draw(self):
        pyxel.circ(self._x, self._y, 2, 8)


class Player(Ally):

    def __init__(self, x: float, y: float, w: int = 16, h: int = 16):
        super().__init__(x, y, w, h)
    
    def update(self, bullets_list: list):
        super().update()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            player_center_x = self._x + self._w / 2
            player_center_y = self._y + self._h / 2

            target_x = pyxel.mouse_x + 8
            target_y = pyxel.mouse_y + 8

            angle = math.atan2(target_y - player_center_y, target_x - player_center_x)
            new_bullet = Bullet(player_center_x, player_center_y, angle)

            bullets_list.append(new_bullet)

    def draw(self):
        pyxel.blt(
            self._x, self._y, 0,
            0, 0,
            self._w, self._h, 0
        )

class SimpleEnemy(Enemy):

    def __init__(self, x: float, y: float, speed: float = 1.0, w: int = 16, h: int = 16):
        super().__init__(x, y, speed, w, h)

    def draw(self):
        pyxel.blt(
            self._x, self._y, 0,
            16, 0,
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
            0, 16,
            self._w, self._h, 0
        )