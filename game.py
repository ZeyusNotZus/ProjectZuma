import pyxel
import entities

SCREEN_WIDTH: int = 120
SCREEN_HEIGHT: int = 120

class Game:
    def __init__(self):
        self.exp = 0
        
        self.player = entities.Player(SCREEN_WIDTH // 2 - 8, SCREEN_HEIGHT // 2 - 8)
       
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Project Z")
        pyxel.load("sprites.pyxres")
        pyxel.run(self.update, self.draw)
        
    
    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(
            5, 5, 
            "EXP{:04}".format(self.exp),
            6
        )

        self.player.draw()

def main():
    Game()

if __name__ == "__main__":
    main()
