import pygame as pg
from random import randint

from logic.seting import WORLD_LAYERS, CELL_SIZE, screen, split_image, load_image, WIDTH, HEIGHT
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

    def update(self, pos, collision_group):
        for sprite in self:
            sprite.update(pos, collision_group)


class Enemy(Entity):
    sprites = split_image(load_image('images/dog_sprites.png'), 32, CELL_SIZE * 2)
    def __init__(self, pos, *group):
        super().__init__(pos, self.sprites, *group)
        self.step = 4
        self.max_hp = 100
        self.hp = self.max_hp
        self.damage = 10

        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 5 * 2 + 1)
        self.dict_direct = self.dict_direction = {(0, 1): 'down', (-1, 0) : 'left', (1, 0): 'right',
                               (0, -1): 'up'}

    def shift(self, delta_x, delta_y):
        self.hitbox.centerx -= delta_x
        self.hitbox.centery -= delta_y
        self.rect.center = self.hitbox.center

    def shifting(self, delta_x, delta_y, group_sprites):
        is_direct = []
        self.shift(delta_x, 0)
        is_direct.append(self.collisions(group_sprites))
        self.shift(-delta_x, 0)

        self.shift(0, delta_y)
        is_direct.append(self.collisions(group_sprites))
        self.shift(0, -delta_y)

        direct = [delta_x, delta_y]

        for i in range(2):
            if is_direct[i]:
                direct[i] = 0

        if direct[0] == direct[1] == 0:
            return

        if 0 not in direct:
            direct[randint(0, 1)] = 0

        self.shift(*direct)
        self.animate(self.dict_direct[self.set_one(direct)])

    def set_one(self, list):
        for i in range(2):
            if list[i] > 0:
                list[i] = -1
            elif list[i] < 0:
                list[i] = 1
            else:
                list[i] = 0
        return tuple(list)

    def input(self, pos):
        direct = []
        for coord, center in zip(pos, self.hitbox.center):
            if coord > center:
                direct.append(-1 * randint(1, self.step))
            elif coord < center:
                direct.append(1 * randint(1, self.step))
            else:
                direct.append(0)


        return direct


    def update(self, pos, collision_group):
        if 0 <= self.hitbox.centerx <= screen.get_width() and 0 <= self.hitbox.centery <= screen.get_height():
            self.shifting(*self.input(pos), collision_group)
