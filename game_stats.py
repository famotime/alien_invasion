class GameStats():
    """跟踪游戏统计信息"""
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit  # 不再加1
        self.score = 0
        self.level = 1
        self.bombs_left = self.ai_settings.bombs_per_ship * self.ships_left  # 总炸弹数量
