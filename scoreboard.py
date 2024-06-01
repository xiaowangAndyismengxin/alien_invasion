import json
from pathlib import Path
from show_text import ShowText


class Scoreboard:
    """一个用于显示分数的类"""

    def __init__(self, ai_game):
        """初始化"""

        # 设置值
        self.ai_game = ai_game
        self.score = ai_game.stats.score

        # 创建实例
        self.show_current_score = ShowText(
            ai_game,
            (255, 255, 255),
            None,
            30,
            self.score,
            True,
            True,
            'right',
            'top',
            20,
            10
        )

        # 最高分
        self.path = Path('top_score.json')
        self.top_score = json.loads(
            self.path.read_text()
        )
        self.show_top_score_msg = ShowText(
            ai_game,
            (255, 255, 255),
            None,
            30,
            'hi',
            False,
            True,
            'left',
            'top',
            20,
            10
        )

        self.show_top_score_num = ShowText(
            ai_game,
            (255, 255, 255),
            None,
            30,
            self.top_score,
            True,
            True,
            'left',
            'top',
            self.show_top_score_msg.msg_rect.width + 30,
            10
        )

        self.show_level_msg = ShowText(
            ai_game,
            (255, 255, 255),
            None,
            30,
            'level',
            False,
            True,
            'left',
            'top',
            20,
            30
        )

        self.show_level_num = ShowText(
            ai_game,
            (255, 255, 255),
            None,
            30,
            self.ai_game.stats.level,
            True,
            True,
            'left',
            'top',
            self.show_level_msg.msg_rect.width + 30,
            30
        )

        self.show_left_ships_msg = ShowText(
            ai_game,
            (255, 255, 255),
            None,
            30,
            'ships left',
            False,
            True,
            'left',
            'top',
            20,
            50
        )

        self.show_left_ships_num = ShowText(
            ai_game,
            (255, 255, 255),
            None,
            30,
            self.ai_game.stats.ships_left,
            True,
            True,
            'left',
            'top',
            self.show_left_ships_msg.msg_rect.width + 30,
            50
        )

    def prep_score(self):
        """准备打印"""

        # 获取最新分数
        self.score = self.ai_game.stats.score
        self.top_score = json.loads(
            self.path.read_text()
        )

        # 准备分数
        self.show_current_score.prep_msg(self.score)

        # 准备最高分
        self.show_top_score_msg.prep_msg('hi')
        self.show_top_score_num.prep_msg(self.top_score)

        # 准备等级
        self.show_level_msg.prep_msg('level')
        self.show_level_num.prep_msg(self.ai_game.stats.level)

        # 显示剩余飞船
        self.show_left_ships_msg.prep_msg('ships left')
        self.show_left_ships_num.prep_msg(self.ai_game.stats.ships_left)

    def show_score(self):
        """显示分数"""

        # 显示分数
        self.show_current_score.show_msg()
        self.show_top_score_msg.show_msg()
        self.show_top_score_num.show_msg()
        self.show_level_msg.show_msg()
        self.show_level_num.show_msg()
        self.show_left_ships_msg.show_msg()
        self.show_left_ships_num.show_msg()
