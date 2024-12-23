import pygame
from logic.seting import *
from main import * # Из main нельзя ничего импортировать так ты по факту создаешь второй главный(исполняемый) файл


class Menu:
    def __init__(self):
        self.buttons_texts = []  # тексты для кнопок меню
        self.buttons_tasks = []  # задачи кнопок меню
        # self.draw_buttons()

    # def draw_buttons(self):
    #     pygame.draw.rect(screen, pygame.color.Color('red'), (100, 100, 120, 120))


def menu_scene(scene):
    # инициализация для переключения сцен
    start_game = Game() # Экземпляр класса Game может быть только один, так получаетя как будто ты создаешь две игры

    # Ненадо
    # pygame.init()
    # pygame.display.set_caption('Castle')
    # screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
    # Дав раза инициализация - хрень. Все уже инициализируется в seting

    im = pygame.transform.scale(load_image('images/castle_menu.jpg'), screen.get_size())
    screen.blit(im, (0, 0))
    # text = pygame.font.SysFont('Corbel', 35).render('start', True, pygame.color.Color('green'))
    # pygame.draw.rect(screen, pygame.color.Color('red'), (100, 150, 150, 50))
    # pygame.draw.rect(screen, pygame.color.Color('red'), (100, 150, 150, 50))
    # pygame.draw.rect(screen, pygame.color.Color('red'), (100, 150, 150, 50))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_game.switch_scene(None)

        pygame.display.flip()
    pygame.quit()
