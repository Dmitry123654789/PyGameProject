from random import randint

import pygame

from logic.Game.Things.Thing import Portal, HealthBottle
from logic.seting import CELL_SIZE


class Things(pygame.sprite.Group):
    """Класс вещей"""
    def __init__(self, tmx_map, draw_group):
        super().__init__()
        self.add_things(tmx_map, draw_group)

    def add_things(self, draw_group, tmx_map):
        # Добавляем лечебные бутылки с 50% шансом
        for obj in tmx_map.get_layer_by_name('Points_bottle'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            if randint(0, 1) == 1:
                HealthBottle(pos, draw_group, self)

        # Добавляем все порталы
        for obj in tmx_map.get_layer_by_name('Portal'):
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            pos = obj.x / 16 * CELL_SIZE + size[0] / 2, obj.y / 16 * CELL_SIZE + size[1] / 2
            Portal(pos, draw_group, self)

    def shift(self, delta_x, delta_y):
        # Сдвиг всех спрайтов группы на какую-либо дельту
        for sprite in self:
            sprite.shift(delta_x, delta_y)

    def update(self, player_group,enemy_group):
        """Обновление спрайтов группы"""
        for sprite in self:
            if isinstance(sprite, HealthBottle):
                sprite.update(player_group)
            elif isinstance(sprite, Portal):
                sprite.update(enemy_group)
