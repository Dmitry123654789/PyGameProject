import pygame as pg

from logic.seting import WORLD_LAYERS, CELL_SIZE, screen, split_image, load_image
from logic.Entity.entity import Entity


class EnemiesGroup(pg.sprite.Group):
    def __init__(self, draw_group, map):
        super().__init__()
        self.add_enemy(draw_group, map)

    def add_enemy(self, draw_group, tmx_map):
        for obj in tmx_map.get_layer_by_name('Points'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            Enemy(pos, draw_group, self)

    def shift(self, delta_x, delta_y):
        for sprite in self:
            sprite.shift(delta_x, delta_y)


class Enemy(Entity):
    sprites = split_image(load_image('images/dog_sprites.png'), 32, CELL_SIZE * 2)
    def __init__(self, pos, *group):
        super().__init__(pos, self.sprites, *group)
        self.max_hp = 100
        self.hp = self.max_hp
        self.damage = 10

        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 5 * 2 + 1)

    def shift(self, delta_x, delta_y):
        self.hitbox.center = (self.hitbox.centerx - delta_x, self.hitbox.centery - delta_y)
        self.rect.center = self.hitbox.center

