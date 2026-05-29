from classes import DrawHandler, UpdateHandler
from model import Model
from view import View

class Controller(UpdateHandler, DrawHandler):
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
        self._frame = 0
    
    @property
    def frame(self):
        return self._frame

    def start_game(self):
        self._view.init_window(self, self)

    def update(self):
        if not self._model.is_game_over:
            self._model.update(self.frame)
            self._frame += 1

    def draw(self):
        self._view.draw_game(self._model)