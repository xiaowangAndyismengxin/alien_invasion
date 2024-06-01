"""
这是游戏的主程序
作者：xiaowangAndy
祝您游戏愉快
"""

import pygame
import sys
import pathlib
import json
import random
import time
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from explosion import Explosion
from button import Button
from increase_speed_settings import IncreaseSpeed
from scoreboard import Scoreboard


class AlienInvasion:
    """用于管理游戏大部分行为"""

    def __init__(self):
        """初始化游戏资源"""

        # 导入settingsd设置
        setting_path = pathlib.Path('settings.json')
        self.settings = json.loads(
            setting_path.read_text()
        )

        # 导入最高分
        self.top_score_path = pathlib.Path('top_score.json')
        self.top_score = json.loads(
            self.top_score_path.read_text()
        )

        # 初始化游戏界面
        pygame.init()

        # 设置屏幕
        self.screen = pygame.display.set_mode(self.settings['full_resolution'],
                                              pygame.FULLSCREEN)
        pygame.display.set_caption('alien_invasion')

        # 设置时钟
        self.clock = pygame.time.Clock()

        # 读取行为
        self.ship = Ship(self)
        self.alien = Alien(self)
        self.stats = GameStats(self)
        self.increase_speed = IncreaseSpeed(self)
        self.sb = Scoreboard(self)

        # 初始化值
        self.ship.moving_right = False
        self.ship.moving_left = False
        self.firing = False
        self.alien_later = 0
        self.fire_time = 0
        pygame.mouse.set_visible(True)
        self.game_active = False
        self.stop_msg = 'Play'
        self.hit_aliens = 0

        # 设置组
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bg_stars = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        # 创建
        self._create_fleet()
        self._create_stars()

        # 音乐
        pygame.mixer.music.load('sounds/bg_music.mp3')
        pygame.mixer.music.set_volume(1)

        self.bullet_sound = pygame.mixer.Sound('sounds/bullet.mp3')
        self.bullet_sound.set_volume(0.4)

        self.alien_explosion = pygame.mixer.Sound('sounds/explosion.wav')

        self.button_down_sound = pygame.mixer.Sound('sounds/button_down.mp3')

        self.defeat_sound = pygame.mixer.Sound('sounds/defeat.mp3')

    def run_game(self):
        """游戏主程序"""

        while True:
            self._check_event()

            # 判断游戏是否在活动状态
            if self.game_active:
                self._moving_ship()
                self._moving_alien()
                self._fire()
                self._update_bullets()

            self._update_screen()
            # 更新屏幕
            self.clock.tick(self.settings['game_fps'])

    def _moving_ship(self):
        """移动飞船"""

        self.ship.move_ship()

    def _check_event(self):
        """侦测按键"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_event_keydown(event)

            elif event.type == pygame.KEYUP:
                self._check_event_keyup(event)

            # 检测鼠标按下
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _update_screen(self):
        """更新屏幕"""

        # 设置背景颜色
        self.screen.fill(self.settings['bg_color'])

        # 画星星
        self.bg_stars.draw(self.screen)

        # 绘制虚线
        pygame.draw.line(
            self.screen,
            (100, 100, 100),
            self.ship.rect.midtop,
            (self.ship.rect.center[0], 0),
            3
        )

        # 显示计分板
        self.sb.prep_score()
        self.sb.show_score()

        # 画子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 画飞船
        self.ship.blit()

        # 画外星人
        self.aliens.draw(self.screen)

        # 画爆炸
        self.explosion_group.draw(self.screen)

        # 更新爆炸
        self.explosion_group.update()

        # 画按钮
        if not self.game_active:
            self.play_button = Button(self, self.stop_msg)
            self.play_button.draw_button()

        # 更新
        pygame.display.flip()

    def _check_event_keydown(self, event):
        """处理KEYDOWN事件"""

        if event.key == pygame.K_SPACE:
            self.firing = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_event_keyup(self, event):
        """处理KEYUP事件"""

        if event.key == pygame.K_SPACE:
            self.firing = False

    def _check_play_button(self, mouse_pos):
        """检查点击按钮"""

        # 检查是否点击检查按钮
        if (self.play_button.rect.collidepoint(mouse_pos) and
                not self.game_active):
            self.stats.reset_stats()
            self.game_active = True

            # 清除所有子弹
            self.bullets.empty()
            self.aliens.empty()

            # 创造一个新的战队并重置飞船位置
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

            # 重新加载设置
            self.settings = json.loads(
                pathlib.Path('settings.json').read_text()
            )

            # 重置信息
            self.hit_aliens = 0
            self.alien_later = -self.alien.rect.height
            self.fire_time = 0

            # 播放游戏背景音乐并播放点击音效
            pygame.mixer.music.play(-1)
            self.button_down_sound.play()

    def _fire(self):
        """开火"""

        # 如果要开火
        if self.firing:

            # 在零时发射
            if self.fire_time == 0:

                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
                self.bullet_sound.play()
                self.fire_time += 1

            # 每次加一
            elif self.fire_time < self.settings['bullet']['time']:
                self.fire_time += 1

            # 到时间后归零
            elif self.fire_time >= self.settings['bullet']['time']:
                self.fire_time = 0

        # 在不发射时归零
        else:
            self.fire_time = 0

    def _explosion(self, x, y):
        """爆炸"""

        new_explosion = Explosion(x, y)
        self.explosion_group.add(new_explosion)

    def _update_bullets(self):
        """子弹更新"""

        # 移动
        self.bullets.update()

        # 删除子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 检查碰撞
        self._check_alien_collisions()

    def _create_fleet(self):
        """创建一个外星人战队"""

        # 创建第一个外星人
        alien = Alien(self)

        # 初始化战队
        alien_width, alien_height = alien.rect.size
        current_x = alien_width
        alien_list = []

        # 开启两层循环
        # 第一曾是竖向填充

        # 第二是横向填充
        while current_x <= (self.screen.get_width() - 2 * alien_width):
            self._create_alien(current_x, alien_list)
            # 推进到下一个位置
            current_x += 2 * alien_width

        # 删除多余外星人
        self._del_more_list(alien_list, random.randint(
            1,
            int(self.screen.get_width() / (2 * self.alien.rect.width + 1))
        ))
        self.aliens.add(alien_list)

    def _create_alien(self, x_position, n_list):
        """创建单个外星人"""

        # 创建一个外星人
        new_alien = Alien(self)

        # 更新位置
        new_alien.rect.x = x_position

        # 将外星人加入组
        n_list.append(new_alien)

    def _moving_alien(self):
        """移动外星人"""

        # 计时
        self.aliens.update()
        self.alien_later += self.settings['alien_speed']

        if self.alien_later >= 2 * self.alien.rect.height:
            self._create_fleet()
            self.alien_later = 0

        # 检测碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查外星人是否到底部了
        self._check_aliens_bottom()

    def _ship_hit(self):
        """飞船碰撞"""

        # 在还有飞船时开启碰撞效果
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            # 设置碰撞效果
            y = self.settings['bg_color']
            for i in range(2):
                self.settings['bg_color'] = self.settings['when_ship_hit']
                self._update_screen()
                time.sleep(0.3)
                self.settings['bg_color'] = y
                self._update_screen()
                time.sleep(0.4)
            time.sleep(0.5)

            # 从头再来
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()

        # 游戏失败
        else:

            # 关闭游戏的运行状态
            self.game_active = False

            # 重新让光标可见
            pygame.mouse.set_visible(True)

            # 设置按钮样式
            self.stop_msg = 'Replay'

            # 播放音乐
            pygame.mixer.music.stop()
            self.defeat_sound.play()

            # 检查最高分
            self._check_top_score()

            # 重置等级
            self.stats.level = 1

    def _check_top_score(self):
        if self.top_score < self.stats.score:
            self.top_score = self.stats.score
            top_score = json.dumps(self.top_score)
            self.top_score_path.write_text(
                top_score
            )

    def _check_aliens_bottom(self):
        """检查是否到达底部"""

        # 检测外星人到达底部
        for alien in self.aliens.copy():
            if alien.rect.bottom >= self.screen.get_height():
                self._ship_hit()  # 像飞船被撞一样处理
                break

    def _check_alien_collisions(self):
        """检查外星人碰撞"""

        # 检测与外星人的碰撞
        collisions = pygame.sprite.groupcollide(
            self.aliens, self.bullets, True, True

        )

        # 如果碰撞了
        if collisions:
            # 播放爆炸音频
            self.alien_explosion.play()

            # 将击中的外星人数量加一
            self.hit_aliens += len(collisions)

            # 更新分数
            self.stats.score += (
                    len(collisions) *
                    self.settings['alien_points']
            )

            # 重置分数
            self.sb.prep_score()

            # 更新游戏运行速度
            self._increase_speed()

        # 加载爆炸
        for i in collisions.keys():
            x, y = i.rect.center
            self._explosion(x, y)

    def _increase_speed(self):
        """更新游戏运行速度"""

        # 更新游戏运行速度
        if self.hit_aliens >= self.settings['speedup_aliens']:
            self.increase_speed.increase_speed()

            # 将设置应用
            self.settings = self.increase_speed.settings
            self.stats.level += 1
            self.hit_aliens = 0

    def _create_stars(self):
        """创建星星"""

        star = Star()

        # 定义值
        star_width, star_height = star.rect.size
        current_x, current_y = star_width, star_height

        # 循环放置
        while current_y <= (self.screen.get_height() - star_height):
            while current_x <= (self.screen.get_width() - star_width):
                self._create_star(current_x, current_y)
                current_x += star_width

            # 在一行放置结束后
            # 重置x并递增y
            current_x = star_width
            current_y += star_height

        # 删除星星
        self._del_more(self.bg_stars, self.settings['stars_alwd'])

    def _create_star(self, x, y):
        """加入新的星星"""

        new_start = Star()
        new_start.rect.x = x
        new_start.rect.y = y
        self.bg_stars.add(new_start)

    def _del_more(self, group, count):
        """删除多余"""

        # 设置值
        group_list = list(group)
        group.remove(self._del_more_list(group_list, count))

    def _del_more_list(self, n_list, count):
        """删除多余的列表版本"""

        remove = []

        # 循环删除
        while len(n_list) > count:
            # 更改列表
            i = random.choice(n_list)
            n_list.remove(i)
            remove.append(i)

        return remove


def main():
    """开始游戏"""

    # 开始游戏
    ai_game = AlienInvasion()
    ai_game.run_game()
    return 0


if __name__ == '__main__':
    main()
