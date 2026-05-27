import pyxel
import math

class Ally:

    def __init__(self, x: float, y: float, w: int = 16, h: int = 16):
        self.x = x
        self.y = y
        self.w = w  # size of sprite is 16x16
        self.h = h

    def update(self):
        ...

    def draw(self):
        ...

class Enemy:

    def __init__(self, x: float, y: float, speed: float = 1.0, w: int = 16, h: int = 16):
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
        self.vy = -self.speed * math.sin(math.radians(direction))

class Bullet:
    def __init__(self, x: float, y: float, angle: float, speed: float = 3.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.w = 8
        self.h = 8
        
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pyxel.circ(self.x, self.y, 2, 8)


class Player(Ally):

    def __init__(self, x: float, y: float, w: int = 16, h: int = 16):
        super().__init__(x, y, w, h)
    
    def update(self, bullets_list: list):
        super().update()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            player_center_x = self.x + self.w / 2
            player_center_y = self.y + self.h / 2

            target_x = pyxel.mouse_x
            target_y = pyxel.mouse_y

            angle = math.atan2(target_y - player_center_y, target_x - player_center_x)
            new_bullet = Bullet(player_center_x, player_center_y, angle)

            bullets_list.append(new_bullet)

    def draw(self):
        pyxel.blt(
            self.x, self.y, 0,
            0, 0,
            self.w, self.h, 0
        )

class SimpleEnemy(Enemy):

    def __init__(self, x: float, y: float, speed: float = 1.0, w: int = 16, h: int = 16):
        super().__init__(x, y, speed, w, h)

    def draw(self):
        pyxel.blt(
            self.x, self.y, 0,
            16, 0,
            self.w, self.h, 0
        )