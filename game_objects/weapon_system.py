import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 7
        
    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

class WeaponSystem:
    def __init__(self):
        self.projectiles = pygame.sprite.Group()
        self.shoot_delay = 20
        self.shoot_timer = 0
        
    def update(self, player, enemies):
        self.shoot_timer = max(0, self.shoot_timer - 1)
        
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and self.shoot_timer == 0:
            self.shoot(player)
            self.shoot_timer = self.shoot_delay
            
        self.projectiles.update()
        
        for projectile in self.projectiles:
            if not pygame.display.get_surface().get_rect().colliderect(projectile.rect):
                projectile.kill()
            
    def shoot(self, player):
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - player.rect.centerx
        dy = mouse_pos[1] - player.rect.centery
        dist = math.sqrt(dx**2 + dy**2)
        if dist != 0:
            direction = (dx/dist, dy/dist)
            projectile = Projectile(player.rect.centerx, player.rect.centery, direction)
            self.projectiles.add(projectile)
            
    def draw(self, screen):
        self.projectiles.draw(screen)
