import pyxel
import math

class Ally:

    def __init__(self, x: int, y: int, w: int = 16, h: int = 16):
        self.x = x
        self.y = y
        self.w = w  # size of sprite is 16x16
        self.h = h

    def update(self):
        ...

    def draw(self):
        ...

class Enemy:

    def __init__(self, x: int, y: int, speed: float = 1.0, w: int=16, h: int =16):
        self.x = x
        self.y = y
        self.speed = speed
        self.w = w  # size of sprite is 16x16
        self.h = h
        self.vx: float = 0.0
        self.vy: float = 0.0

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        ...
    
    def move(self, direction: int): # direction is in degrees
        self.vx = self.speed * math.cos(math.radians(direction))
        self.vy = self.speed * math.sin(math.radians(direction))

class Player(Ally):

    def __init__(self, x: int, y: int, w: int = 16, h: int = 16):
        super().__init__(x, y, w, h)

    def draw(self):
        pyxel.blt(
            self.x, self.y, 0,
            0, 0,
            self.w, self.h, 0
        )
    
    def update(self):
        ...

class SimpleEnemy(Enemy):

    def __init__(self, x: int, y: int, w: int = 16, h: int = 16):
        super().__init__(x, y, w, h)

    def draw(self):
        pyxel.blt(
            self.x, self.y, 0,
            16, 0,
            self.w, self.h, 0
        )