import pyxel

class BaseSprite:

    def __init__(self, x:int, y:int, w:int=16, h:int=16):
        self.x = x
        self.y = y
        self.w = w  # size of sprite is 16x16
        self.h = h

    def update(self):
        ...

    def draw(self):
        ...

class PlayerSprite(BaseSprite):

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