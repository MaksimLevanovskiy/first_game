import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        """Загружаем картинку корабля"""
        self.image = pygame.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        """тригеры для отпускания клавиши"""
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        """настройки корабля (скорость и тд.)"""
        self.set_ship = ai_game.settings
        self.stay = True
        self.anim_count = 0
        self.stayHere = [pygame.image.load('shipAnim1.png'),pygame.image.load('shipAnim2.png'),pygame.image.load('shipAnim3.png')]

        """Оси движения в данный момент 2 по x и по y"""
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    """Метод обновления экрана"""

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    """проверяет условия тригера и бортов и при True перемещает корабль"""

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.set_ship.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.set_ship.ship_speed

        if self.moving_up and self.rect.y > 0:
            self.y -= self.set_ship.ship_speed

        if self.moving_down and self.rect.y < 675:
            self.y += self.set_ship.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


