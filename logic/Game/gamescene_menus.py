import pygame

import data.globals
from logic.Game.Input import Button, TextBox
from logic.seting import screen


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
        self.tex_box = TextBox(0, 0, pygame.font.Font('data\\font.otf', screen.get_width() // 30),
                               'Player', ['Your name: ', 'Ваше имя: '])

    def draw(self, surface: pygame.Surface):
        self.screen2 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
        self.screen2.fill(pygame.Color('black'))
        self.screen2.set_alpha(250)
        self.button_next = Button(self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.35,
                                  self.screen2.get_height() * 0.55,
                                  'map', self.screen2)
        self.button_next.draw(self.screen2)
        if data.globals.LANGUAGE:
            text = 'Победа!'
        else:
            text = 'You win!'

        render_text = pygame.font.Font('data\\font.otf', screen.get_width() // 15).render(text, True,
                                                                                          pygame.Color('white'))
        self.screen2.blit(render_text, (
            self.screen2.get_width() * 0.5 - self.screen2.get_width() * 0.2, self.screen2.get_height() * 0.05))

        self.tex_box.font = pygame.font.Font('data\\font.otf', screen.get_width() // 35)
        self.tex_box.update()
        text_box_surf = self.tex_box.draw()
        self.screen2.blit(text_box_surf, (
            self.screen2.get_width() // 2 - text_box_surf.get_width() // 2 - 5, render_text.get_height() + 50))
        self.tex_box.x, self.tex_box.y = (
            self.screen2.get_width() // 2 - text_box_surf.get_width() // 2 - 5 + screen.get_width() * 0.25,
            render_text.get_height() + 50 + screen.get_height() * 0.25)
        surface.blit(self.screen2, (screen.get_width() * 0.25, screen.get_height() * 0.25))

    def update(self, mouse_pos: tuple[int, int]) -> None or str:
        """Проверяет нажатие на кнопку и вовзращает действие, в зависимости от нажатой кнопки"""
        new_mouse_pos = mouse_pos[0] - screen.get_width() * 0.25, mouse_pos[1] - screen.get_height() * 0.25
        if self.button_next.rect.collidepoint(new_mouse_pos):
            return 'map_end'


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
