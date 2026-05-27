import pyxel

# REMOVE AFTER IMPLEMENTATION OF STANDARDIZED SCREEN SIZE

SCREEN_WIDTH: int = 128
SCREEN_HEIGHT: int = 128

class View:
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        self._width = width
        self._height = height

    def init_window(self, controller):
        pyxel.init(self._width, self._height, title = "Project Z")
        pyxel.mouse(True)
        pyxel.load("sprites.pyxres")
        pyxel.run(controller.update, controller.draw)

    def draw_game(self, exp: int, player, enemies: list, bullets: list):
        pyxel.cls(0)
        pyxel.text(5, 5, "EXP:{:04}".format(exp), 6)

        # drawing of entities

        player.draw()

        for enemy in enemies:
            enemy.draw()
        
        for bullet in bullets:
            bullet.draw()