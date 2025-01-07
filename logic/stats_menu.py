import pygame

from logic.seting import *


class Statistics:
    def __init__(self):
        self.buttons_poses = []
        self.buttons_tasks = []
        self.screen2 = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        self.buttons_poses.append(pygame.rect.Rect(self.screen2.get_width() - 70, 20, 35, 35))

    def draw(self, surface):
        self.screen2.set_alpha(100)
        self.screen2.fill(pygame.color.Color('white'))
        self.screen2.blit(pygame.font.Font('data/font.otf', 30).render('Назад: Esc', True, pygame.Color('black')),
                          (0, 0))
        # im_close = pygame.transform.scale(load_image('images/close.png'), (35, 35))
        # pygame.draw.rect(self.screen2, pygame.Color('red'), self.buttons_poses[0])
        # self.screen2.blit(im_close, (self.screen2.get_width() - 70, 20))
        screen.blit(self.screen2, (screen.get_width() // 3, screen.get_height() // 3))

    def handle_event(self, event, surface):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'Close'

