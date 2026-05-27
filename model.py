import entities
import pyxel

# REMOVE AFTER IMPLEMENTATION OF STANDARDIZED SCREEN SIZE

SCREEN_WIDTH: int = 128
SCREEN_HEIGHT: int = 128

class Model:
    def __init__(self):
        self._exp: int = 0
        self._player = entities.Player(SCREEN_WIDTH // 2 - 8, SCREEN_HEIGHT // 2 + 25)
        self._enemies: list = []
        self._bullets: list = []
        self._crosshair = entities.Crosshair(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self._is_game_over: bool = False

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @property
    def exp(self) -> int:
        return self._exp

    @property
    def player(self):
        return self._player

    @property
    def enemies(self) -> list:
        return self._enemies

    @property
    def bullets(self) -> list:
        return self._bullets
    
    @property
    def crosshair(self) -> list:
        return self._crosshair
    
    def update(self):
        self._player.update(self._bullets)

        if pyxel.frame_count % 60 == 0:
            self.generate_enemy()

        for enemy in self._enemies:
            enemy.update()
            enemy.move(0)

        for bullet in self._bullets[:]:
            bullet.update()
            if (bullet._x < 0 or bullet._x > SCREEN_WIDTH or 
                bullet._y < 0 or bullet._y > SCREEN_HEIGHT):
                self._bullets.remove(bullet)
            
        self.check_collisions()

    def generate_enemy(self):
        enemy = entities.SimpleEnemy(0, 25, 0.5)
        self._enemies.append(enemy)
    
    def check_collisions(self):
        for bullet in self._bullets[:]:
            for enemy in self._enemies[:]:
                if (enemy._x <= bullet._x <= enemy._x + enemy._w and
                    enemy._y <= bullet._y <= enemy._y + enemy._h):
                    
                    if bullet in self._bullets:
                        self._bullets.remove(bullet)
                    if enemy in self._enemies:
                        self._enemies.remove(enemy)
                    
                    self._exp += 1
                    break