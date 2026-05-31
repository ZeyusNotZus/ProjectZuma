from sympy import randprime

import os
import json
from random import Random

from configs import SCREEN_HEIGHT, SCREEN_WIDTH, MAP_2, MAP_TYPE, GRID_HEIGHT, GRID_WIDTH, GAME_THEME, TILE_SIZE, SPAWN_INTERVAL
from entities import Bullet, Enemy, Player, Crosshair, SimpleEnemy

# REMOVE AFTER IMPLEMENTATION OF STANDARDIZED SCREEN SIZE


class Model:
    def __init__(self, rng: Random | None = None):  
        self._exp: int = 0
        self._enemies: list[Enemy] = []
        self._bullets: list[Bullet] = []
        self._is_game_over: bool = False

        self._map = MAP_2
        self._enemy_spawn_rate: int = 60
        self._enemy_move_speed: int = 60

        self._start_tiles = self._find_all_start_tiles()
        self._end_tile = self._find_tile_coordinate('E')
        self._rng = rng or Random()
        self._player = Player(SCREEN_WIDTH // 2 - 8, SCREEN_HEIGHT // 2 + 25, self._rng)     
        self._crosshair = Crosshair()

        # get settings
        settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
        with open(settings_path) as f:
            settings = json.load(f)
        self._lives: int = settings["player_lives"]
        self._enemies_per_round: int = settings["enemies_per_round"]

    def _find_tile_coordinate(self, character: str) -> tuple[int, int]:
        for row_idx, row in enumerate(self._map):
            for col_idx, tile in enumerate(row):
                if tile == character:
                    return (col_idx, row_idx)
                
        return (-1, -1)

    def _find_all_start_tiles(self) -> list[tuple[int, int]]:
        start_tiles: list[tuple[int, int]] = []
        for row_idx, row in enumerate(self._map):
            for col_idx, tile in enumerate(row):
                if tile == 'S':
                    start_tiles.append((col_idx, row_idx))

        return start_tiles

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
    def enemies(self) -> list[Enemy]:
        return self._enemies

    @property
    def bullets(self) -> list[Bullet]:
        return self._bullets
    
    @property
    def crosshair(self):
        return self._crosshair
    
    @property
    def map_data(self) -> MAP_TYPE:
        return self._map
    
    @property
    def lives(self) -> int:
        return self._lives
    
    def update(self, frame: int):
        self._player.update(self._bullets)
        self.generate_enemy(frame)
        self.move_enemy(frame)
        self.move_bullet()
        self.check_collisions()
    
    def move_enemy(self, frame: int):
        if frame % self._enemy_move_speed == 0: # enemy movement every 60 frames / 2 seconds (based on specs)
            for enemy in self._enemies[:]:
                if (enemy.tile_x, enemy.tile_y) == self._end_tile:
                    self._enemies.remove(enemy)
                    self._lives -= 1
                    if self._lives <= 0:
                        self._is_game_over = True
                    continue

                valid_moves: list[tuple[int, int]] = []        
                
                opposite_dir = None
                if enemy.last_dir is not None:
                    opposite_dir = (-enemy.last_dir[0], -enemy.last_dir[1]) # notes the opposite direction of last move direction


                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    if opposite_dir and (dx, dy) == opposite_dir: # dont backtrack
                        continue

                    next_x, next_y = enemy.tile_x + dx, enemy.tile_y + dy
                    
                    if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT: # bounds of map
                        if self._map[next_y][next_x] in ['P', 'S', 'E']:
                            valid_moves.append((dx, dy))                 

                if valid_moves:
                    chosen_dx, chosen_dy = self._rng.choice(valid_moves) # choose randomly at an intersection
                    enemy.move_tile(chosen_dx, chosen_dy) # WARNING: THIS MAY CAUSE LOOPING WHEN A PATH HAS A LOOP



    def move_bullet(self):
        for bullet in self._bullets[:]:
            bullet.update()
            if (bullet.x < 0 or bullet.x > SCREEN_WIDTH or 
                bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                self._bullets.remove(bullet)

    def generate_enemy(self, frame: int):
        if frame % self._enemy_spawn_rate== 0:
            if not self._start_tiles:
                return
            
            enemy_color = self._rng.choice(GAME_THEME)

        spawn_tile = self._rng.choice(self._start_tiles)
        spawn_x, spawn_y = spawn_tile
        
        enemy = SimpleEnemy(spawn_x, spawn_y, enemy_color, 0.5)
        self._enemies.append(enemy)
    
    def check_collisions(self):
        for bullet in self._bullets[:]:
            bx, by = bullet.x, bullet.y

            for enemy in self._enemies[:]:
                ex = enemy.tile_x * TILE_SIZE
                ey = enemy.tile_y * TILE_SIZE

                if (ex <= bx <= ex + TILE_SIZE and
                    ey <= by <= ey + TILE_SIZE):

                    if bullet.color == enemy.color:
                        self._bullets.remove(bullet)
                        self._enemies.remove(enemy)
                        self._exp += 1
                        break