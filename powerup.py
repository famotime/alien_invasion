import pygame
from pygame.sprite import Sprite
import random

class PowerUp(Sprite):
    """A base class to represent a power-up in the game."""

    def __init__(self, ai_game, powerup_type, image_path):
        """Initialize the power-up and set its starting position."""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.powerup_type = powerup_type
        self.image_loaded = False # Flag to track if image was loaded

        # Attempt to load the power-up image.
        try:
            self.image = pygame.image.load(image_path)
            # 获取外星飞船的尺寸作为参考
            alien_image = pygame.image.load('images/alien.bmp')
            alien_rect = alien_image.get_rect()
            # 将道具图片缩小到外星飞船的一半大小
            self.image = pygame.transform.scale(self.image, (alien_rect.width // 2, alien_rect.height // 2))
            self.image_loaded = True
        except pygame.error as e:
            print(f"Warning: Could not load image {image_path}: {e}")
            # Create a placeholder surface if image loading fails.
            placeholder_size = (30, 30) # Default size for placeholder
            self.image = pygame.Surface(placeholder_size)
            # Use a default color (magenta) or a color based on type
            # For simplicity, using magenta for all placeholders.
            self.image.fill((255, 0, 255)) # Magenta
            print(f"Created placeholder for {self.powerup_type} at {image_path}")

        self.rect = self.image.get_rect()

        # Set the initial position of the power-up.
        # rect.x should be a random position within the screen width.
        # rect.y should be at the top of the screen (e.g., slightly negative or 0).
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.rect.height  # Start just above the screen

        # Store the power-up's position as a floating-point number for precise movement.
        self.y = float(self.rect.y)

        # Duration of the power-up effect (in milliseconds or game ticks)
        # This might be loaded from settings based on powerup_type, e.g., self.settings.powerup_durations[powerup_type]
        # Using a placeholder value for now.
        self.duration = 5000  # Example: 5 seconds

        # Active flag: True when the power-up effect is active on the player
        self.active = False

    def update(self):
        """Update the power-up's position."""
        # Move the power-up down the screen.
        # We'll assume settings.powerup_speed will be added later.
        # Using a placeholder value if not available.
        powerup_speed = getattr(self.settings, 'powerup_speed', 1.0) # Default to 1.0 if not in settings
        self.y += powerup_speed
        self.rect.y = int(self.y)

    def blitme(self):
        """Draw the power-up at its current location."""
        self.screen.blit(self.image, self.rect)

    def activate(self):
        """Activate the power-up's effect."""
        # This method will be overridden by specific power-up types
        # or will trigger changes in the ship/game settings.
        self.active = True
        print(f"{self.powerup_type} activated!") # Placeholder action

    def deactivate(self):
        """Deactivate the power-up's effect."""
        # This method will be overridden by specific power-up types
        # or will revert changes in the ship/game settings.
        self.active = False
        print(f"{self.powerup_type} deactivated!") # Placeholder action

# Example of how specific power-ups might be derived (optional, for context):
# class ShieldPowerUp(PowerUp):
#     def __init__(self, ai_game):
#         super().__init__(ai_game, 'shield', 'images/shield_powerup.png') # Assuming image path
#         self.duration = getattr(self.settings, 'shield_duration', 7000)
#
#     def activate(self):
#         super().activate()
#         # Add shield effect to the ship
#         self.ai_game.ship.activate_shield(self.duration)
#
#     def deactivate(self):
#         super().deactivate()
#         # Remove shield effect from the ship
#         self.ai_game.ship.deactivate_shield()

# class RapidFirePowerUp(PowerUp):
#     def __init__(self, ai_game):
#         super().__init__(ai_game, 'rapid_fire', 'images/rapid_fire_powerup.png') # Assuming image path
#         self.duration = getattr(self.settings, 'rapid_fire_duration', 10000)
#
#     def activate(self):
#         super().activate()
#         # Modify ship's firing rate
#         self.ai_game.ship.activate_rapid_fire(self.duration)
#
#     def deactivate(self):
#         super().deactivate()
#         # Revert ship's firing rate
#         self.ai_game.ship.deactivate_rapid_fire()


class ShieldPowerUp(PowerUp):
    """A power-up that grants the ship temporary invincibility."""
    def __init__(self, ai_game):
        """Initialize the shield power-up."""
        super().__init__(ai_game, 'shield', 'images/shield_powerup.bmp')
        # Specific duration for this power-up can be set here or via settings
        # self.duration = getattr(self.settings, 'shield_duration', 7000)


class RapidFirePowerUp(PowerUp):
    """A power-up that increases the ship's firing rate."""
    def __init__(self, ai_game):
        """Initialize the rapid fire power-up."""
        super().__init__(ai_game, 'rapid_fire', 'images/rapid_fire_powerup.bmp')
        # self.duration = getattr(self.settings, 'rapid_fire_duration', 10000)


class MultiShotPowerUp(PowerUp):
    """A power-up that allows the ship to fire multiple projectiles at once."""
    def __init__(self, ai_game):
        """Initialize the multi-shot power-up."""
        super().__init__(ai_game, 'multi_shot', 'images/multi_shot_powerup.bmp')
        # self.duration = getattr(self.settings, 'multi_shot_duration', 10000)


class SpeedBoostPowerUp(PowerUp):
    """A power-up that temporarily increases the ship's movement speed."""
    def __init__(self, ai_game):
        """Initialize the speed boost power-up."""
        super().__init__(ai_game, 'speed_boost', 'images/speed_boost_powerup.bmp')
        # self.duration = getattr(self.settings, 'speed_boost_duration', 8000)
