import pygame

from logic.seting import *


class Statistics:
    def __init__(self):
        self.buttons_poses = []
        self.buttons_tasks = []
        self.screen2 = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        self.buttons_poses.append(pygame.rect.Rect(self.screen2.get_width() - 70, 20, 35, 35))
        self.draw()

    def draw(self):
        self.screen2.set_alpha(100)
        self.screen2.fill(pygame.color.Color('white'))
        # im_close = pygame.transform.scale(load_image('images/close.png'), (35, 35))
        # pygame.draw.rect(self.screen2, pygame.Color('red'), self.buttons_poses[0])
        # self.screen2.blit(im_close, (self.screen2.get_width() - 70, 20))
        screen.blit(self.screen2, (WIDTH // 3, HEIGHT // 3))


# над размером окна и его расположением относительно главного нужно подумать
# оставляем его на потом, до реализации статистики
def setting_scene():
    pygame.init()
    stats = Statistics()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
        pygame.display.flip()
    pygame.quit()
