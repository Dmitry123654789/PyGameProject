from logic.seting import *
from main import *


def setting_scene():
    pygame.init()
    start_game = Game()
    pygame.display.set_caption('Настройки')
    screen2 = pygame.display.set_mode((400, 400))
    im = pygame.transform.scale(load_image('images/castle_menu.jpg'), screen.get_size())
    screen2.blit(im, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_game.switch_scene(None)
        pygame.display.flip()
    pygame.quit()
