import pygame

import data.globals
from logic.seting import screen, virtual_surface, WIDTH, HEIGHT
from logic.Menu.stats_menu import Statistics
from logic.support import load_image
from logic.Menu.Elements import MenuButton, Speaker


class Menu(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.text = data.globals.LANGUAGE  # текущий язык
        self.im_speaker = True  # True - включен. False - выключен
        self.another_scene = None  # активно ли еще одно окно
        self.is_action_true = True  # активно ли главное меню
        self.add_buttton()
        self.language(change_language=False)

    def add_buttton(self):
        tasks = [('Start game', 'Начать игру'), ('Statistics', 'Статистика'), ('Change language', 'Сменить язык'),
                 ('exit', 'Выход')]
        for n, task in enumerate(tasks):
            MenuButton((0, n * 50), task, n, self)
        Speaker(self)

    def update(self):
        for sprite in self.sprites():
            sprite.update()

    def language(self, change_language=True):
        if change_language:
            data.globals.LANGUAGE = not data.globals.LANGUAGE
            self.text = data.globals.LANGUAGE
        for sprite in self.sprites()[:-1]:
            sprite.update_language(self.text)

    # отрисовывает все
    def draw(self, surface: pygame.Surface):
        # Устанавливаем задний фон
        image = load_image('images/background_menu.png')
        dark_surf = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        dark_surf.fill((0, 0, 0, 30))
        image.blit(dark_surf, (0, 0))
        surface.blit(pygame.transform.scale(image, screen.get_size()), (0, 0))

        # Вывод названия игры
        text = pygame.font.Font('data/font.otf', screen.get_height() // 10).render('Bark and Battle', True, '#ffd166')
        surface.blit(text, (screen.get_width() // 2 - text.get_width() / 2, 100))

        # Отрисовываем кнопки
        super().draw(surface)


# проверяет нажатие мыши на кнопки
def check_coords(coord_mouse: tuple[int, int], menu):
    for elem in menu.sprites():
        if elem.rect.collidepoint(coord_mouse):
            return elem
    return None


# выполняет действие кнопки, на которую нажатли
def open_smth(elem, menu, switch_scene):
    if menu.is_action_true:
        if elem == menu.sprites()[0]:  # начало игры
            switch_scene('world_map_scene')
            return False
        elif elem == menu.sprites()[1]:  # статистика
            menu.another_scene = Statistics()
            menu.is_action_true = False
        elif elem == menu.sprites()[2]:  # меняет язык
            menu.text = not menu.text
            menu.buttons_tasks = menu.language()
        elif elem == menu.sprites()[3]:  # выход из игры через кнопку
            exit(1)
        elif elem == menu.sprites()[4]:  # выключает музыку
            if menu.sprites()[4].update_value():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            menu.im_speaker = not menu.im_speaker
    return True


def main_menu_scene(switch_scene):
    menu = Menu()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход из игры по крестику окна
                exit(1)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # проверка нажатия мыши
                res = check_coords(event.pos, menu)
                if res:
                    running = open_smth(res, menu, switch_scene)
                if isinstance(menu.another_scene, Statistics):
                    menu.another_scene.update(event.pos)
            if event.type == pygame.WINDOWRESIZED:  # изменение размера окна
                # Окно не может быть меньше каких-то размеров
                if screen.get_size()[0] < WIDTH:
                    pygame.display.set_mode((WIDTH, screen.get_size()[1]), pygame.RESIZABLE)
                if screen.get_size()[1] < HEIGHT:
                    pygame.display.set_mode((screen.get_size()[0], HEIGHT), pygame.RESIZABLE)

            if menu.another_scene is not None:  # вызывается доп сцена и ожидается результат выполнения от нее
                if menu.another_scene.handle_event(event) == 'Close':
                    menu.another_scene = None
                    menu.is_action_true = True

        # отрисовываем на сцене
        virtual_surface.fill(pygame.Color('black'))
        menu.update()
        menu.draw(virtual_surface)
        if menu.another_scene is not None:
            menu.another_scene.draw(virtual_surface)

        # отрисовываем сцену на экране
        screen.blit(virtual_surface, (0, 0))
        pygame.display.flip()
