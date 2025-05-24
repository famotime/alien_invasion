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
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 加载开始/结束图片
    start_image = pygame.image.load('./images/start.jpeg')
    start_image = pygame.transform.scale(start_image, (ai_settings.screen_width, ai_settings.screen_height))

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)
    sb = Scoreboard(ai_settings, screen, stats, ship)

    # 确保在游戏开始时正确初始化炸弹数量
    stats.bombs_left = ai_settings.bombs_per_ship * ai_settings.ship_limit
    sb.prep_bombs()

    # 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    player_bullets = Group() # Renamed from bullets
    enemy_bullets = Group() # New group for enemy bullets
    aliens = Group()
    explosions = Group()
    powerups = Group() # New group for power-ups

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:
        # Pass relevant groups to check_events, update_bullets, update_aliens, and update_screen
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, player_bullets, enemy_bullets, explosions, powerups)

        if stats.game_active:
            ship.update()
            # Player bullets
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups)
            # Enemy bullets
            gf.update_enemy_bullets(ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, explosions, powerups)
            # Aliens (including firing)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, explosions, powerups)
            # Update powerups separately
            gf.update_powerups(ai_settings, screen, stats, ship, powerups, sb) 
            explosions.update()

        # Pass all relevant groups to update_screen
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, play_button, explosions, powerups, start_image)


run_game()
