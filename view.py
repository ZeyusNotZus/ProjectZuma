import pyxel
from classes import DrawHandler, ModelData, UpdateHandler

# REMOVE AFTER IMPLEMENTATION OF STANDARDIZED SCREEN SIZE

SCREEN_WIDTH: int = 256
SCREEN_HEIGHT: int = 128
TILE_SIZE: int = 16

class View:
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        self._width = width
        self._height = height

    def init_window(self, update_handler: UpdateHandler, draw_handler: DrawHandler):
        pyxel.init(self._width, self._height, title = "Project Z")
        pyxel.mouse(False)
        pyxel.load("sprites.pyxres")
        pyxel.run(update_handler.update, draw_handler.draw)

    def draw_game(self, model: ModelData):
    #def draw_game(self, exp: int, player, enemies: list, bullets: list, crosshair):
        pyxel.cls(0)

        # map
        # tile_sprites = {
        #     'W': (16, 32),  # Wall
        #     'S': (32, 32),  # Spawn
        #     'E': (48, 32),  # End
        #     'P': (64, 32),  # Path
        #     '.': (80,  32),  # Background
        # }

        # for row_idx, row in enumerate(model.map_data):
        #     for col_idx, tile_type in enumerate(row):
        #         px = col_idx * TILE_SIZE
        #         py = row_idx * TILE_SIZE
 
        #         u, v = tile_sprites.get(tile_type, (0, 32))
        #         pyxel.blt(px, py, 0, u, v, TILE_SIZE, TILE_SIZE)

        pyxel.bltm(0,0,0,0,0,16*16,8*16)

        # entities
        model.player.draw()

        enemies = model.enemies
        for enemy in enemies:
            enemy.draw()
        
        bullets = model.bullets
        for bullet in bullets:
            bullet.draw()

        # drawing of crosshair
        model.crosshair.draw()

        pyxel.text(220, 118, "EXP:{:04}".format(model.exp), 7)