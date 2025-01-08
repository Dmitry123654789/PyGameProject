import pygame
from random import randint
from logic.seting import CELL_SIZE, WORLD_LAYERS, load_image


class Things(pygame.sprite.Group):
    def __init__(self, tmx_map, draw_group):
        super().__init__()
        self.add_things(tmx_map, draw_group)

    def add_things(self, draw_group, tmx_map):
        for obj in tmx_map.get_layer_by_name('Points_bottle'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            if randint(0, 1) == 1:
                HealthBottle(pos, draw_group, self)

    def shift(self, delta_x, delta_y):
        for sprite in self:
            sprite.shift(delta_x, delta_y)

    def update(self, player_group):
        for sprite in self:
            sprite.update(player_group)


class HealthBottle(pygame.sprite.Sprite):
    sprite = pygame.transform.scale(load_image('images/bottle.png'), (CELL_SIZE, CELL_SIZE))
    def __init__(self, pos, *group):
        super().__init__(*group)
        self.z = WORLD_LAYERS['Main']
        self.image = self.sprite
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect
        self.health = 15

    def shift(self, delta_x, delta_y):
        self.hitbox.center = (self.hitbox.centerx - delta_x, self.hitbox.centery - delta_y)
        self.rect.center = self.hitbox.center

    def update(self, player_group):
        if self.health == 0:
            self.kill()

