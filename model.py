import os
import json
import random
import maps
from entities import Bullet, Enemy, Player, Crosshair, SimpleEnemy

# REMOVE AFTER IMPLEMENTATION OF STANDARDIZED SCREEN SIZE

SCREEN_WIDTH: int = 256
SCREEN_HEIGHT: int = 128
TILE_SIZE: int = 16
GRID_WIDTH: int = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // TILE_SIZE

class Model:
    def __init__(self):  
        self._exp: int = 0
        self._enemies: list[Enemy] = []
        self._bullets: list[Bullet] = []
        self._is_game_over: bool = False

        self._map = maps.MAP_2

        self._start_tiles = self.find_all_start_tiles()
        self._end_tile = self.find_tile_coordinate('E')

        self._player = Player(SCREEN_WIDTH // 2 - 8, SCREEN_HEIGHT // 2 + 25)     
        self._crosshair = Crosshair(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # get settings
        settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
        with open(settings_path) as f:
            settings = json.load(f)
        self._lives: int = settings["player_lives"]
        self._enemies_per_round: int = settings["enemies_per_round"]

    def find_tile_coordinate(self, character: str) -> tuple[int, int]:
        for row_idx, row in enumerate(self._map):
            for col_idx, tile in enumerate(row):
                if tile == character:
                    return (col_idx, row_idx)
                
        return (-1, -1)

    def find_all_start_tiles(self) -> list[tuple[int, int]]:
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
    def map_data(self) -> maps.MAP_TYPE:
        return self._map
    
    @property
    def lives(self) -> int:
        return self._lives
    
    def update(self, frame: int):
        self._player.update(self._bullets)

        if frame % 60 == 0: # enemy spawn every 60 frames / 2 seconds
            self.generate_enemy()

        if frame % 60 == 0: # enemy movement every 60 frames / 2 seconds (based on specs)
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
                    chosen_dx, chosen_dy = random.choice(valid_moves) # choose randomly at an intersection
                    enemy.move_tile(chosen_dx, chosen_dy) # WARNING: THIS MAY CAUSE LOOPING WHEN A PATH HAS A LOOP

        for bullet in self._bullets[:]:
            bullet.update()
            if (bullet.x < 0 or bullet.x > SCREEN_WIDTH or 
                bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                self._bullets.remove(bullet)
            
        self.check_collisions()

    def generate_enemy(self):
        if not self._start_tiles:
            return
        
        enemy_color: int = random.choice([1, 2, 7, 8, 9, 12])

        spawn_tile = random.choice(self._start_tiles)
        spawn_x, spawn_y = spawn_tile
        
        enemy = SimpleEnemy(spawn_x, spawn_y, enemy_color, 0.5)
        self._enemies.append(enemy)
    
    def check_collisions(self):
        for bullet in self._bullets[:]:
            for enemy in self._enemies[:]:
                
                enemy_left = enemy.tile_x * TILE_SIZE
                enemy_right = enemy_left + TILE_SIZE
                enemy_top = enemy.tile_y * TILE_SIZE
                enemy_bottom = enemy_top + TILE_SIZE
                
                if (enemy_left <= bullet.x <= enemy_right and
                    enemy_top <= bullet.y <= enemy_bottom):
                    
                    if bullet.color == enemy.color:
                        if bullet in self._bullets: 
                            self._bullets.remove(bullet)
                        if enemy in self._enemies: 
                            self._enemies.remove(enemy)
                        
                        self._exp += 1
                        break