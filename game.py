import pyxel
import entities

SCREEN_WIDTH: int = 120
SCREEN_HEIGHT: int = 120

class Game:
    def __init__(self):
        self.exp = 0
        self.player = entities.Player(SCREEN_WIDTH // 2 - 8, SCREEN_HEIGHT // 2 + 25)
        self.enemies = []
        self.bullets = []
        
        # pyxel
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title = "Project Z")
        pyxel.mouse(True)
        pyxel.load("sprites.pyxres")
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.player.update(self.bullets)

        if pyxel.frame_count % 60 == 0:
            self.generate_enemy()

        for enemy in self.enemies:
            enemy.update()
            enemy.move(0)

        for bullet in self.bullets[:]:
            bullet.update()

            if (bullet.x < 0 or bullet.x > SCREEN_WIDTH or 
                bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                self.bullets.remove(bullet)
            
        self.check_collisions()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(
            5, 5, 
            "EXP{:04}".format(self.exp),
            6
        )

        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()
        
        for bullet in self.bullets:
            bullet.draw()
    
    def generate_enemy(self):
        enemy = entities.SimpleEnemy(0, 25, 0.5)
        self.enemies.append(enemy)
    
    def check_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (enemy.x <= bullet.x <= enemy.x + enemy.w and
                    enemy.y <= bullet.y <= enemy.y + enemy.h):
                    
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    
                    self.exp += 1
                    break


def main():
    Game()

if __name__ == "__main__":
    main()
