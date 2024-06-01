import pygame


class ShowText:
    """一个用于显示文本的类"""

    def __init__(
            self,
            ai_game,
            text_color,
            font_name,
            font_size,
            msg,
            num,
            antialias,
            x_d,
            y_d,
            x_p,
            y_p

    ):
        """初始化"""

        # 设置字体
        self.text_color = text_color
        self.font = pygame.font.SysFont(font_name, font_size)

        # 设置值
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.msg = msg
        self.antialias = antialias
        self.ai_game = ai_game
        self.settings = ai_game.settings

        # 获得坐标
        self.x_p = x_p
        self.y_p = y_p
        self.x_d = x_d
        self.y_d = y_d

        # 是否是数字
        self.num = num

        # 准备打印
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """准备打印"""

        # 重新读取设置
        self.settings = self.ai_game.settings

        # 获取字符串
        if self.num:
            msg_str = f'{int(msg):,}'
        else:
            msg_str = msg

        # 创建图像
        self.msg_image = self.font.render(
            msg_str,
            self.antialias,
            self.text_color,
            self.settings['bg_color']
        )
        self.msg_rect = self.msg_image.get_rect()

    def show_msg(self):
        """展示文字"""

        # 设置位置
        if self.x_d == 'right':
            self.msg_rect.right = self.screen.get_width() - self.x_p
        elif self.x_d == 'left':
            self.msg_rect.left = self.x_p

        if self.y_d == 'top':
            self.msg_rect.top = self.y_p
        elif self.y_d == 'bottom':
            self.msg_rect.bottom = self.screen.get_height() - self.y_p

        # 显示文字
        self.screen.blit(self.msg_image, self.msg_rect)
