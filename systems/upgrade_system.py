import pygame

class UpgradeSystem:
    def __init__(self):
        self.stats = {
            '1': {'name': 'Damage', 'key': 'damage', 'increment': 5},
            '2': {'name': 'Speed', 'key': 'speed', 'increment': 0.5},
            '3': {'name': 'Max Health', 'key': 'max_health', 'increment': 20},
            '4': {'name': 'Attack Speed', 'key': 'attack_speed', 'increment': 0.2},
            '5': {'name': 'Max Shield', 'key': 'max_shield', 'increment': 10},
            '6': {'name': 'Shield Regen', 'key': 'shield_regen', 'increment': 0.1},
            '7': {'name': 'Health Regen', 'key': 'health_regen', 'increment': 0.12}
        }

    def show_stats_window(self, screen, player):
        window_width = 600
        window_height = 500
        window_x = (screen.get_width() - window_width) // 2
        window_y = (screen.get_height() - window_height) // 2
        
        stats_window = True
        font = pygame.font.Font(None, 48)
        
        while stats_window:
            pygame.draw.rect(screen, (50, 50, 50), (window_x, window_y, window_width, window_height))
            pygame.draw.rect(screen, (100, 100, 100), (window_x, window_y, window_width, window_height), 3)
            
            title = font.render(f"Level Up! (Level {player.level})", True, (255, 255, 255))
            screen.blit(title, (window_x + 20, window_y + 20))
            
            y_offset = 100
            for key, stat in self.stats.items():
                current_value = getattr(player, stat['key'])
                text = font.render(f"{key}. {stat['name']}: {current_value:.1f} (+{stat['increment']})", True, (255, 255, 255))
                screen.blit(text, (window_x + 30, window_y + y_offset))
                y_offset += 60
            
            instructions = font.render("Press 1-7 to upgrade stat", True, (255, 255, 255))
            screen.blit(instructions, (window_x + 20, window_y + y_offset + 20))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode in self.stats:
                        stat = self.stats[event.unicode]
                        current_value = getattr(player, stat['key'])
                        setattr(player, stat['key'], current_value + stat['increment'])
                        return