import pyxel
from classes import DrawHandler, ModelData, UpdateHandler
# REMOVE AFTER IMPLEMENTATION OF STANDARDIZED SCREEN SIZE

SCREEN_WIDTH: int = 128
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

        for row_idx, row in enumerate(model.map_data):
            for col_idx, tile_type in enumerate(row):
                px = col_idx * TILE_SIZE
                py = row_idx * TILE_SIZE
                match tile_type:
                    case 'W':
                        pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 13) # CHAMHE LATER FOR SPRITES
                    case 'S':
                        pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 3)
                    case 'E':
                        pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 8)
                    case 'P':
                        pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 15)
                    case '.':
                        pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 13)
                    case _:
                        ...

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

        pyxel.text(5, 5, "EXP:{:04}".format(model.exp), 6)