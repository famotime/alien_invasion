import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.settings = ai_settings # Renamed for consistency with task, was self.ai_settings
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.moving_right = False
        self.moving_left = False

        # Power-up attributes
        self.shield_active = False
        self.rapid_fire_active = False
        self.multi_shot_active = False
        self.speed_boost_active = False
        self.powerup_timers = {}  # Stores end_time for each power-up

        # Store original values that power-ups might change
        self.original_ship_speed = self.settings.ship_speed_factor # Assuming ship_speed_factor is the one to modify
        # Assuming bullet_cooldown is a setting for firing rate. If not, this needs to be adapted.
        # Let's assume there's no direct bullet_cooldown setting in Settings for now, and rapid_fire will adjust bullets_allowed.
        # self.original_bullet_cooldown = getattr(self.settings, 'bullet_cooldown', 200) # Example value

        # Placeholder for visual effect of shield
        self.shield_image = None # Will be set if shield is active
        self.shield_rect = None

    def activate_powerup(self, powerup_type, duration_ms): # duration_ms from powerup object
        """Activate a power-up and set its timer."""
        print(f"Ship activating {powerup_type} for {duration_ms} ms.")
        current_time = pygame.time.get_ticks()
        self.powerup_timers[powerup_type] = current_time + duration_ms

        if powerup_type == 'shield':
            self.shield_active = True
            # Create a simple visual for the shield (e.g., a slightly larger, transparent circle)
            # This is a basic example; a proper image or drawing routine would be better.
            shield_surface = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (0, 0, 255, 100), shield_surface.get_rect().center, self.rect.width // 2 + 5)
            self.shield_image = shield_surface
            self.shield_rect = self.shield_image.get_rect(center=self.rect.center)

        elif powerup_type == 'rapid_fire':
            self.rapid_fire_active = True
            # Actual effect handled in fire_bullet in game_functions.py
            # Potentially adjust settings.bullets_allowed if that's how rapid fire is implemented
            # self.settings.bullets_allowed = self.settings.bullets_allowed_rapid_fire (needs this setting)

        elif powerup_type == 'multi_shot':
            self.multi_shot_active = True
            # Actual effect handled in fire_bullet in game_functions.py

        elif powerup_type == 'speed_boost':
            self.speed_boost_active = True
            self.settings.ship_speed_factor = self.original_ship_speed * getattr(self.settings, 'speed_boost_factor', 1.5) # Needs speed_boost_factor in settings

    def update_powerups(self):
        """Check timers and deactivate expired power-ups."""
        current_time = pygame.time.get_ticks()
        powerup_types_to_check = ['shield', 'rapid_fire', 'multi_shot', 'speed_boost']

        for powerup_type in powerup_types_to_check:
            if self.powerup_timers.get(powerup_type, float('inf')) <= current_time:
                print(f"Deactivating {powerup_type} for ship.")
                if powerup_type == 'shield':
                    self.shield_active = False
                    self.shield_image = None
                elif powerup_type == 'rapid_fire':
                    self.rapid_fire_active = False
                    # Revert settings.bullets_allowed if it was changed
                    # self.settings.bullets_allowed = self.settings.bullets_allowed_normal (needs this setting)
                elif powerup_type == 'multi_shot':
                    self.multi_shot_active = False
                elif powerup_type == 'speed_boost':
                    self.speed_boost_active = False
                    self.settings.ship_speed_factor = self.original_ship_speed
                
                self.powerup_timers.pop(powerup_type, None)

    def update(self):
        """根据移动标志调整飞船的位置 and update powerups."""
        self.update_powerups() # Check and update active power-ups

        # 更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed_factor # Use settings directly
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed_factor # Use settings directly

        # 根据self.center更新rect对象
        self.rect.centerx = self.center

        # Update shield position if active
        if self.shield_active and self.shield_image:
            self.shield_rect.center = self.rect.center


    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
        if self.shield_active and self.shield_image:
            self.screen.blit(self.shield_image, self.shield_rect)


    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
        # self.centery = self.screen_rect.bottom - self.rect.height / 2 # Original centery for ship
        self.rect.centerx = self.center # Update rect position
        self.rect.bottom = self.screen_rect.bottom # Ensure ship is at the bottom

        # Deactivate all powerups and reset timers when ship is centered (e.g. after a hit)
        self.shield_active = False
        self.rapid_fire_active = False
        self.multi_shot_active = False
        if self.speed_boost_active: # Only reset speed if it was active
            self.settings.ship_speed_factor = self.original_ship_speed
        self.speed_boost_active = False
        self.powerup_timers = {}
        self.shield_image = None
        # self.bombs = self.settings.bombs_per_ship  # 重置炸弹数量
