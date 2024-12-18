import pygame
from pytmx import load_pygame, TiledTileLayer

from logic.seting import *


class Field:
    tmx_map = load_pygame('data/world.tmx')

    def __init__(self):
        super().__init__()

    def update(self, delt_x=0, delt_y=0):
        title_img = self.tmx_map.get_tile_image_by_gid
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, serf in layer:
                    title = title_img(serf)

                    if title:
                        title = pygame.transform.scale(title, (CELL_SIZE, CELL_SIZE))
                        screen.blit(title, (x * CELL_SIZE - delt_x, y * CELL_SIZE - delt_y))

    def set_darkness(self):
        """Затемнение"""
        darkness = pygame.Surface(SIZE)
        darkness.fill(pygame.Color('black'))
        darkness.set_alpha(100)
        screen.blit(darkness, (0, 0))
