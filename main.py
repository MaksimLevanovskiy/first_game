import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from Button import Button
from ship import Ship
from bullet import Bullet
from allien import Enemy
from scoreboard import Score


class Alien:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)
        self.background = pygame.image.load('Space Background.png')
        self.background_rect = self.background.get_rect()

        self.menu_background = pygame.image.load('space.jpg')
        self.menu_rect = self.menu_background.get_rect()

        self.ship = Ship(self)
        self.gamestats = GameStats(self)
        self.play_button = Button(self, 'Play')
        self.end_button = Button(self, 'Quit')
        self.score = Score(self)
        self.clock = pygame.time.Clock()

        self.running = True

        self._create_fleet()

    def run_game(self):

        while self.running:
            self._check_event()
            if self.gamestats.game_mode:
                self.ship.update()
                self.bullets.update()
                self._delete_bullet()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(self.settings.FPS)
    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gamestats._save_game()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            self.gamestats._save_game()
            sys.exit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _update_screen(self):

        if not self.gamestats.game_mode:
            self.screen.blit(self.menu_background, self.menu_rect)
            self.play_button.draw_button()

        else:
            self.screen.blit(self.background, self.background_rect)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.aliens.draw(self.screen)
            self.score.show_score()
            self.ship.blitme()

        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _delete_bullet(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for alien in collisions.values():
                self.gamestats.score += self.settings.allien_points * len(alien)
            self.score.prep_score()
            self.score.pre_high_score()
            self.score.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.gamestats.game_level += 1
            self.score.pre_level()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _create_fleet(self):
        alien = Enemy(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        avalible_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        avalible_space_x = self.settings.screen_width - (2 * alien_width)

        numbers_rows = avalible_space_y // (2 * alien_width)
        numbers_of_aliens = avalible_space_x // (alien_width * 2)

        for alien_numb in range(numbers_of_aliens):
            for alien_rows in range(numbers_rows):
                alien = Enemy(self)
                alien.x = alien_width + 2 * alien_width * alien_numb
                alien.rect.x = alien.x
                alien.rect.y = alien.rect.height + 2 * alien.rect.height * alien_rows
                self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.gamestats.ship_left > 0:
            self.gamestats.ship_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.score.prep_ships()
            sleep(1)
        else:
            self.gamestats.game_mode = False
            pygame.mouse.set_visible(True)

    def _check_alliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.gamestats.game_mode:
            self.settings.initialize_dynamic_settings()
            self.gamestats.reset_stats()
            self.gamestats.game_mode = True
            self.score.prep_score()
            self.score.prep_ships()
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)




if __name__ == '__main__':
    ai = Alien()
    ai.run_game()
