import pygame

from logic.seting import *
from main import *


# над размером окна и его расположением относительно главного нужно подумать
# оставляем его на потом, до реализации статистики
def setting_scene(screen):
    pygame.init()
    pygame.display.set_caption('Настройки')
    screen2 = pygame.Surface((500, 500))
    screen2.set_alpha(80)
    screen2.fill(pygame.color.Color('white'))
    screen.blit(screen2, (960, 540))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
