import pygame
from game_objects.player import Player
from game_objects.enemy_system import EnemyManager
from game_objects.weapon_system import WeaponSystem
from systems.upgrade_system import UpgradeSystem

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("QIYANA SURVIVOR")

def main():
    running = True
    player = Player()
    enemy_manager = EnemyManager()
    weapon_system = WeaponSystem()
    upgrade_system = UpgradeSystem()
    
    cheat_code = ""
    time_scale = 1.0
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    time_scale = 0.5
                    if event.unicode.isalpha():
                        cheat_code += event.unicode.upper()
                        if "QIYANA" in cheat_code:
                            player.level += 1
                            player.experience = 0
                            player.max_health += 20
                            player.health = player.max_health
                            cheat_code = ""
                            print("Cheat activated: Level Up!")
                            upgrade_system.show_stats_window(screen, player)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    time_scale = 1.0
                    cheat_code = ""

        player.update()
        enemy_manager.update(player)
        weapon_system.update(player, enemy_manager.enemies)
        
        hits = pygame.sprite.spritecollide(player, enemy_manager.enemies, False)
        if hits:
            for enemy in hits:
                player.take_damage(enemy.damage, enemy.name, shield_break=enemy.shield_break)
            if player.health <= 0:
                running = False
        
        projectile_hits = pygame.sprite.groupcollide(weapon_system.projectiles, enemy_manager.enemies, True, True)
        for projectile, enemies in projectile_hits.items():
            for enemy in enemies:
                print(f"Defeated {enemy.name} enemy!")
            exp_gain = len(enemies) * 10
            if player.add_experience(exp_gain):
                player.level += 1
                player.experience -= player.exp_to_next_level
                player.exp_to_next_level = int(player.exp_to_next_level * 1.2)
                player.max_health += 20
                player.health = player.max_health
                upgrade_system.show_stats_window(screen, player)
        
        screen.fill(BLACK)
        all_sprites.draw(screen)
        enemy_manager.draw(screen)
        weapon_system.draw(screen)
        
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"HP: {int(player.health)}/{player.max_health}", True, RED)
        exp_text = font.render(f"EXP: {int(player.experience)}/{int(player.exp_to_next_level)}", True, GREEN)
        level_text = font.render(f"Level: {player.level}", True, YELLOW)
        shield_text = font.render(f"Shield: {int(player.shield)}/{player.max_shield}", True, (0, 200, 255))
        
        screen.blit(health_text, (10, 10))
        screen.blit(exp_text, (10, 40))
        screen.blit(level_text, (10, 70))
        screen.blit(shield_text, (10, 100))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
