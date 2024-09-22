import pygame.font
from pygame.sprite import Group, Sprite
from ship import Ship


class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats, ship):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.ship = ship  # 添加这行

        # 显示得分信息时使用的字体设置
        self.text_color = (79,195,247)
        self.font = pygame.font.SysFont(None, 48)

        # 准备得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_bombs()  # 添加这行

    def prep_score(self):
        """将得分转换为渲染图像"""
        # 将stats.score的值圆整到10的整数倍
        rounded_score = round(self.stats.score, -1)
        # 加入千分位分隔符
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        # 将得分放在屏幕右上角（顶部和右边距离窗口边界20像素）
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "HighScore: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为渲染图像"""
        self.level_image = self.font.render("Level: " + str(self.stats.level), True, self.text_color)
        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还余下多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_bombs(self):
        """显示还余下多少炸弹"""
        self.bombs = Group()
        for bomb_number in range(self.ship.bombs):
            bomb = Bomb(self.ai_settings, self.screen, self.ship)
            bomb.rect.x = 10 + bomb_number * bomb.rect.width
            bomb.rect.y = self.screen_rect.bottom - 10 - bomb.rect.height
            self.bombs.add(bomb)

    def show_score(self):
        """在屏幕上显示当前得分、最高得分、剩余飞船数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        self.bombs.draw(self.screen)

class Bomb(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super(Bomb, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.ship = ship

        # 绘制表示炸弹的文字
        self.font = pygame.font.SysFont(None, 48)
        self.image = self.font.render('B', True, (255, 0, 0))
        self.rect = self.image.get_rect()
