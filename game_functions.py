import sys
import time
import pygame
from bullet import Bullet, BulletR, BulletL
from alien import Alien
from explosion import Explosion, SimpleShipExplosion, BombExplosion


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, explosions):
    """响应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 空格键开火
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # q键关闭程序
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
        fire_bomb(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
    elif event.key == pygame.K_b and stats.bombs_left > 0:
        # 投放炸弹
        bomb_explosion = BombExplosion(ship.rect.center, (ai_settings.screen_width, ai_settings.screen_height))
        explosions.add(bomb_explosion)
        stats.bombs_left -= 1  # 减少可用炸弹数量
        sb.prep_bombs()  # 更新炸弹图标显示


def check_keyup_events(event, ship):
    """响应松开键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        # 播放声音
        sound = pygame.mixer.Sound(new_bullet.sound)
        sound.play()
        bullets.add(new_bullet)


def fire_bomb(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    if stats.bombs_left > 0:
        stats.bombs_left -= 1
        sb.prep_bombs()

        # 计算得分
        score_increase = len(aliens) * ai_settings.alien_points * 0.5
        stats.score += int(score_increase)
        sb.prep_score()
        check_high_score(stats, sb)

        # 创建炸弹爆炸效果
        bomb_explosion = BombExplosion(ship.rect.center, (ai_settings.screen_width, ai_settings.screen_height))
        explosions.add(bomb_explosion)

        # 播放炸弹爆炸声音
        explosion_sound = pygame.mixer.Sound('sound/bomb_explosion.wav')
        explosion_sound.play()

        # 等待炸弹爆炸效果完成
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 300:  # 等待300毫秒
            explosions.update()
            update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, None, explosions)
            pygame.display.flip()

        # 为每个外星人创建爆炸效果并立即移除外星人
        for alien in aliens.sprites():
            alien_explosion = Explosion(alien.rect.center, "sm")
            explosions.add(alien_explosion)

        # 清空外星人群
        aliens.empty()

        # 等待外星人爆炸效果完成
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 1000:  # 等待1秒
            explosions.update()
            update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, None, explosions)
            pygame.display.flip()

        # 创建新的外星人群
        create_fleet(ai_settings, screen, ship, aliens)

        # 更新屏幕
        update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, None, explosions)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        sb.prep_bombs()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, explosions, start_image=None):
    """更新屏幕上的图像"""
    if not stats.game_active and start_image:
        # 显示开始/结束图片
        screen.blit(start_image, (0, 0))
        play_button.draw_button()

        # 检查鼠标是否悬停在Play按钮上
        mouse_pos = pygame.mouse.get_pos()
        if play_button.is_hovered(mouse_pos):
            draw_instructions(screen, play_button)
    else:
        screen.fill(ai_settings.bg_color)
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)

        # 绘制爆炸效果
        for explosion in explosions:
            explosion.draw(screen)

        # 显示得分
        sb.show_score()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def draw_instructions(screen, play_button):
    """绘制游戏按键说明"""
    font = pygame.font.Font(None, 24)  # 使用默认字体

    instructions = [
        "Space: Fire",
        "Arrow Keys: Move ship left/right",
        "Alt: Drop bomb"
    ]

    # 创建一个半透明的白色背景
    bg_surface = pygame.Surface((300, 100))
    bg_surface.fill((255, 255, 255))
    bg_surface.set_alpha(128)  # 50% 透明度

    # 设置说明文字的位置
    bg_rect = bg_surface.get_rect()
    bg_rect.centerx = screen.get_rect().centerx
    bg_rect.top = play_button.rect.bottom + 20  # Play 按钮下方 20 像素

    # 绘制半透明背景
    screen.blit(bg_surface, bg_rect)

    # 绘制文字
    y_position = bg_rect.top + 10
    for instruction in instructions:
        text = font.render(instruction, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = y_position
        screen.blit(text, text_rect)
        y_position += 30  # 每行之间的间距


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """更新子弹的位置，并删除已飞出窗口的子弹"""
    # 更新子弹的位置
    bullets.update()
    # 检查是否有子弹击中了外星人
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
    # 删除已飞出窗口的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0 or bullet.rect.left >= ai_settings.screen_width or bullet.rect.right <= 0:
            bullets.remove(bullet)
    # print(len(bullets))


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """响应子弹和外星人的碰撞"""
    # 若有碰撞则删除子弹和外星人(groupcollide方法返回字典，键值对分别为重叠的子弹和外星人实例列表，True/False表示是否删除重叠实例)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # 遍历所有被击中的外星人来计算得分（如果一颗子弹集中了多个外星人，则多次记分）
        for aliens_hit in collisions.values():
            for alien in aliens_hit:
                # 创建爆炸效果
                explosion = Explosion(alien.rect.center, "sm")
                explosions.add(explosion)
                # 播放爆炸声音
                sound = pygame.mixer.Sound(alien.sound)
                sound.play()
            stats.score += ai_settings.alien_points * len(aliens_hit)
            sb.prep_score()
        # 检查是否打破了最高分
        check_high_score(stats, sb)
    # 如果全部外星人被消灭，则删除现有子弹并新建一群外星人，并提高等级
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        stats.level += 1
        sb.prep_level()


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人，间距为外星人宽度"""
    available_space_x = ai_settings.screen_width - alien_width * 2
    number_aliens_x = int(available_space_x / (alien_width * 2))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人，并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + alien_width * 2 * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少外星人
    alien = Alien(ai_settings, screen)  # 创建一个外星人来获取宽度信息，不加入外星人群组
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    # 计算可容纳多少行外星人
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens) or stats.score < 0:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
        if stats.score < 0:
            stats.score = 0
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """响应飞船被外星人撞到"""
    if stats.ships_left > 1:
        # 创建简单的飞船爆炸效果
        explosion = SimpleShipExplosion(ship.rect.center)
        explosions.add(explosion)

        # 播放飞船爆炸声音
        explosion_sound = pygame.mixer.Sound('sound/me_down.wav')
        explosion_sound.play()

        # 飞船数量减1，并更新显示数量
        stats.ships_left -= 1
        stats.bombs_left = ai_settings.bombs_per_ship  # 重置炸弹数量为每艘飞船的初始数量
        sb.prep_ships()
        sb.prep_bombs()

        # 将飞船隐藏
        ship.rect.center = (-100, -100)

        # 重绘屏幕，显示爆炸效果
        update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, None, explosions)
        pygame.display.flip()

        # 等待爆炸效果结束
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 1000:  # 等待1秒
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            explosions.update()
            update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, None, explosions)
            pygame.display.flip()

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新外星人
        create_fleet(ai_settings, screen, ship, aliens)
        # 将飞船放到屏幕底端中央
        ship.rect.center = (screen.get_rect().centerx, screen.get_rect().bottom - ship.rect.height / 2)
        ship.center_ship()

        # 重置飞船的炸弹数量
        ship.bombs = ai_settings.bombs_per_ship
        sb.prep_bombs()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 创建爆炸效果
            explosion = Explosion(alien.rect.midbottom, "lg")
            explosions.add(explosion)
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
            break


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()