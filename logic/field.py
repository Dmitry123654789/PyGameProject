import pygame
from pytmx import load_pygame

from logic.seting import *

tmx_map = load_pygame('data/world.tmx')


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class TileObject(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.hitbox = pygame.rect.Rect(*pos, *size)


class Field(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def set_darkness(self):
        """Затемнение"""
        darkness = pygame.Surface(SIZE)
        darkness.fill(pygame.Color('black'))
        darkness.set_alpha(100)
        screen.blit(darkness, (0, 0))
