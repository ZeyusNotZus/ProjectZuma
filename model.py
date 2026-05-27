from typing import Sequence

from entities import Bullet, Enemy, Crosshair, Player, SimpleEnemy
# REMOVE AFTER IMPLEMENTATION OF STANDARDIZED SCREEN SIZE

SCREEN_WIDTH: int = 128
SCREEN_HEIGHT: int = 128

class Model:
    def __init__(self):
        self._exp: int = 0
        self._player = Player(SCREEN_WIDTH // 2 - 8, SCREEN_HEIGHT // 2 + 25)
        self._enemies: list[Enemy]  = []
        self._bullets: list[Bullet] = []
        self._crosshair = Crosshair(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self._is_game_over: bool = False

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @property
    def exp(self) -> int:
        return self._exp

    @property
    def player(self) -> Player:
        return self._player

    #Changed to Sequence so only model can mutate
    @property
    def enemies(self) -> Sequence[Enemy]:
        return tuple(self._enemies)

    @property
    def bullets(self) -> Sequence[Bullet]:
        return tuple(self._bullets)
    
    @property
    def crosshair(self) -> Crosshair:
        return self._crosshair
    
    # Controller passes frame (to avoid depending on pyxel)
    def update(self, frame: int):
        self._player.update(self._bullets)

        if frame % 60 == 0:
            self.generate_enemy()

        for enemy in self._enemies:
            enemy.update()
            enemy.move(0)

        for bullet in self._bullets[:]:
            bullet.update()
            bullet_x, bullet_y = bullet.coordinates
            if (bullet_x < 0 or bullet_x > SCREEN_WIDTH or 
                bullet_y < 0 or bullet_y > SCREEN_HEIGHT):
                self._bullets.remove(bullet)
            
        self.check_collisions()

    def generate_enemy(self):
        enemy = SimpleEnemy(0, 25, 0.5)
        self._enemies.append(enemy)
    
    def check_collisions(self):
        for bullet in self._bullets[:]:
            for enemy in self._enemies[:]:
                enemy_w, enemy_h = enemy.dimensions
                bullet_x, bullet_y = bullet.coordinates
                enemy_x, enemy_y = enemy.coordinates
                if (enemy_x <= bullet_x <= enemy_x + enemy_w and
                    enemy_y <= bullet_y <= enemy_y + enemy_h):
                    
                    if bullet in self._bullets:
                        self._bullets.remove(bullet)
                    if enemy in self._enemies:
                        self._enemies.remove(enemy)
                    
                    self._exp += 1
                    break