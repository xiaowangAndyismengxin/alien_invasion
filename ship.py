import pygame


class Ship:
    """管理Ship行为"""

    def __init__(self, ai_game):
        """初始化资源"""

        # 获取游戏信息
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.ai_game = ai_game

        # 加载图像
        self.image = pygame.image.load('material/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        # 鼠标捕获
        pygame.event.set_grab(True)

        # 获取飞船位置
        self.x = float(self.rect.x)

    def move_ship(self):
        """更新位置"""

        # 检测鼠标位置
        pos = pygame.mouse.get_pos()

        # 判断位置受否合法
        if pos[0] > self.screen.get_width() - self.rect.width:

            pygame.mouse.set_pos(self.screen.get_width() -
                                 self.rect.width,
                                 pos[1])
            pos = pygame.mouse.get_pos()

        self.x = pos[0]

        # 应用位置
        self.rect.x = self.x

    def center_ship(self):
        """回正飞船"""

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        pygame.mouse.set_pos((self.x, 24))

    def blit(self):
        """显示飞船"""

        self.screen.blit(self.image, self.rect)
