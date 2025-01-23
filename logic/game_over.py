import pygame
from logic.seting import LANGUAGE, screen
from logic.pause import Button


class DeadScene:
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

    def update(self, mouse_pos: tuple[int, int]) -> None or str:
        new_mouse_pos = mouse_pos[0] - screen.get_width() * 0.25, mouse_pos[1] - screen.get_height() * 0.25
        if self.button_reset.rect.collidepoint(new_mouse_pos):
            return 'reset'
