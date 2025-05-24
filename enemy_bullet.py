import pygame
from pygame.sprite import Sprite

class EnemyBullet(Sprite):
    """A class to manage bullets fired by aliens."""

    def __init__(self, ai_settings, screen, alien):
        """Create a bullet object at the alien's current position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.enemy_bullet_width,
                                ai_settings.enemy_bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

        self.color = ai_settings.enemy_bullet_color
        self.speed_factor = ai_settings.enemy_bullet_speed_factor

    def update(self):
        """Move the bullet down the screen."""
        # Update the decimal position of the bullet.
        self.y += self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
