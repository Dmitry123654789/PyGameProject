import os
import sys

import pygame

from logic.seting import screen


def load_image(name, colorkey=None):
    """Превращает одно изображение в surface"""
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def split_image(image, sprite_height_width, cell_size):
    """Разделение изображения на словарь surface
    :param image: изображение для нарезки
    :param sprite_height_width: ширина и длина одного спрайта,
    :param cell_size: итоговый размер спрайта"""
    sprites = {'down': [], 'left': [], 'right': [], 'up': []}
    for y, key in enumerate(sprites.keys()):
        for x in range(6):
            rect = pygame.Rect(x * sprite_height_width, y * sprite_height_width, sprite_height_width,
                               sprite_height_width)
            frame = pygame.transform.scale(image.subsurface(rect).copy(), (cell_size, cell_size))
            sprites[key].append(frame)

    return sprites


def fade_out(draw_function):
    """Скрытие окна"""
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))  # Очищаем экран перед началом fade-out
    for alpha in range(0, 255, 10):  # Изменяем шаг для более плавной анимации
        if draw_function:
            draw_function()  # Отрисовываем текущую сцену (но только один раз за цикл)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))  # Добавляем затемняющий слой
        pygame.display.update()  # Обновляем экран после наложения fade-эффекта
        pygame.time.delay(20)  # Увеличиваем задержку для большей плавности


def fade_in(draw_function):
    """Скрытие окна"""
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))  # Плавное проявление новой сцены
    for alpha in range(255, -1, -10):
        if draw_function:
            draw_function()  # Отрисовываем новую сцену (только один раз за цикл)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))  # Уменьшаем прозрачность fade-слоя
        pygame.display.update()  # Обновляем экран после наложения fade-эффекта
        pygame.time.delay(20)  # Увеличиваем задержку для большей плавности
