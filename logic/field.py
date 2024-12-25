from dataclasses import field

import pygame
from pytmx import load_pygame

from logic.seting import *

tmx_map = load_pygame('data/world.tmx')


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

    def set_darkness(self):
        """Затемнение"""
        darkness = pygame.Surface(self.rect.size)
        darkness.fill(pygame.Color('black'))
        darkness.set_alpha(100)
        self.image.blit(darkness, (0, 0))


class TileObject(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(*pos, *size)


class Field(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, tmx_map.width * CELL_SIZE, tmx_map.height * CELL_SIZE)
        self.now_coord = [screen.get_size()[0] / 2, screen.get_size()[1] / 2]

    def create_field(self, collision_group, draw_field):
        for layer in tmx_map.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * CELL_SIZE, y * CELL_SIZE)
                    Tile(pos, pygame.transform.scale(surf, (CELL_SIZE, CELL_SIZE)), self, draw_field)

        for obj in tmx_map.get_layer_by_name('Polygon'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            TileObject(pos, size, self)

    def update_coord(self, pos_player, rect_player, delta_x=0, delta_y=0):
        self.now_coord[0] += delta_x
        self.now_coord[1] += delta_y

        # Подошел ли персонаж к концу карты
        # if self.now_coord[0] - screen.get_size()[0] / 2 < 0 or self.now_coord[0] + screen.get_size()[0] / 2 > self.rect.width:
        #     print( self.now_coord[0], pos_player.centerx)
        #     return True

        # Находится ли персонаж в своем квадрате
        if delta_x > 0 and pos_player.x + pos_player.width < rect_player.x + rect_player.width or delta_x < 0 and pos_player.x > rect_player.x or \
                delta_y > 0 and pos_player.y + pos_player.height < rect_player.y + rect_player.height or delta_y < 0 and pos_player.y > rect_player.y:
            return True

        print( self.now_coord[0], pos_player.centerx)
        for sprite in self.sprites():
            sprite.rect.center = (sprite.rect.centerx - delta_x, sprite.rect.centery - delta_y)

        return False




