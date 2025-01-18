import os
import sys

import pygame

FPS = 240
SIZE = WIDTH, HEIGHT = 800, 600
CELL_SIZE = 30
LANGUAGE = True  # True - Русский. False - английский. TRUE/FALSE сделано для удобства и чтобы не писать много if-ов
pygame.init()
pygame.display.set_caption('Bark and Battle')
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
screen.fill(pygame.Color('black'))
is_music_play = False
volume_sound_background = 0.1
virtual_surface = pygame.Surface(
    (2560, 1440), pygame.SRCALPHA)  # поверхность, на которой отрисовывается все изначально
current_level = ''
WORLD_LAYERS = {
    'Grass': 0,
    'Shadow': 6,
    'Wall': 2,
    'Down_layer': 3,
    'Down_sprites': 4,
    'Main': 5,
    'Sprites': 5,
    'Up_sprites': 6,
    'Up_layer': 7
}

ENEMY = {
    # Цвет: шаг, здоровье, урон, шанс
    'orange': (4, 100, 10, 50),
    'brown': (6, 150, 15, 30),
    'dark': (8, 200, 25, 10)
}
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
    """Разделяет изображение на словарь surface"""
    """Surface, ширина и длина одного спрайта, итоговый размер спрайта"""
    sprites = {'down': [], 'left': [], 'right': [], 'up': []}
    for y, key in enumerate(sprites.keys()):
        for x in range(6):
            rect = pygame.Rect(x * sprite_height_width, y * sprite_height_width, sprite_height_width,
                               sprite_height_width)
            frame = pygame.transform.scale(image.subsurface(rect).copy(), (cell_size, cell_size))
            sprites[key].append(frame)

    return sprites
