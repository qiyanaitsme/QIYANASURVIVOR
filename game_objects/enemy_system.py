import pygame
import random
from enum import Enum

class EnemyType(Enum):
    BASIC = {"health": 30, "speed": 2, "color": (255, 0, 0)}
    FAST = {"health": 20, "speed": 4, "color": (0, 255, 0)}
    TANK = {"health": 100, "speed": 1, "color": (255, 255, 0)}
    SHIELD_BREAKER = {"health": 40, "speed": 3, "color": (255, 0, 255), "shield_break": True}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        self.type = enemy_type
        stats = EnemyType[enemy_type].value
        self.image = pygame.Surface((20, 20))
        self.image.fill(stats["color"])
        self.rect = self.image.get_rect()
        self.health = stats["health"]
        self.speed = stats["speed"]
        self.damage = 5
        self.shield_break = stats.get("shield_break", False)
        self.name = enemy_type
        self.spawn_position()
        
    def spawn_position(self):
        side = random.randint(0, 3)
        if side == 0:
            self.rect.x = random.randint(0, 800)
            self.rect.y = -20
        elif side == 1:
            self.rect.x = 820
            self.rect.y = random.randint(0, 600)
        elif side == 2:
            self.rect.x = random.randint(0, 800)
            self.rect.y = 620
        else:
            self.rect.x = -20
            self.rect.y = random.randint(0, 600)

class EnemyManager:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0
        
    def scale_enemy_stats(self, enemy, player_level):
        enemy.health *= (1 + 0.1 * player_level)
        enemy.speed *= (1 + 0.05 * player_level)
        enemy.damage *= (1 + 0.1 * player_level)
        
    def update(self, player):
        self.spawn_timer += 1
        if self.spawn_timer >= 60:
            if random.random() < 0.05:
                new_enemy = Enemy('SHIELD_BREAKER')
            else:
                enemy_type = random.choice(['BASIC', 'FAST', 'TANK'])
                new_enemy = Enemy(enemy_type)
            
            self.scale_enemy_stats(new_enemy, player.level)
            self.enemies.add(new_enemy)
            self.spawn_timer = 0
            
        for enemy in self.enemies:
            self.move_enemy_to_player(enemy, player)
            
    def move_enemy_to_player(self, enemy, player):
        dx = player.rect.x - enemy.rect.x
        dy = player.rect.y - enemy.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            enemy.rect.x += dx / dist * enemy.speed
            enemy.rect.y += dy / dist * enemy.speed
            
    def draw(self, screen):
        self.enemies.draw(screen)
