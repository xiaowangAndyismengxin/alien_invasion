import pygame


class Explosion(pygame.sprite.Sprite):
    """
    Explosion 类继承自 pygame.sprite.Sprite，用于创建和管理爆炸动画效果。
    """

    def __init__(self, x, y):
        """
        初始化方法设置爆炸的起始位置，并加载爆炸的各个阶段的图像。
        :param x: 爆炸的 x 坐标
        :param y: 爆炸的 y 坐标
        """

        # 调用父类(pygame.sprite.Sprite)的初始化方法
        pygame.sprite.Sprite.__init__(self)

        # 初始化存储爆炸帧的列表
        self.images = []

        # 循环加载爆炸的每个阶段的图片，并缩放到指定大小（100x100像素）
        for num in range(1, 6):
            img = pygame.image.load(f"explosion/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)

        # 设置当前显示的爆炸帧索引
        self.index = 0

        # 设置当前爆炸帧的图像
        self.image = self.images[self.index]

        # 获取当前图像的矩形区域，并设置其中心点为传入的坐标
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # 初始化计数器，用于控制动画的播放
        self.counter = 0

    def update(self):
        """
        更新方法用于控制爆炸动画的播放。
        爆炸速度由 explosion_speed 变量控制。
        """

        explosion_speed = 4

        # 更新爆炸动画
        self.counter += 1

        # 判断是否需要更新到下一帧
        if (self.counter >= explosion_speed and
                self.index < len(self.images) - 1):

            self.counter = 0
            self.index += 1

            # 更新当前帧图像
            self.image = self.images[self.index]

        # 如果动画完成，调用 kill() 方法销毁爆炸实例
        if (self.index >= len(self.images) - 1 and
                self.counter >= explosion_speed):
            self.kill()
