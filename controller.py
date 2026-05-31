from classes import DrawHandler, UpdateHandler, GameState
from model import Model
from view import View
import pyxel

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
        # for now SPACE bar ung wave start
        if pyxel.btnp(pyxel.KEY_SPACE) and self._model.state == GameState.PREPARATION:
            self._model.start_wave()

        # Update the model
        if self._model.state != GameState.GAME_OVER:
            self._model.update(self.frame)
            self._frame += 1

    def draw(self):
        self._view.draw_game(self._model)