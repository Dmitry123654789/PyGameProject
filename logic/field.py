import pygame
from pytmx import load_pygame, TiledTileLayer

from logic.seting import *

tmx_map = load_pygame('data/world.tmx')


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class Field(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    # def update(self, delt_x=0, delt_y=0):
    #     title_img = self.tmx_map.get_tile_image_by_gid
    #     for layer in self.tmx_map.visible_layers:
    #         if isinstance(layer, TiledTileLayer):
    #             for x, y, serf in layer:
    #                 title = title_img(serf)
    #
    #                 if title:
    #                     title = pygame.transform.scale(title, (CELL_SIZE, CELL_SIZE))
    #                     screen.blit(title, (x * CELL_SIZE - delt_x, y * CELL_SIZE - delt_y))

    def set_darkness(self):
        """Затемнение"""
        darkness = pygame.Surface(SIZE)
        darkness.fill(pygame.Color('black'))
        darkness.set_alpha(100)
        screen.blit(darkness, (0, 0))


field = Field()
for layer in tmx_map.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * CELL_SIZE, y * CELL_SIZE)
            Tile(pos, pygame.transform.scale(surf, (CELL_SIZE, CELL_SIZE)), field)
