import os
import sys

import pygame

SIZE = WIDTH, HEIGHT = 800, 600
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
