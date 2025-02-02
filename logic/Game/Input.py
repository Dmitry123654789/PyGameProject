import pygame

import data.globals
from data.languages import english, russian
from logic.seting import screen


class Button(pygame.sprite.Sprite):  # Класс кнопки для меню уровней
    def __init__(self, pos_x: float, pos_y: float, text: str, surface: pygame.Surface):
        super().__init__()
        if data.globals.LANGUAGE:
            lang = russian.rus
        else:
            lang = english.eng
        font = pygame.font.Font('data/font.otf', 30)
        self.button = pygame.Surface((surface.get_width() // 1.3, surface.get_height() // 3), pygame.SRCALPHA)
        pygame.draw.rect(self.button, (60, 60, 60), self.button.get_rect(), 0, 20)
        text_surf = font.render(lang[text], False, 'White')
        self.button.blit(text_surf, (self.button.get_width() // 2 - text_surf.get_width() // 2,
                                     self.button.get_height() // 2 - text_surf.get_height() // 2))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.button.get_rect().move(pos_x, pos_y)

    def draw(self, surface):  # Отрисовывает кнопку на поверхности
        surface.blit(self.button, self.rect)


class TextBox:
    def __init__(self, x, y, text, font, back_text):
        """
        :param x: Координата X
        :param y: Координата Y
        :param text: Текущий вводимый текст
        :param font: Шрифт текста
        :param back_text: Текст перед TextBox
        """
        # ['Your name', 'Ваше имя']
        self.max_len = 10  # Максимальная длина вводимого текста
        self.ind = 0  # Индекс для мигания курсора
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.language = back_text  # Поддержка разных языков
        self.select = False  # Флаг выбора (активно ли поле)
        self.rect_color = None  # Цвет рамки текстового поля
        self.text_render = None  # Отрисованный текст
        self.back_text_render = None  # Отрисованная подсказка
        self.rect = None

        self.update()

    def update_text(self, event):
        """Обновление текста в поле при вводе пользователем"""
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]  # Удаление последнего символа при нажатии Backspace
        else:
            self.text += event.unicode  # Добавление введённого символа

        self.text = self.text[:self.max_len]  # Ограничение длины текста

    def update_select(self, pos):
        """Проверяет, было ли нажатие мыши на текстовое поле"""
        self.select = self.rect.collidepoint(pos)  # Устанавливает флаг выбора

    def update(self):
        """Обновление отрисовки текста, прямоугольника и фонового текста"""
        self.text_render = self.font.render(self.text, True, 'white')  # Отрисовка текста
        self.back_text_render = self.font.render(self.language[data.globals.LANGUAGE], True, 'white')  # Отрисовка фонового текста

        # Создание прямоугольника текстового поля
        self.rect = pygame.Rect(
            self.x + self.back_text_render.get_width(), self.y - 7,
            max(100, self.text_render.get_width() + 12), self.font.get_linesize() + 9
        )

    def draw(self):
        """Отрисовка текстового поля, текста и мигающего курсора"""
        # Изменение цвета рамки в зависимости от состояния
        if self.select:
            self.rect_color = 'lightskyblue3'  # Голубой цвет при выборе
        else:
            self.rect_color = 'gray15'  # Серый цвет при отсутствии выбора
            self.ind = 0  # Сброс индекса мигания

        self.ind += 0.05  # Изменение индекса для мигания курсора

        screen.blit(self.back_text_render, (self.x, self.y))
        screen.blit(self.text_render, (self.x + 7 + self.back_text_render.get_width(), self.y))
        pygame.draw.rect(screen, self.rect_color, self.rect, 2)
        # Отрисовка мигающего курсора
        pygame.draw.rect(
            screen, ['black', 'white'][int(self.ind) % 2],
            (self.x + self.text_render.get_width() + self.back_text_render.get_width() + 7,
             self.y, 2, self.font.get_linesize() - 5)
        )
