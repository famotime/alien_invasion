import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    pygame.mixer.init()  # 初始化音频系统
    ai_settings = Settings()  # 创建一个Settings实例
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))     # 参数为元组
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)
    sb = Scoreboard(ai_settings, screen, stats, ship)

    # 确保在游戏开始时正确初始化炸弹数量
    stats.bombs_left = ai_settings.bombs_per_ship * ai_settings.ship_limit
    sb.prep_bombs()

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建外星人群
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建一个用于存储爆炸效果的编组
    explosions = Group()

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, explosions)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
            explosions.update()

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, explosions)


run_game()
