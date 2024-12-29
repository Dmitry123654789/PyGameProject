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
            print(obj.image)
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            Tile(pos, pygame.transform.scale(obj.image, size), self, draw_field)

        # Добавляем слой полигонов (хитбоксов)
        for obj in tmx_map.get_layer_by_name('Polygon'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            TileObject(pos, size, self)



    def update_coord(self, pos_player, rect_player, delta_x=0, delta_y=0):
        # Обновляем наши фактические координаты на поле
        self.now_coord[0] += delta_x
        self.now_coord[1] += delta_y
        # if self.now_coord[0] >= tmx_map.width or self.now_coord[0] < 0 or self.now_coord[1] >= tmx_map.height or self.now_coord[1] < 0:
        #     return
        print(self.now_coord, pos_player)
        # Находится ли персонаж в своем квадрате
        if not ((delta_x > 0 and pos_player.right > rect_player.right) or
                (delta_x < 0 and pos_player.left < rect_player.left) or
                (delta_y > 0 and pos_player.bottom > rect_player.bottom) or
                (delta_y < 0 and pos_player.top < rect_player.top)):
            return True

        # Подошел ли персонаж к концу карты

        if (pos_player.left >= self.now_coord[0] - pos_player.width / 2 and delta_x < 0) or \
                (screen.get_size()[0] - pos_player.right >= self.now_coord[0] / 2 and delta_x > 0) or \
                (pos_player.top >= self.now_coord[1] - pos_player.height / 2 and delta_y < 0) or \
                (self.now_coord[1] + (screen.get_size()[1] - pos_player.bottom) > self.rect.height and delta_y > 0):

            return True

        # Передвигаем все спрайты
        for sprite in self.sprites():
            sprite.rect.center = (sprite.rect.centerx - delta_x, sprite.rect.centery - delta_y)
        return False
