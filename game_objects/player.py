import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 150, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.shield = 50
        self.max_shield = 50
        self.attack_speed = 1.0
        self.damage = 20
        self.level = 1
        self.experience = 0
        self.exp_to_next_level = 100

        self.shield_regen = 0
        self.health_regen = 0
        self.regen_timer = 0
        
        self.damage_cooldown = 1000
        self.last_damage = 0
        self.is_alive = True
        
    def update(self):
        if not self.is_alive:
            return
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed
        
        screen = pygame.display.get_surface()
        self.rect.clamp_ip(screen.get_rect())

        self.regen_timer += 1
        if self.regen_timer >= 120:
            if self.shield < self.max_shield and self.shield_regen > 0:
                self.shield = min(self.max_shield, self.shield + self.shield_regen)
                print(f"Shield regenerated: {self.shield:.1f}/{self.max_shield}")
                
            if self.health < self.max_health and self.health_regen > 0:
                self.health = min(self.max_health, self.health + self.health_regen)
                print(f"Health regenerated: {self.health:.1f}/{self.max_health}")
                
            self.regen_timer = 0
        
    def take_damage(self, amount, enemy_name, shield_break=False):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage >= self.damage_cooldown:
            self.regen_timer = 0
            
            if shield_break:
                self.shield = 0
                print(f"Shield broken by {enemy_name}!")
            elif self.shield > 0:
                self.shield -= amount
                if self.shield < 0:
                    self.health += self.shield
                    self.shield = 0
            else:
                self.health -= amount
            
            self.last_damage = current_time
            print(f"Took {amount} damage from {enemy_name}! Shield: {self.shield:.1f}, HP: {self.health:.1f}")
            if self.health <= 0:
                self.health = 0
                self.is_alive = False
            
    def add_experience(self, amount):
        self.experience += amount
        print(f"EXP gained: {amount}, Total: {self.experience}/{self.exp_to_next_level}")
        return self.experience >= self.exp_to_next_level
