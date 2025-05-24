class Settings():
    """存储所有设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 3  # 游戏开始时的飞船数量

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 9

        # 外星人下移速度
        self.fleet_drop_speed = 20

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5

        # 清屏炸弹设置
        self.bombs_per_ship = 3  # 每艘飞船携带的炸弹数量

        # 道具掉落设置
        self.powerup_drop_chance_on_kill = 0.1  # 外星人被击落时掉落道具的概率为10%

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 0.3
        # 1右移，-1左移
        self.fleet_direction = 1

        # 记分
        self.alien_points = 50 # Default points for NormalAlien

        # Alien type specific settings
        self.fast_alien_speed_multiplier = 2.0
        self.tank_alien_health = 3
        self.tank_alien_speed_multiplier = 0.75
        self.shooter_alien_fire_cooldown = 120  # frames

        self.normal_alien_points = 50 # Explicitly defined
        self.fast_alien_points = 70
        self.tank_alien_points = 100
        self.shooter_alien_points = 120
        
        # Probabilities for spawning each alien type
        self.alien_spawn_chances = {
            'normal': 0.60,
            'fast': 0.15,
            'tank': 0.15,
            'shooter': 0.10
        }

        # Enemy bullet settings
        self.enemy_bullet_speed_factor = 1
        self.enemy_bullet_width = 5
        self.enemy_bullet_height = 10
        self.enemy_bullet_color = (255, 50, 50) # Light red
        self.enemy_bullets_allowed = 10


    def increase_speed(self):
        """提高速度设置和外星人点数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
