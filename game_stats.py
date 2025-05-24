import json

HIGH_SCORE_FILE = 'highscore.json'

class GameStats():
    """跟踪游戏统计信息"""
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """加载最高分"""
        try:
            with open(HIGH_SCORE_FILE) as f:
                high_score = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
        else:
            return high_score

    def save_high_score(self):
        """保存最高分"""
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                json.dump(self.high_score, f)
        except IOError:
            print(f"Error: Could not save high score to {HIGH_SCORE_FILE}")

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit  # 不再加1
        self.score = 0
        self.level = 1
        self.bombs_left = self.ai_settings.bombs_per_ship * self.ships_left  # 总炸弹数量
