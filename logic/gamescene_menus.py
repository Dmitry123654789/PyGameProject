import pygame

from logic.seting import screen
from data.languages import english, russian
import data.globals


class Button(pygame.sprite.Sprite):  # Класс кнопки для меню уровней
    def __init__(self, pos_x: float, pos_y: float, text: str, surface: pygame.Surface):
        super().__init__()
        if data.globals.LANGUAGE:
            lang = russian.rus
        else:
            lang = english.eng
        font = pygame.font.Font('data/font.otf', 30)
        self.button = pygame.Surface((surface.get_width() // 1.3, surface.get_height() // 3), pygame.SRCALPHA)
        pygame.draw.rect(self.button, (60, 60, 60), self.button.get_rect(), 0, 20)
        text_surf = font.render(lang[text], False, 'White')
        self.button.blit(text_surf, (self.button.get_width() // 2 - text_surf.get_width() // 2,
                                     self.button.get_height() // 2 - text_surf.get_height() // 2))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.button.get_rect().move(pos_x, pos_y)

    def draw(self, surface):  # Отрисовывает кнопку на поверхности
        surface.blit(self.button, self.rect)


class Pause:  # Меню паузы
    def __init__(self):
        self.screen2 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
        self.button_continue = None
        self.button_map = None

    def draw(self, surface: pygame.Surface):
        self.screen2 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
        self.screen2.fill(pygame.Color('black'))
        self.screen2.set_alpha(200)
        self.button_continue = Button(self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.35,
                                      self.screen2.get_height() * 0.15,
                                      'continue', self.screen2)
        self.button_map = Button(self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.35,
                                 self.screen2.get_height() * 0.55,
                                 'map', self.screen2)
        self.button_continue.draw(self.screen2)
        self.button_map.draw(self.screen2)
        surface.blit(self.screen2, (screen.get_width() * 0.25, screen.get_height() * 0.25))

    def update(self, mouse_pos: tuple[int, int]) \
            -> None or str:  # Проверяет нажатие на кнопку и вовзращает действие, в зависимости от нажатой кнопки
        new_mouse_pos = mouse_pos[0] - screen.get_width() * 0.25, mouse_pos[1] - screen.get_height() * 0.25
        if self.button_map.rect.collidepoint(new_mouse_pos):
            return 'map'
        if self.button_continue.rect.collidepoint(new_mouse_pos):
            return 'continue'


class EndGame:  # Класс меню окончания уровня
    def __init__(self):
        self.screen2 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
        self.button_next = Button(self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.35,
                                  self.screen2.get_height() * 0.6, 'map', self.screen2)

    def draw(self, surface: pygame.Surface):
        self.screen2 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
        self.screen2.fill(pygame.Color('black'))
        self.screen2.set_alpha(250)
        self.button_next = Button(self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.15,
                                  self.screen2.get_height() * 0.6, 'map', self.screen2)
        self.button_next.draw(self.screen2)
        if data.globals.LANGUAGE:
            text = 'Вы победили!'
        else:
            text = 'You win!'
        self.screen2.blit(pygame.font.Font('data/font.otf', screen.get_width() // 13).render(text, True,
                                                                                             pygame.Color('white')),
                          (self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.29,
                           self.screen2.get_height() * 0.2))
        surface.blit(self.screen2, (screen.get_width() * 0.25, screen.get_height() * 0.25))

    def update(self, mouse_pos: tuple[int, int]) \
            -> None or str:  # Проверяет нажатие на кнопку и вовзращает действие, в зависимости от нажатой кнопки
        new_mouse_pos = mouse_pos[0] - screen.get_width() * 0.25, mouse_pos[1] - screen.get_height() * 0.25
        if self.button_next.rect.collidepoint(new_mouse_pos):
            return 'map'


class DeadScene:  # Класс меню смерти игрока
    def __init__(self):
        self.screen2 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
        self.button_reset = Button(self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.35,
                                   self.screen2.get_height() * 0.6, 'reset', self.screen2)

    def draw(self, surface: pygame.Surface):
        self.screen2 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
        self.screen2.fill(pygame.Color('black'))
        self.screen2.set_alpha(250)
        self.button_reset = Button(self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.35,
                                   self.screen2.get_height() * 0.6, 'reset', self.screen2)
        self.button_reset.draw(self.screen2)
        self.screen2.blit(pygame.font.Font('data/font.otf', screen.get_width() // 13).render('YOU DIED', True,
                                                                                             pygame.Color(132, 31, 31)),
                          (self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.29,
                           self.screen2.get_height() * 0.2))
        surface.blit(self.screen2, (screen.get_width() * 0.25, screen.get_height() * 0.25))

    def update(self, mouse_pos: tuple[int, int]) \
            -> None or str:  # Проверяет нажатие на кнопку и вовзращает действие, в зависимости от нажатой кнопки
        new_mouse_pos = mouse_pos[0] - screen.get_width() * 0.25, mouse_pos[1] - screen.get_height() * 0.25
        if self.button_reset.rect.collidepoint(new_mouse_pos):
            return 'reset'
