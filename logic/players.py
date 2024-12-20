import pygame as pg

from logic.seting import *


class Player(pg.sprite.Sprite):
    image = load_image("images/dog_sprites.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lst_sprites = []
        for i in range(8):
            self.lst_sprites.append(split_image_to_surfaces(self.image, 32, CELL_SIZE, 11, i, 5))

        self.ind_sprite = 0
        self.animation_timer = 0
        self.animation_interval = 50
        self.step = 8
        self.dict_direction = {0: (0, 1), 1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (-1, 1), 5: (-1, -1), 6: (1, 1), 7: (1, -1)}
        self.direction = 2 # down, left, right, up, left_down, left_up, right_down, right_up
        self.go = False
        self.dict_key = {'down': (pg.K_DOWN, pg.K_s), 'up': (pg.K_UP, pg.K_w), 'right': (pg.K_RIGHT, pg.K_d), 'left': (pg.K_LEFT, pg.K_a)}

    def side(self, key, side):
        return any(key[i] for i in self.dict_key[side])

    def input(self):
        self.go = True
        key = pg.key.get_pressed()
        if self.side(key, 'up') and self.side(key, 'right'):
            self.direction = 7
        elif self.side(key, 'up') and self.side(key, 'left'):
            self.direction = 5
        elif self.side(key, 'down') and self.side(key, 'left'):
            self.direction = 4
        elif self.side(key, 'down') and self.side(key, 'right'):
            self.direction = 6
        elif self.side(key, 'up'):
            self.direction = 3
        elif self.side(key, 'down'):
            self.direction = 0
        elif self.side(key, 'right'):
            self.direction = 2
        elif self.side(key, 'left'):
            self.direction = 1
        else:
            self.go = False
            self.image = self.lst_sprites[self.direction][1]

        if self.go:
            self.image = self.lst_sprites[self.direction][self.ind_sprite]
            self.rect.x += self.step * self.dict_direction[self.direction][0]
            self.rect.y += self.step * self.dict_direction[self.direction][1]

    def update(self, tick):
        if tick - self.animation_timer >= self.animation_interval:
            self.ind_sprite += 1
            self.ind_sprite %= len(self.lst_sprites[0])
            self.animation_timer = tick
            self.input()


