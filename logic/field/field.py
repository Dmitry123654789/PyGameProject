import pygame

from pytmx import load_pygame
from logic.seting import *
from logic.field.Tiles import *

tmx_map = load_pygame('data/world.tmx')


class Field(pygame.sprite.Group):

    def __init__(self, now_x, now_y):
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, tmx_map.width * CELL_SIZE, tmx_map.height * CELL_SIZE)
        self.now_coord = [now_x, now_y]

    def create_field(self, collision_group, draw_field):
        # Добавляем все видимые слои тайтлов
        for layer in tmx_map.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * CELL_SIZE, y * CELL_SIZE)
                    Tile(pos, pygame.transform.scale(surf, (CELL_SIZE, CELL_SIZE)), self, draw_field)

        # Добавляем слой спрайтов
        for obj in tmx_map.get_layer_by_name('Sprites'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            Tile(pos, pygame.transform.scale(obj.image, size), self, draw_field)

        # Добавляем слой полигонов (хитбоксов)
        for obj in tmx_map.get_layer_by_name('Polygon'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            TileObject(pos, size, self, collision_group)


    def shift_sprites(self, delta_x, delta_y):
        for sprite in self.sprites():
            sprite.rect.center = (sprite.rect.centerx - delta_x, sprite.rect.centery - delta_y)

    def update_coord(self, pos_player, rect_player, delta_x=0, delta_y=0):
        # Обновляем наши фактические координаты на поле
        self.now_coord[0] += delta_x
        self.now_coord[1] += delta_y

        # Находится ли персонаж в своем квадрате
        if not ((delta_x > 0 and pos_player.right > rect_player.right) or
                (delta_x < 0 and pos_player.left < rect_player.left) or
                (delta_y > 0 and pos_player.bottom > rect_player.bottom) or
                (delta_y < 0 and pos_player.top < rect_player.top)):
            return 1

        # Подошел ли персонаж к концу карты
        if delta_x > 0 and self.now_coord[0] + (screen.get_size()[0] - pos_player.x) >= self.rect.width or \
                delta_y > 0 and self.now_coord[1] + (screen.get_size()[1] - pos_player.y) >= self.rect.height or \
                delta_x < 0 and self.now_coord[0] - pos_player.centerx <= 0 or \
                delta_y < 0 and self.now_coord[1] - pos_player.centery <= 0:
            return 1

        # Передвигаем все спрайты
        self.shift_sprites(delta_x, delta_y)
        return 0
