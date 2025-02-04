import sqlite3

import pygame

import data.globals
from logic.seting import screen


class StatisticButton(pygame.sprite.Sprite):
    """Класс кнопки статистики"""

    def __init__(self, pos, numb, *group):
        super().__init__(*group)

        # Создание поверхности кнопки
        self.image = pygame.surface.Surface((120, 35))
        self.image.fill((163, 163, 163))

        self.numb = numb  # Номер уровня

        # Выбор языка
        self.lang = 'Уровень' if data.globals.LANGUAGE else 'Level'

        # Отображение текста на кнопке
        self.image.blit(pygame.font.Font('data/font.otf', 25).render(f'{self.lang} {self.numb + 1}',
                                                                     True, pygame.Color('black')), (5, 5))

        # Определение прямоугольника кнопки для обработки столкновений
        self.rect = self.image.get_rect(topleft=pos)
        self.select = False  # Флаг выбора кнопки

    def collision(self, pos):
        """Проверка нажатия на кнопку"""
        return self.rect.collidepoint(pos)

    def update(self, pos):
        """Обновление состояния кнопки при наведении"""
        if self.rect.collidepoint(pos):
            self.image.fill((100, 100, 100))  # Затемнение кнопки при наведении
            self.select = True
        else:
            self.image.fill((163, 163, 163))  # Возвращение цвета при уходе курсора
            self.select = False

        # Обновление текста на кнопке
        self.image.blit(pygame.font.Font('data/font.otf', 25).render(f'{self.lang} {self.numb + 1}',
                                                                     True, pygame.Color('black')), (5, 5))


class Statistics(pygame.sprite.Group):
    """Класс окна статистики"""

    def __init__(self):
        super().__init__()

        self.add_button()  # Добавление кнопок

        # Подключение к базе данных
        self.con = sqlite3.connect('statictic.sqlite')

        # Название кнопки выхода на выбранном языке
        self.lang = 'Назад' if data.globals.LANGUAGE else 'Back'

    def add_button(self):
        """Добавление кнопок статистики"""
        for i in range(4):
            if i == 0:
                # Первая кнопка автоматически выделяется
                but = StatisticButton((0, 0), i, self)
                but.select = True
                but.update((0, 0))
            else:
                StatisticButton((0, 0), i, self)

    def update(self, pos):
        """Обновление кнопок при наведении"""
        collide = [sprite.collision(pos) for sprite in self.sprites()]

        if any(collide):
            for sprite in self.sprites():
                sprite.update(pos)

    def draw(self, surface):
        """Отрисовка окна статистики и кнопок"""
        # Создание полупрозрачного окна статистики
        screen2 = pygame.surface.Surface((max(700, screen.get_width() // 2), screen.get_height() // 2))
        screen2.set_alpha(100)
        screen2.fill(pygame.color.Color('white'))

        screen2.blit(pygame.font.Font('data/font.otf', 25).render(f'{self.lang}: Esc', True, pygame.Color('black')),
                     (20, 10))

        # Вычисление позиции окна по центру экрана
        dest_x, dest_y = (
            screen.get_width() // 2 - screen2.get_width() // 2,
            screen.get_height() // 2 - screen2.get_height() // 2
        )

        # Отображение окна статистики
        surface.blit(screen2, (dest_x, dest_y))

        # Отображение кнопок
        for n, sprite in enumerate(self.sprites()):
            sprite.rect.x = dest_x + 20 + n * (2 + sprite.rect.width)
            sprite.rect.y = dest_y + 40
            surface.blit(sprite.image, sprite.rect)

            # Если кнопка выбрана, отображаем статистику
            if sprite.select:
                cur = self.con.cursor()

                # Запрос к базе данных: получение лучших результатов для уровня
                result = cur.execute("SELECT Time, Name FROM GameStat "
                                     "WHERE Level = ? "
                                     "ORDER BY Time", (sprite.numb + 1,)).fetchall()

                # Отображение топ-10 результатов
                for i in range(10):
                    if i >= len(result):
                        text = f'{i + 1}. {' ' * 10}: __.__.__'  # Заполнение пустых строк
                    else:
                        hours = result[i][0] // 60 // 60
                        minutes = result[i][0] // 60 % 60
                        text = (f'{i + 1}. {result[i][1]}: {''.ljust(10 - len(result[i][1]))}'
                                f'{str(hours).zfill(2)}.{str(minutes).zfill(2)}.{str(result[i][0] % 60).zfill(2)}')

                    font_size = screen.get_height() // 100 * 5 - 10
                    surface.blit(pygame.font.Font('data/font.otf', font_size).render(text, True, pygame.Color('black')),
                                 (dest_x + 25, dest_y + 90 + font_size * i))

    def handle_event(self, event):
        """Обработка нажатия клавиш"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'Close'  # Закрытие окна при нажатии Escape
