import pygame

import data.globals
from data.languages.language import game_elements


class Button(pygame.sprite.Sprite):  # Класс кнопки для меню уровней
    def __init__(self, pos_x: float, pos_y: float, text: str, surface: pygame.Surface):
        super().__init__()
        font = pygame.font.Font('data/font.otf', 30)
        self.button = pygame.Surface((surface.get_width() // 1.3, surface.get_height() // 3), pygame.SRCALPHA)
        pygame.draw.rect(self.button, (60, 60, 60), self.button.get_rect(), 0, 20)
        text_surf = font.render(game_elements[text][data.globals.LANGUAGE_INDEX], False, 'White')
        self.button.blit(text_surf, (self.button.get_width() // 2 - text_surf.get_width() // 2,
                                     self.button.get_height() // 2 - text_surf.get_height() // 2))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.button.get_rect().move(pos_x, pos_y)

    def draw(self, surface):  # Отрисовывает кнопку на поверхности
        surface.blit(self.button, self.rect)


class TextBox:
    def __init__(self, x, y, font, text):
        """
        :param x: Координата X
        :param y: Координата Y
        :param text: Текущий вводимый текст
        :param font: Шрифт текста
        """
        # ['Your name', 'Ваше имя']
        self.max_len = 10  # Максимальная длина вводимого текста
        self.ind = 0  # Индекс для мигания курсора
        self.x = x
        self.y = y
        self.text = text
        self.font = font
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
        pos = pos[0] - self.x, pos[1] - self.y
        self.select = self.rect.collidepoint(pos)  # Устанавливает флаг выбора

    def update(self):
        """Обновление отрисовки текста, прямоугольника и фонового текста"""
        self.text_render = self.font.render(self.text, True, 'white')  # Отрисовка текста
        # Отрисовка фонового текста
        self.back_text_render = self.font.render(game_elements['text_box'][data.globals.LANGUAGE_INDEX], True, 'white')

        # Создание прямоугольника текстового поля
        self.rect = pygame.Rect(
            self.back_text_render.get_width(), 0,
            max(100, self.text_render.get_width() + 12), self.font.get_linesize() + 10
        )

    def draw(self):
        """Отрисовка текстового поля, текста и мигающего курсора"""
        # Изменение цвета рамки в зависимости от состояния
        if self.select:
            self.rect_color = 'lightskyblue3'  # Голубой цвет при выборе
        else:
            self.rect_color = 'gray15'  # Серый цвет при отсутствии выбора
            self.ind = 0  # Сброс индекса мигания

        self.ind += 0.1  # Изменение индекса для мигания курсора
        surf = pygame.surface.Surface((self.back_text_render.get_width() + self.rect.width + 7, self.rect.height),
                                      pygame.SRCALPHA)
        surf.blit(self.back_text_render, (0, 5))
        surf.blit(self.text_render, (3 + self.back_text_render.get_width(), 5))
        pygame.draw.rect(surf, self.rect_color, self.rect, 2)
        # Отрисовка мигающего курсора
        pygame.draw.rect(
            surf, ['black', 'white'][int(self.ind) % 2],
            (self.text_render.get_width() + self.back_text_render.get_width() + 5,
             7, 2, self.font.get_linesize() - 5)
        )
        return surf
