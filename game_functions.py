import sys
import time
import pygame
import random # Added for power-up spawning
from bullet import Bullet, BulletR, BulletL
from alien import NormalAlien, FastAlien, TankAlien, ShooterAlien, BaseAlien # Updated Alien imports
from explosion import Explosion, SimpleShipExplosion, BombExplosion
# Import PowerUp classes
from powerup import PowerUp, ShieldPowerUp, RapidFirePowerUp, MultiShotPowerUp, SpeedBoostPowerUp


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, player_bullets, enemy_bullets, explosions, powerups):
    """响应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, explosions, powerups)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, player_bullets, enemy_bullets, powerups, mouse_x, mouse_y)


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, explosions, powerups):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 空格键开火
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, player_bullets) # player_bullets
    # q键关闭程序
    elif event.key == pygame.K_q:
        sys.exit()
    # For testing power-up spawning, remove later
    # elif event.key == pygame.K_p: 
    #     _try_spawn_powerup(ai_settings, screen, ship, powerups)
    elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
        fire_bomb(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions) # player_bullets
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


def fire_bullet(ai_settings, screen, ship, player_bullets): # ai_settings is ship.settings
    """如果还没有达到限制，就发射一颗子弹"""
    # Determine bullets_allowed based on rapid_fire
    current_bullets_allowed = ai_settings.bullets_allowed
    if ship.rapid_fire_active:
        # Assuming a setting like 'bullets_allowed_rapid_fire' exists or we just allow more
        current_bullets_allowed = getattr(ai_settings, 'bullets_allowed_rapid_fire', ai_settings.bullets_allowed * 2)

    if len(player_bullets) < current_bullets_allowed:
        if ship.multi_shot_active:
            # Multi-shot: Create three bullets - center, left, right
            # Center bullet (standard)
            bullet_center = Bullet(ai_settings, screen, ship)
            
            # Left bullet
            bullet_left = Bullet(ai_settings, screen, ship)
            bullet_left.rect.x -= getattr(ai_settings, 'multi_shot_spread_amount', 20) # Spread amount from settings
            # Optionally, give it a slight angle if Bullet class supports dx/dy or angle
            # For simplicity, just offsetting x for now.
            # If Bullet has dx, dy: bullet_left.dx = -0.5 

            # Right bullet
            bullet_right = Bullet(ai_settings, screen, ship)
            bullet_right.rect.x += getattr(ai_settings, 'multi_shot_spread_amount', 20) # Spread amount from settings
            # If Bullet has dx, dy: bullet_right.dx = 0.5

            player_bullets.add(bullet_center, bullet_left, bullet_right)
            # Play sound once for the volley
            sound = pygame.mixer.Sound(bullet_center.sound)
            sound.play()
        else:
            # Standard single bullet
            new_bullet = Bullet(ai_settings, screen, ship)
            sound = pygame.mixer.Sound(new_bullet.sound)
            sound.play()
            player_bullets.add(new_bullet)


def fire_bomb(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions): # player_bullets
    if stats.bombs_left > 0:
        stats.bombs_left -= 1
        sb.prep_bombs()

        # 计算得分 (using a placeholder for enemy_bullets in update_screen call if needed)
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
        # Assuming powerups is available here or passed if needed for screen update
        # Passing None for enemy_bullets for now, will be updated if this function needs it
        while pygame.time.get_ticks() - start_time < 300:  # 等待300毫秒
            explosions.update()
            update_screen(ai_settings, screen, stats, sb, ship, aliens, player_bullets, None, explosions, powerups, None) 
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
            update_screen(ai_settings, screen, stats, sb, ship, aliens, player_bullets, None, explosions, powerups, None)
            pygame.display.flip()

        # 创建新的外星人群
        create_fleet(ai_settings, screen, ship, aliens)

        # 更新屏幕
        update_screen(ai_settings, screen, stats, sb, ship, aliens, player_bullets, None, explosions, powerups, None)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, player_bullets, enemy_bullets, powerups, mouse_x, mouse_y):
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
        player_bullets.empty()
        enemy_bullets.empty() # Clear enemy bullets
        powerups.empty() # Clear existing powerups on new game

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, play_button, explosions, powerups, start_image=None):
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
        for bullet in player_bullets.sprites(): # Player bullets
            bullet.draw_bullet()
        
        if enemy_bullets: # Draw enemy bullets
            for bullet in enemy_bullets.sprites():
                bullet.draw_bullet()

        ship.blitme()
        aliens.draw(screen)

        # Draw power-ups
        if powerups: # Check if powerups group exists
            for powerup in powerups.sprites():
                powerup.blitme()

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


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups): # Renamed bullets to player_bullets
    """更新子弹的位置，并删除已飞出窗口的子弹"""
    # 更新子弹的位置
    player_bullets.update()
    # 检查是否有子弹击中了外星人
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups) # player_bullets
    # 删除已飞出窗口的子弹
    for bullet in player_bullets.copy():
        if bullet.rect.bottom <= 0 or bullet.rect.left >= ai_settings.screen_width or bullet.rect.right <= 0:
            player_bullets.remove(bullet)
    # print(len(player_bullets))


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups): # Renamed bullets to player_bullets
    """响应子弹和外星人的碰撞"""
    # 子弹摧毁，外星人不自动摧毁
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    
    if collisions:
        for aliens_hit_by_bullet in collisions.values(): # List of aliens hit by a single bullet
            for alien_hit in aliens_hit_by_bullet:
                destroyed = alien_hit.take_damage(1) # Assume player bullets do 1 damage
                if destroyed:
                    # 创建爆炸效果
                    explosion = Explosion(alien_hit.rect.center, "sm")
                    explosions.add(explosion)
                    # 播放爆炸声音
                    sound = pygame.mixer.Sound(alien_hit.sound)
                    sound.play()
                    
                    # 增加得分
                    stats.score += alien_hit.points # Use points from the specific alien instance
                    sb.prep_score()
                    
                    # Chance to spawn a power-up when an alien is killed
                    if random.random() < ai_settings.powerup_drop_chance_on_kill:
                        _try_spawn_powerup(ai_settings, screen, ship, powerups, alien_hit.rect.center)
                    
                    alien_hit.kill() # Remove the alien from all groups
                # If not destroyed, alien just took damage, bullet is already gone.
        
        # 检查是否打破了最高分 (moved outside the inner loop, check once after all collisions)
        check_high_score(stats, sb)

    # 如果全部外星人被消灭，则删除现有子弹并新建一群外星人，并提高等级
    if len(aliens) == 0:
        player_bullets.empty() # player_bullets
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
    """创建一个随机类型的外星人，并将其放在当前行"""
    # Determine which alien type to spawn
    alien_types = list(ai_settings.alien_spawn_chances.keys())
    probabilities = list(ai_settings.alien_spawn_chances.values())
    chosen_type_str = random.choices(alien_types, probabilities, k=1)[0]

    if chosen_type_str == 'normal':
        alien = NormalAlien(ai_settings, screen)
    elif chosen_type_str == 'fast':
        alien = FastAlien(ai_settings, screen)
    elif chosen_type_str == 'tank':
        alien = TankAlien(ai_settings, screen)
    elif chosen_type_str == 'shooter':
        alien = ShooterAlien(ai_settings, screen)
    else: # Default to NormalAlien if something goes wrong
        alien = NormalAlien(ai_settings, screen)
    
    # Alien width and height are determined by the specific alien type's image
    alien_width = alien.rect.width
    alien.x = alien_width + alien_width * 2 * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 使用NormalAlien获取基础尺寸信息，不加入外星人群组
    # This is a simplification; if alien types have vastly different sizes,
    # fleet layout might need more complex logic or use BaseAlien's default image size.
    temp_alien = NormalAlien(ai_settings, screen) 
    number_aliens_x = get_number_aliens_x(ai_settings, temp_alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, temp_alien.rect.height)

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


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, explosions, powerups):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置，包括射手射击"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update() # Calls update on each alien, including ShooterAlien's frames_since_last_shot increment

    for alien in aliens.sprites():
        if isinstance(alien, ShooterAlien):
            alien.try_fire(enemy_bullets, ai_settings, screen) # Pass necessary groups/settings

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens) or stats.score < 0:
        # Pass player_bullets to ship_hit, as it's the convention
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups)
        if stats.score < 0:
            stats.score = 0
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups): # Renamed bullets to player_bullets
    """响应飞船被外星人撞到或被敌方子弹击中"""
    if ship.shield_active:
        print("Shield blocked hit!")
        # Optionally, consume the shield on hit or let it run its duration
        # To consume on hit:
        # ship.shield_active = False
        # ship.powerup_timers.pop('shield', None) 
        # ship.shield_image = None # remove visual
        return # Ship is protected

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

        # 重绘屏幕，显示爆炸效果 (Passing None for enemy_bullets for now)
        update_screen(ai_settings, screen, stats, sb, ship, aliens, player_bullets, None, None, explosions, powerups)
        pygame.display.flip()

        # 等待爆炸效果结束
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 1000:  # 等待1秒
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            explosions.update()
            update_screen(ai_settings, screen, stats, sb, ship, aliens, player_bullets, None, None, explosions, powerups)
            pygame.display.flip()

        # 清空外星人和子弹列表
        aliens.empty()
        player_bullets.empty()
        # enemy_bullets group should also be cleared here if it exists and needs to be
        # However, enemy bullets are usually cleared on new game (check_play_button)
        # or handled by update_enemy_bullets

        # powerups.empty() # Optionally clear powerups on ship hit, or let them persist

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


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups): # Renamed bullets to player_bullets
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 创建爆炸效果
            explosion = Explosion(alien.rect.midbottom, "lg")
            explosions.add(explosion)
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups) # player_bullets
            break


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        stats.save_high_score()
# --- Enemy Bullet Functions ---

def update_enemy_bullets(ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, explosions, powerups):
    """Update position of enemy bullets and get rid of old bullets and check collisions."""
    enemy_bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in enemy_bullets.copy():
        if bullet.rect.top >= screen.get_rect().bottom:
            bullet.kill() # Use kill() to remove from all groups it might be in

    check_enemy_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, explosions, powerups)

def check_enemy_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, player_bullets, enemy_bullets, explosions, powerups):
    """Respond to enemy bullet-ship collisions."""
    # Check for any bullets that have hit the ship.
    # The True argument removes the bullet from the enemy_bullets group.
    # Using collide_rect_ratio for potentially more forgiving hit detection.
    collided_bullets = pygame.sprite.spritecollide(ship, enemy_bullets, True, pygame.sprite.collide_rect_ratio(0.7))

    if collided_bullets:
        # For each bullet that hit, a ship_hit is triggered.
        # ship_hit will handle lives, game state, etc.
        # player_bullets is passed as it's part of ship_hit's signature from other calls
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, player_bullets, explosions, powerups)


# --- Power-up specific functions ---

def _try_spawn_powerup(ai_settings, screen, ship, powerups, position=None):
    """Try to spawn a power-up based on chance."""
    # This function can be called periodically or on specific events (e.g., alien kill)
    # For periodic spawning, it would be called from update_powerups.
    # For event-based (like alien kill), it's called from check_bullet_alien_collisions.
    # The 'position' argument allows spawning at a specific location (e.g., where an alien died).

    # If position is None, it means it's a random timed spawn.
    # We'll assume a setting like 'powerup_spawn_chance_time' for periodic spawning.
    # This function can be expanded to differentiate between timed and drop spawns if needed.

    powerup_types = [ShieldPowerUp, RapidFirePowerUp, MultiShotPowerUp, SpeedBoostPowerUp]
    chosen_powerup_class = random.choice(powerup_types)

    # Create an instance of the chosen power-up.
    # The PowerUp class expects 'ai_game' which contains screen, settings etc.
    # We are passing individual components here based on existing function signatures.
    # This might need adjustment if powerup classes strictly expect an 'ai_game' object.
    # For now, we construct a temporary 'mock_ai_game' object or pass params directly.
    # Let's assume powerup classes can take screen and settings if ai_game is not directly passed.
    
    # Create a simple object that mimics the ai_game structure for PowerUp class
    class MockAiGame:
        def __init__(self, screen_obj, settings_obj, ship_obj):
            self.screen = screen_obj
            self.settings = settings_obj
            self.ship = ship_obj # ship might be needed by some powerups later

    mock_ai_game = MockAiGame(screen, ai_settings, ship)
    new_powerup = chosen_powerup_class(mock_ai_game)

    if position:
        new_powerup.rect.center = position
        new_powerup.y = float(new_powerup.rect.y) # Update float y if spawned at specific y

    powerups.add(new_powerup)
    # print(f"Spawned {new_powerup.powerup_type}")


def update_powerups(ai_settings, screen, stats, ship, powerups, sb): # Added sb for potential future use
    """Update power-ups, handle spawning, and check for collisions."""
    # Chance to spawn a power-up periodically
    if random.random() < getattr(ai_settings, 'powerup_spawn_chance_time', 0.0005): # Example: 0.05% chance per frame
         _try_spawn_powerup(ai_settings, screen, ship, powerups)

    powerups.update() # Calls the update() method of each power-up in the group

    # Remove power-ups that have fallen off the screen
    for powerup in powerups.copy():
        if powerup.rect.top > screen.get_rect().bottom:
            powerup.kill() # Use kill() to remove from all groups

    # Check for collisions between ship and power-ups
    check_ship_powerup_collisions(ai_settings, stats, ship, powerups, sb)


def check_ship_powerup_collisions(ai_settings, stats, ship, powerups, sb): # Added sb
    """Respond to ship-powerup collisions."""
    # Using spritecollideany to get the first powerup collided with.
    # For removing the specific powerup, we'll use groupcollide with dokill=True for powerups.
    collided_powerups = pygame.sprite.spritecollide(ship, powerups, True, pygame.sprite.collide_rect_ratio(0.7))

    for powerup in collided_powerups:
        print(f"Player collected: {powerup.powerup_type}")
        # Instead of powerup.activate(), call ship's method
        ship.activate_powerup(powerup.powerup_type, powerup.duration) # Pass duration from powerup object
        
        # Play a sound for collecting power-up (optional)
        # if hasattr(ai_settings, 'powerup_collect_sound'):
        #     collect_sound = pygame.mixer.Sound(ai_settings.powerup_collect_sound)
        #     collect_sound.play()

        # Potentially give score for collecting power-ups (optional)
        # stats.score += getattr(ai_settings, 'powerup_score_value', 50)
        # sb.prep_score()
        # check_high_score(stats, sb)
        
        # powerup.activate() # This line is now replaced by ship.activate_powerup(...)
        # Actual effect logic will be in ship.py or by PowerUp subclasses modifying ship/settings.
        # For now, the PowerUp.activate() method just prints a message.
        # The duration and specific effects will be handled when ship.py is modified.
    
    # The collided powerup is automatically removed due to dokill=True in spritecollide.
    # If we used spritecollideany, we would need:
    # if collided_powerup:
    #     print(f"Player collected: {collided_powerup.powerup_type}")
    #     # ship.activate_powerup(collided_powerup.powerup_type, collided_powerup.duration) # This will be in ship.py
    #     collided_powerup.kill() # Remove the power-up from all groups