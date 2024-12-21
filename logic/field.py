import pygame
from pytmx import load_pygame, TiledTileLayer

from logic.seting import *

tmx_map = load_pygame('data/world.tmx')


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class TileObject(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class Field(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

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
            # pygame.draw.rect(screen, 'yellow', (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

for obj in tmx_map.objects:
    pos = (obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE)
    TileObject(pos, pygame.transform.scale(obj.image, (CELL_SIZE, CELL_SIZE)), field)
    # pygame.draw.rect(screen, 'red', (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
