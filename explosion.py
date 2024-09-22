import pygame
from pygame.sprite import Sprite
import random
import math

class Explosion(Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.center = center
        self.frame = 0
        self.max_frame = 60  # 爆炸效果持续的帧数
        self.fragments = []
        self.create_fragments()

    def create_fragments(self):
        num_fragments = 20 if self.size == "lg" else 10
        for _ in range(num_fragments):
            speed = random.uniform(1, 5)
            angle = random.uniform(0, 360)
            dx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
            dy = speed * pygame.math.Vector2(1, 0).rotate(angle).y
            size = random.randint(1, 3)
            self.fragments.append({
                'pos': list(self.center),
                'vel': [dx, dy],
                'size': size,
                'color': (random.randint(200, 255), random.randint(0, 100), 0)
            })

    def update(self):
        self.frame += 1
        if self.frame > self.max_frame:
            self.kill()
        else:
            for fragment in self.fragments:
                fragment['pos'][0] += fragment['vel'][0]
                fragment['pos'][1] += fragment['vel'][1]
                fragment['vel'][1] += 0.1  # 添加重力效果

    def draw(self, screen):
        for fragment in self.fragments:
            pygame.draw.circle(screen, fragment['color'],
                               (int(fragment['pos'][0]), int(fragment['pos'][1])),
                               fragment['size'])

class ShipExplosion(Sprite):
    def __init__(self, center):
        super().__init__()
        self.center = center
        self.frame = 0
        self.max_frame = 180  # 增加爆炸效果持续的帧数
        self.fragments = []
        self.create_fragments()
        self.start_time = pygame.time.get_ticks()  # 记录爆炸开始的时间
        self.duration = 3000  # 爆炸持续3秒

    def create_fragments(self):
        num_fragments = 50  # 增加碎片数量
        for _ in range(num_fragments):
            angle = random.uniform(0, 360)
            speed = random.uniform(0.5, 2)  # 降低初始速度
            size = random.randint(5, 15)  # 增加碎片大小
            rotation_speed = random.uniform(-3, 3)  # 降低旋转速度
            self.fragments.append({
                'pos': list(self.center),
                'vel': [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))],
                'size': size,
                'color': (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)),  # 更亮的颜色
                'rotation': random.uniform(0, 360),
                'rotation_speed': rotation_speed
            })

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()
        else:
            self.frame += 1
            for fragment in self.fragments:
                fragment['pos'][0] += fragment['vel'][0]
                fragment['pos'][1] += fragment['vel'][1]
                fragment['vel'][1] += 0.03  # 减小重力效果
                fragment['rotation'] += fragment['rotation_speed']
                # 逐渐减小速度，模拟空气阻力
                fragment['vel'][0] *= 0.995
                fragment['vel'][1] *= 0.995
                # 逐渐缩小碎片
                if self.frame > self.max_frame / 2:
                    fragment['size'] = max(0, fragment['size'] - 0.05)

    def draw(self, screen):
        for fragment in self.fragments:
            rotated_rect = pygame.Surface((fragment['size'], fragment['size']), pygame.SRCALPHA)
            pygame.draw.rect(rotated_rect, fragment['color'], (0, 0, fragment['size'], fragment['size']))
            rotated_image = pygame.transform.rotate(rotated_rect, fragment['rotation'])
            screen.blit(rotated_image, (int(fragment['pos'][0] - rotated_image.get_width() // 2),
                                        int(fragment['pos'][1] - rotated_image.get_height() // 2)))

class SimpleShipExplosion(Sprite):
    def __init__(self, center):
        super().__init__()
        self.center = center
        self.frame = 0
        self.max_frame = 240  # 爆炸效果持续的帧数
        self.fragments = []
        self.create_fragments()

    def create_fragments(self):
        num_fragments = 20  # 碎片数量
        for _ in range(num_fragments):
            angle = random.uniform(0, 360)
            speed = random.uniform(1, 3)
            size = random.randint(5, 15)  # 碎片大小
            self.fragments.append({
                'pos': list(self.center),
                'vel': [speed * pygame.math.Vector2(1, 0).rotate(angle).x,
                        speed * pygame.math.Vector2(1, 0).rotate(angle).y],
                'size': size,
                'color': (255, 0, 0)  # 红色
            })

    def update(self):
        self.frame += 1
        if self.frame > self.max_frame:
            self.kill()
        else:
            for fragment in self.fragments:
                fragment['pos'][0] += fragment['vel'][0]
                fragment['pos'][1] += fragment['vel'][1]
                fragment['vel'][1] += 0.1  # 添加重力效果
                # 逐渐缩小碎片
                fragment['size'] = max(0, fragment['size'] - 0.2)

    def draw(self, screen):
        for fragment in self.fragments:
            pygame.draw.rect(screen, fragment['color'],
                             (int(fragment['pos'][0]), int(fragment['pos'][1]),
                              int(fragment['size']), int(fragment['size'])))

class BombExplosion(Sprite):
    def __init__(self, center, screen_size):
        super().__init__()
        self.center = center
        self.screen_size = screen_size
        self.radius = 0
        self.max_radius = min(screen_size) // 2
        self.duration = 1000  # 1秒
        self.start_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        progress = (current_time - self.start_time) / self.duration
        if progress >= 1:
            self.kill()
        else:
            self.radius = int(self.max_radius * progress)

    def draw(self, screen):
        surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 0, 0, 128), self.center, self.radius)
        screen.blit(surface, (0, 0))