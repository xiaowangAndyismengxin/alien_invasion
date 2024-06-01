import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """创建背景星星"""

    def __init__(self):
        """初始化"""

        super().__init__()

        # 加载星星的图像
        self.image = pygame.image.load('material/bg_star.bmp')
        self.rect = self.image.get_rect()

        # 生成星星
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
