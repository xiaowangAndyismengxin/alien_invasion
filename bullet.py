import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """一个子弹类"""

    def __init__(self, game):
        """初始化值"""

        super().__init__()

        # 加载值
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings['bullet']['color']

        # 创建矩形
        self.rect = pygame.Rect(0, 0,
                                self.settings['bullet']['size'][0],
                                self.settings['bullet']['size'][1])

        # 设置位置
        self.rect.midtop = game.ship.rect.midtop

        # 获取精确位置
        self.y = float(self.rect.y)

    def update(self):
        """子弹飞行"""

        self.y -= self.settings['bullet']['speed']
        self.rect.y = self.y

    def draw_bullet(self):
        """画子弹"""

        # 画子弹
        pygame.draw.rect(self.screen, self.color, self.rect)
