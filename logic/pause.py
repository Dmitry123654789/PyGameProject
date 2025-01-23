import pygame

from logic.seting import LANGUAGE, screen
from data.languages import english, russian


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x: float, pos_y: float, text: str, surface: pygame.Surface):
        super().__init__()
        if LANGUAGE:
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

    def draw(self, surface):
        surface.blit(self.button, self.rect)


class Pause:
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

    def update(self, mouse_pos: tuple[int, int]) -> None or str:
        new_mouse_pos = mouse_pos[0] - screen.get_width() * 0.25, mouse_pos[1] - screen.get_height() * 0.25
        if self.button_map.rect.collidepoint(new_mouse_pos):
            return 'map'
        if self.button_continue.rect.collidepoint(new_mouse_pos):
            return 'continue'
