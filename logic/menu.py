import pygame

from logic.seting import *
from logic.story_telling import show_story
from logic.stats_menu import Statistics


class Menu:
    def __init__(self):
        self.buttons_poses = []  # расположения кнопок
        self.text = LANGUAGE
        self.buttons_tasks = self.language()  # задачи кнопок меню
        self.im_speaker = True  # True - включен. False - выключен
        self.fill_buttons_poses()
        self.another_scene = None
        self.is_action_true = True

    # функция для смены языка
    # в дальнейшем будет брать слова из отдельного файла
    def language(self):
        global LANGUAGE
        if self.text:
            LANGUAGE = True
            return ['Начать игру', 'Статистика', 'Сменить язык', 'Выход']
        else:
            LANGUAGE = False
            return ['Start game', 'Statistics', 'Language', 'Exit']

    def fill_buttons_poses(self):
        self.buttons_poses = [pygame.rect.Rect(screen.get_width() // 8, i, 200, 50) for i in
                              range(150, 400, 80)]  # расположения кнопок
        self.buttons_poses.append(pygame.rect.Rect(screen.get_width() - screen.get_width() // 6, 0, 75, 75))

    # отрисовывает все
    def draw(self, surface):
        im = pygame.transform.scale(load_image('images/castle_menu.jpg'), screen.get_size())
        surface.blit(im, (0, 0))
        font = pygame.font.Font('data/font.otf', 30)
        surface.blit(pygame.font.Font('data/font.otf', 50).render('Bark and Battle', True, (192, 192, 192)),
                     (screen.get_width() // 8, 50))
        for elem in zip(self.buttons_poses[:-1], self.buttons_tasks):
            text = font.render(elem[1], True, (192, 192, 192))
            surface.blit(text, (elem[0].x + 10, elem[0].y + 15))
        if self.im_speaker:
            im_speaker = pygame.transform.scale(load_image('images/speaker.png'), (50, 50))
        else:
            im_speaker = pygame.transform.scale(load_image('images/mute_speaker.png'), (50, 50))
        surface.blit(im_speaker, (self.buttons_poses[-1].x, self.buttons_poses[-1].y))


def menu_scene(switch_scene):
    menu = Menu()
    running = True
    virtual_surface = pygame.surface.Surface(screen.get_size())

    # проверяет нажатие мыши на кнопки
    def check_coords(coord_mouse):
        for elem in menu.buttons_poses:
            if elem.collidepoint(coord_mouse):
                open_smth(elem)

    def open_smth(elem):
        nonlocal running
        if menu.is_action_true:
            if elem == menu.buttons_poses[0]:  # начало игры
                running = False
                switch_scene(show_story)
            elif elem == menu.buttons_poses[1]:  # статистика
                menu.another_scene = Statistics()
                menu.is_action_true = False
            elif elem == menu.buttons_poses[2]:  # меняет язык
                menu.text = not menu.text
                menu.buttons_tasks = menu.language()
            elif elem == menu.buttons_poses[4]:  # выключает музыку
                if menu.im_speaker:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                menu.im_speaker = not menu.im_speaker
            elif elem == menu.buttons_poses[3]:  # выход из игры через кнопку
                running = False
                switch_scene(None)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                check_coords(event.pos)
            if event.type == pygame.WINDOWRESIZED:
                # Окно не может быть меньше каких-то размеров
                if screen.get_size()[0] < WIDTH:
                    pygame.display.set_mode((WIDTH, screen.get_size()[1]), pygame.RESIZABLE)
                if screen.get_size()[1] < HEIGHT:
                    pygame.display.set_mode((screen.get_size()[0], HEIGHT), pygame.RESIZABLE)

            if menu.another_scene is not None:
                if menu.another_scene.handle_event(event, virtual_surface) == 'Close':
                    menu.another_scene = None
                    menu.is_action_true = True

        menu.draw(virtual_surface)
        if menu.another_scene is not None:
            menu.another_scene.draw(virtual_surface)
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
    pygame.quit()
