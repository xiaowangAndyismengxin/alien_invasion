import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""

        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('material/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = -self.rect.height

        # Store the alien's exact horizontal position.
        self.y = float(self.rect.y)

    def update(self):
        """向下移动外星人"""

        self.settings = self.ai_game.settings
        self.y += self.settings['alien_speed']
        self.rect.y = self.y
