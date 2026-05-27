from model import Model
from view import View

class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view

    def start_game(self):
        self._view.init_window(self)

    def update(self):
        if not self._model.is_game_over:
            self._model.update()

    def draw(self):
        self._view.draw_game(
            exp=self._model.exp,
            player=self._model.player,
            enemies=self._model.enemies,
            bullets=self._model.bullets
        )