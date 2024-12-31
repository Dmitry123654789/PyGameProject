import os
import sys

import pygame

pygame.init()

SIZE = WIDTH, HEIGHT = 800, 600
FPS = 120
CELL_SIZE = 64

pygame.display.set_caption('Castle')
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
screen.fill(pygame.Color('black'))


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
    """Разделяет изображение на список surface"""
    """Surface, ширина одного спрайта, высота одного спрайта, итоговый размер спрайта"""
    sprites = {'down': [], 'left': [], 'right': [], 'up': []}
    for y, key in enumerate(sprites.keys()):
        for x in range(6):
            rect = pygame.Rect(x * sprite_height_width, y * sprite_height_width + 7, sprite_height_width,
                               sprite_height_width)
            frame = pygame.transform.scale(image.subsurface(rect).copy(), (cell_size, cell_size))
            sprites[key].append(frame)

    return sprites
