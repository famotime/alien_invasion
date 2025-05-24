import pygame
from pygame.sprite import Sprite

class BaseAlien(Sprite):
    """基本外星人类，定义所有外星人类型的共同行为"""
    def __init__(self, ai_settings, screen, image_path='images/alien.bmp', health=1, points=50, speed_factor=None):
        """初始化基本外星人并设置其起始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.health = health
        self.points = points
        self.speed_factor = speed_factor if speed_factor is not None else self.ai_settings.alien_speed_factor

        # 每个外星人最初都在屏幕左上角附近 (this will be set by create_alien)
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

        # 外星人爆炸的声音文件 (can be overridden by subclasses)
        self.sound = 'sound/enemy1_down.wav'

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """检测外星人是否位于屏幕边缘"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        return False

    def update(self):
        """移动外星人"""
        current_speed = self.speed_factor
        self.x += (current_speed * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def take_damage(self, amount):
        """外星人受到伤害"""
        self.health -= amount
        if self.health <= 0:
            return True
        return False

class NormalAlien(BaseAlien):
    """普通外星人"""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen, 
                         points=ai_settings.normal_alien_points)
        self.sound = 'sound/enemy1_down.wav' # Default sound

class FastAlien(BaseAlien):
    """快速外星人"""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen, 
                         speed_factor=ai_settings.alien_speed_factor * ai_settings.fast_alien_speed_multiplier, 
                         points=ai_settings.fast_alien_points)
        # Consider a different image, e.g., tinting or a new asset
        # self.image = pygame.image.load('images/fast_alien.bmp') 
        self.sound = 'sound/enemy2_down.wav' 

class TankAlien(BaseAlien):
    """坦克外星人，具有更高生命值但速度较慢"""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen, 
                         health=ai_settings.tank_alien_health, 
                         points=ai_settings.tank_alien_points, 
                         speed_factor=ai_settings.alien_speed_factor * ai_settings.tank_alien_speed_multiplier)
        # Consider a different image
        # self.image = pygame.image.load('images/tank_alien.bmp')
        self.sound = 'sound/enemy3_down.wav'

from enemy_bullet import EnemyBullet # Import EnemyBullet

class ShooterAlien(BaseAlien):
    """射手外星人，可以发射子弹"""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen, points=ai_settings.shooter_alien_points)
        self.fire_interval_frames = ai_settings.shooter_alien_fire_cooldown
        self.frames_since_last_shot = 0
        # self.image = pygame.image.load('images/shooter_alien.bmp') # Optional: distinct image
        self.sound = 'sound/enemy1_down.wav' # Death sound
        try:
            self.shoot_sound_obj = pygame.mixer.Sound('sound/enemy3_flying.wav')
        except pygame.error as e:
            print(f"Warning: Could not load shoot sound for ShooterAlien: {e}")
            self.shoot_sound_obj = None

    def update(self):
        """更新射手外星人的位置并尝试射击"""
        super().update()
        self.frames_since_last_shot += 1
        # Firing logic is now primarily in try_fire, called from game_functions

    def try_fire(self, enemy_bullets_group, ai_settings, screen):
        """尝试射击，如果达到射击间隔且未达到子弹上限"""
        if self.frames_since_last_shot >= self.fire_interval_frames and \
           len(enemy_bullets_group) < ai_settings.enemy_bullets_allowed:
            
            self.frames_since_last_shot = 0
            new_bullet = EnemyBullet(ai_settings, screen, self)
            enemy_bullets_group.add(new_bullet)
            if self.shoot_sound_obj:
                self.shoot_sound_obj.play()
            return True
        return False

# The original Alien class is now replaced by NormalAlien and other specialized types.
# If there was any code directly instantiating Alien, it would need to be updated
# to instantiate NormalAlien or another appropriate type.
# For example, in create_alien function in game_functions.py
# alien = Alien(ai_settings, screen) would become
# alien = NormalAlien(ai_settings, screen) or a random choice from different types.
# This change is outside the scope of this specific subtask (modifying alien.py)
# but is important for the overall integration.
