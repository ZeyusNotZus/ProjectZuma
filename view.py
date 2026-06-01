import pyxel
from classes import DrawHandler, ModelData, UpdateHandler, GameState

from configs import SCREEN_HEIGHT, SCREEN_WIDTH

class View:
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        self._width = width
        self._height = height

    def init_window(self, update_handler: UpdateHandler, draw_handler: DrawHandler):
        pyxel.init(self._width, self._height, title = "Project Z", fps = 30)
        pyxel.mouse(False)
        pyxel.load("sprites.pyxres")
        pyxel.run(update_handler.update, draw_handler.draw)

    def draw_game(self, entities: list[dict[str, int]], current_wave: int, lives: int, exp: int) -> None:
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

        # # entities
        # model.player.draw()

        # enemies = model.enemies
        # for enemy in enemies:
        #     enemy.draw()
        
        # bullets = model.bullets
        # for bullet in bullets:
        #     bullet.draw()

        # # drawing of crosshair
        # model.crosshair.draw()

        pyxel.bltm(0, 0, 0, 0, 0, 16 * 16, 8 * 16) # tile map
        pyxel.bltm(0, 128, 1, 0, 0, 16 * 16, 3 * 16) # bar

        for entity in entities:
            if entity["circ"]:
                pyxel.circ(entity["circ_x"], entity["circ_y"], entity["circ_rad"], entity["circ_col"])
            if entity["blt"]:
                pyxel.blt(entity["x"], entity["y"], entity["img"], entity["u"], entity["v"], entity["w"], entity["h"], entity["colkey"])


        pyxel.text(203, 138, "ROUND:{:02}".format(current_wave), 5)
        pyxel.text(203, 146, "LIVES:{:02}".format(lives), 8)
        pyxel.text(203, 154, "EXP:{:04}".format(exp), 7)

    def print_state(self, state: GameState) -> None:
        if state == GameState.PREPARATION:
            pyxel.text(10, 10, "PREPARATION PHASE", 10)
            pyxel.text(10, 20, "Press SPACE to start wave", 7)
        elif state == GameState.GAME_OVER:
            pyxel.text(SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT//2, "GAME OVER", 8)