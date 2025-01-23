import pygame

from logic.seting import LANGUAGE, screen
from data.languages import english, russian


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, text):
        super().__init__()
        if LANGUAGE:
            lang = russian.rus
        else:
            lang = english.eng
        font = pygame.font.Font('data/font.otf', 30)
        self.button = pygame.Surface((300, 300), pygame.SRCALPHA)
        pygame.draw.rect(self.button, (60, 60, 60), self.button.get_rect(), 0, 20)
        text_surf = font.render(lang[text], False, 'White')
        self.button.blit(text_surf, (self.button.get_width() // 2 - text_surf.get_width() // 2,
                                     self.button.get_height() // 2 - text_surf.get_height() // 2))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.button.get_rect().move(pos_x, pos_y)

    def draw(self, surface):
        surface.blit(self.button, self.rect)


class Pause:
    def __init__(self):
        self.screen2 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
        self.screen2.fill(pygame.Color('black'))
        self.screen2.set_alpha(150)
        self.button_continue = Button(self.screen2.get_width() * 0.5 - 50, self.screen2.get_height() * 0.3,
                                      'continue')
        self.button_map = Button(self.screen2.get_width() * 0.5 - 50, self.screen2.get_height() * 0.6,
                                 'map')

        self.button_continue.draw(self.screen2)
        self.button_map.draw(self.screen2)

    def draw(self, surface):
        surface.blit(self.screen2, (screen.get_width() // 4, screen.get_height() // 3.7))

    def update(self, mouse_pos):
        pass
