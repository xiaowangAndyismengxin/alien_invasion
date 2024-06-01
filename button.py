import pygame

class Button:
    """一个按钮类，用于创建和绘制按钮"""

    def __init__(self, ai_game, msg):
        """初始化按钮实例，设置属性并准备消息文本"""

        # 引用传入的游戏屏幕对象
        self.screen = ai_game.screen
        # 获取屏幕的矩形对象，用于获取屏幕尺寸
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的宽度和高度
        self.width, self.height = 800, 200
        # 设置按钮的颜色
        self.button_color = (0, 0, 135)  # RGB颜色值
        # 设置文本的颜色
        self.text_color = (255, 255, 255)  # RGB颜色值

        # 设置字体（这里使用了一个名为'vinque'的自定义字体）
        self.font = pygame.font.SysFont('vinque', 100)

        # 创建一个矩形对象表示按钮的位置和大小
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 将按钮放置在屏幕中央
        self.rect.center = self.screen.get_rect().center

        # 准备消息文本，这个方法会在下面定义
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """渲染文本并准备将其显示在按钮上"""

        # 使用字体对象和消息创建一个图像
        self.msg_image = self.font.render(
            msg,
            True,  # 如果True，抗锯齿；如果False，不抗锯齿
            self.text_color,  # 文本颜色
            self.button_color  # 文本背景颜色
        )
        # 获取文本图像的矩形对象，用于绘制
        self.msg_image_rect = self.msg_image.get_rect()
        # 将文本图像放置在按钮的中心
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """在屏幕上绘制按钮"""

        # 用按钮颜色填充矩形区域，创建按钮的背景
        self.screen.fill(self.button_color, self.rect)
        # 将文本图像绘制到屏幕上的按钮位置
        self.screen.blit(self.msg_image, self.msg_image_rect)
