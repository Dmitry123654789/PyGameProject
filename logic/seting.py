import os
import sys

import pygame

SIZE = WIDTH, HEIGHT = 1920, 1080
FPS = 120
CELL_SIZE = 64

pygame.init()
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


def split_image_to_surfaces(image, sprite_height_width, cell_size, count_colm, row, colm):
    """Разделяет изображение на список surface"""
    """Surface, ширина одного спрайта, высота одного спрайта, итоговый размер спрайта, количество строк, 
    количество колон, какая строка, сколько колон ну жно вырезать"""

    image_width, image_height = image.get_size()
    sprites = []
    y = sprite_height_width * row
    for x in range(0, image_width // count_colm * colm, sprite_height_width):
        rect = pygame.Rect(x, y, sprite_height_width, sprite_height_width)
        sprite = pygame.transform.scale(image.subsurface(rect).copy(), (cell_size, cell_size))
        sprites.append(sprite)
    return sprites
