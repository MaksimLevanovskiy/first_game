import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('enemy-small.png')
        self.rect = self.image.get_rect()
        # tocka spawna
        self.x = self.rect.width
        self.y = self.rect.height
        # dvisheniya po X s storoni v storonu
        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.allien_speed*self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
