import pygame
from logic.seting import *
from main import *
from logic.setting_menu import setting_scene


class Menu:
    def __init__(self):
        self.buttons_poses = [pygame.rect.Rect(100, i, 200, 50) for i in range(150, 320, 80)]  # расположения кнопок
        self.text_rus = True
        self.buttons_tasks = self.language()  # задачи кнопок меню
        self.draw_options()

    # функция для смены языка
    # в дальнейшем будет брать слова из отдельного файла
    def language(self):
        if self.text_rus:
            return ['Начать игру', 'Настройки', 'Сменить язык']
        return ['Start game', 'Settings', 'Language']

    # отрисовывает все
    def draw_options(self):
        place_background()
        font = pygame.font.Font('data/font.otf', 30)
        screen.blit(pygame.font.Font('data/font.otf', 50).render('Bark and Battle', True, (192, 192, 192)), (100, 50))
        for elem in zip(self.buttons_poses, self.buttons_tasks):
            # pygame.draw.rect(screen, pygame.color.Color('green'), elem[0])
            text = font.render(elem[1], True, (192, 192, 192))
            screen.blit(text, (elem[0].x + 10, elem[0].y + 15))

    def open_smth(self, elem, coord_mouse):
        if elem == self.buttons_poses[0]:
            # начать игру
            pass
        elif elem == self.buttons_poses[1]:
            start_game.switch_scene(setting_scene)
        elif elem == self.buttons_poses[2]:  # меняет язык
            self.text_rus = not self.text_rus
            self.buttons_tasks = self.language()
            self.draw_options()

    # проверяет нажатие мыши на кнопки
    def check_coords(self, coord_mouse):
        for elem in self.buttons_poses:
            if elem.collidepoint(coord_mouse):
                self.open_smth(elem, coord_mouse)


def place_background():
    im = pygame.transform.scale(load_image('images/castle_menu.jpg'), screen.get_size())
    screen.blit(im, (0, 0))


start_game = Game()


def menu_scene():
    # инициализация для переключения сцен
    pygame.init()
    pygame.display.set_caption('Bark and Battle')
    pygame.display.set_icon(load_image('images/icon_app.jpg'))
    menu = Menu()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_game.switch_scene(None)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                menu.check_coords(event.pos)
            if event.type == pygame.WINDOWRESIZED:
                place_background()
        pygame.display.flip()
    pygame.quit()
