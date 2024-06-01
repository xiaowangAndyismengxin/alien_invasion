from pathlib import Path
from json import loads


class IncreaseSpeed:
    """更新游戏"""

    def __init__(self, ai_game):
        """初始化"""

        # 加载设置
        path = Path('settings.json')
        self.settings = loads(path.read_text())
        self.ai_game = ai_game

        # 存储要加速的设置项
        self.to_updated_settings = [
            'alien_speed'
        ]

        # 设置加速速度
        self.speed_up = self.settings['speedup_scale']

    def increase_speed(self):
        """加速!!!"""

        # 重新读取数据
        self.settings = self.ai_game.settings

        # 加速
        for k in self.to_updated_settings:
            self.settings[k] *= self.speed_up

        # 分数是特殊的
        self.settings['alien_points'] *= (
            self.settings['alien_points_speedup'])
