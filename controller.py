from classes import DrawHandler, UpdateHandler
from model import Model
from view import View

class Controller(UpdateHandler, DrawHandler):
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
        self.frame = 0

    def start_game(self):
        self._view.init_window(self, self)

    def update(self):
        if not self._model.is_game_over:
            self._model.update(self.frame)
            self.frame += 1

    def draw(self):
        self._view.draw_game(self._model)