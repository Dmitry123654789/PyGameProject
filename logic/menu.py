import pygame
from logic.seting import *
from logic.story_telling import show_story
from logic.setting_menu import setting_scene


class Menu:
    def __init__(self):
        self.buttons_poses = [pygame.rect.Rect(100, i, 200, 50) for i in range(150, 320, 80)]  # расположения кнопок
        self.buttons_poses.append(pygame.rect.Rect(screen.get_size()[0] - 200, 0, 75, 75))
        self.text = LANGUAGE
        self.buttons_tasks = self.language()  # задачи кнопок меню
        self.im_speaker = True  # True - включен. False - выключен
        self.draw()
        self.another_scene = None

    # функция для смены языка
    # в дальнейшем будет брать слова из отдельного файла
    def language(self):
        global LANGUAGE
        if self.text:
            LANGUAGE = True
            return ['Начать игру', 'Статистика', 'Сменить язык']
        else:
            LANGUAGE = False
            return ['Start game', 'Statistics', 'Language']

    # отрисовывает все
    def draw(self):
        place_background()
        font = pygame.font.Font('data/font.otf', 30)
        screen.blit(pygame.font.Font('data/font.otf', 50).render('Bark and Battle', True, (192, 192, 192)), (100, 50))
        for elem in zip(self.buttons_poses[:-1], self.buttons_tasks):
            text = font.render(elem[1], True, (192, 192, 192))
            screen.blit(text, (elem[0].x + 10, elem[0].y + 15))
        if self.im_speaker:
            im_speaker = pygame.transform.scale(load_image('images/speaker.png'), (75, 75))
        else:
            im_speaker = pygame.transform.scale(load_image('images/mute_speaker.png'), (75, 75))
        screen.blit(im_speaker, (self.buttons_poses[-1].x, self.buttons_poses[-1].y))


def place_background():
    im = pygame.transform.scale(load_image('images/castle_menu.jpg'), screen.get_size())
    screen.blit(im, (0, 0))


def menu_scene(switch_scene):
    menu = Menu()
    running = True

    # проверяет нажатие мыши на кнопки
    def check_coords(coord_mouse):
        for elem in menu.buttons_poses:
            if elem.collidepoint(coord_mouse):
                open_smth(elem)

    def open_smth(elem):
        if elem == menu.buttons_poses[0]:
            switch_scene(show_story)
        elif elem == menu.buttons_poses[1]:  # статистика
            menu.another_scene = setting_scene
        elif elem == menu.buttons_poses[2]:  # меняет язык
            menu.text = not menu.text
            menu.buttons_tasks = menu.language()
            menu.draw()
        elif elem == menu.buttons_poses[3]:
            if menu.im_speaker:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            menu.im_speaker = not menu.im_speaker
            menu.draw()
            # выключает музыку

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                check_coords(event.pos)
            if event.type == pygame.WINDOWRESIZED:
                place_background()
            if menu.another_scene:
                if not menu.another_scene():
                    menu.another_scene = None
                    menu.draw()
            if event.type == pygame.WINDOWRESIZED:
                place_background()
                menu.draw()
        pygame.display.flip()
    pygame.quit()
