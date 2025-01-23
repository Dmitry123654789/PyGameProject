import pygame

from logic.seting import screen


class Statistics:
    def __init__(self):
        self.buttons_poses = []
        self.buttons_tasks = []

    def draw(self, surface):
        screen2 = pygame.surface.Surface((screen.get_width() // 2, screen.get_height() // 2))
        screen2.set_alpha(100)
        screen2.fill(pygame.color.Color('white'))
        screen2.blit(pygame.font.Font('data/font.otf', 25).render('Назад: Esc', True, pygame.Color('black')),
                     (10, 10))
        # im_close = pygame.transform.scale(load_image('images/close.png'), (35, 35))
        # pygame.draw.rect(self.screen2, pygame.Color('red'), self.buttons_poses[0])
        # self.screen2.blit(im_close, (self.screen2.get_width() - 70, 20))
        surface.blit(screen2, (screen.get_width() // 3, screen.get_height() // 3))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'Close'
