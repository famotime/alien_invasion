import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """飞船发射的子弹"""
    def __init__(self, ai_settings, screen, ship):
        """在飞船位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen

        # 在(0, 0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        # 发射子弹的声音文件
        self.sound = 'sound/bullet.wav'

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class BulletR(Bullet):
    """向右边发射的子弹"""
    def __init__(self, ai_settings, screen, ship):
        super().__init__(ai_settings, screen, ship)
        # 在(0, 0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_height, ai_settings.bullet_width)
        self.rect.centery = ship.rect.centery
        self.rect.right = ship.rect.right

        # 存储用小数表示的子弹位置
        self.x = float(self.rect.x)

    def update(self):
        """向右移动子弹"""
        # 更新表示子弹位置的小数
        self.x += self.speed_factor
        self.rect.x = self.x


class BulletL(Bullet):
    """向左边发射的子弹"""
    def __init__(self, ai_settings, screen, ship):
        super().__init__(ai_settings, screen, ship)
        # 在(0, 0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_height, ai_settings.bullet_width)
        self.rect.centery = ship.rect.centery
        self.rect.left = ship.rect.left

        # 存储用小数表示的子弹位置
        self.x = float(self.rect.x)

    def update(self):
        """向左移动子弹"""
        # 更新表示子弹位置的小数
        self.x -= self.speed_factor
        self.rect.x = self.x
