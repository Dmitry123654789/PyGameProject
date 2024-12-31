import pygame as pg
from logic.seting import *


class Entity(pg.sprite.Sprite):
    """"""
    def __init__(self, pos, sprites, *group):
        super().__init__(*group)
        self.ind_sprite = 0
        self.direction = 0  # down, left, right, up
        self.image = sprites['right'][1]
        self.rect = self.image.get_rect(center=pos)
        self.sprites = sprites
        self.animation_timer = 0
        self.animation_interval = 40
        self.str_direction = {0: 'down', 1: 'left', 2: 'right', 3: 'up'}

    def animate(self):
        self.ind_sprite += 1
        self.ind_sprite %= len(self.sprites[self.get_stste()])
        self.image = self.sprites[self.get_stste()][self.ind_sprite]

    def is_animated(self):
        tick = pygame.time.get_ticks()
        if tick - self.animation_timer >= self.animation_interval:
            self.animation_timer = tick
            return True

        return False

    def get_stste(self):
        return self.str_direction[self.direction]


class Player(Entity):
    """Основной класс игрока"""
    sprites = split_image(load_image('images/dog_sprites.png'), 32, CELL_SIZE)
    attack_sprites = split_image(load_image('images/dog_sprites_attack.png'), 32, CELL_SIZE)
    def __init__(self, pos, *group):
        super().__init__(pos, self.sprites, *group)
        self.step = 8 # Количество ходов за одно нажатие клавиши
        self.dict_direction = {0: (0, 1), 1: (-1, 0), 2: (1, 0), 3: (0, -1)} # Направление движения персонажа
        self.dict_key = {'down': (pg.K_DOWN, pg.K_s), 'up': (pg.K_UP, pg.K_w), 'right': (pg.K_RIGHT, pg.K_d),
                         'left': (pg.K_LEFT, pg.K_a)}

        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 5 * 2 + 1)
        self.side_rect = 120 # Размер квадрата персонажа
        self.create_player_rect()
        
    def create_player_rect(self):
        self.rect_player = pg.rect.Rect(screen.get_size()[0] / 2 - self.side_rect / 2,
                                        screen.get_size()[1] / 2 - self.side_rect / 2, self.side_rect, self.side_rect)

    def side(self, key, side):
        """Проверка нажатия клавиши нужного нам направления"""
        return any(key[i] for i in self.dict_key[side])

    def input(self):
        """Отслеживание нажатия клавиш"""
        key = pg.key.get_pressed()
        if self.side(key, 'up'):
            self.direction = 3
        elif self.side(key, 'down'):
            self.direction = 0
        elif self.side(key, 'right'):
            self.direction = 2
        elif self.side(key, 'left'):
            self.direction = 1
        else:
            self.image = self.sprites[self.get_stste()][1]
            return False
        return True

    def going(self, group_sprites, step, field):
        ofset_x_y = (step * self.dict_direction[self.direction][0], step * self.dict_direction[self.direction][1])
        self.hitbox.center = (self.hitbox.centerx + ofset_x_y[0], self.hitbox.centery + ofset_x_y[1])
        if self.collisions(group_sprites):
            self.hitbox.center = (self.hitbox.centerx - ofset_x_y[0], self.hitbox.centery - ofset_x_y[1])
            return False

        res = field.update_coord(self.hitbox, self.rect_player, *ofset_x_y)
        if res == 0:
            self.hitbox.center = (self.hitbox.centerx - ofset_x_y[0], self.hitbox.centery - ofset_x_y[1])
        elif res == 2:
            self.rect.center = self.hitbox.center
            return False
        self.rect.center = self.hitbox.center
        return True

    def collisions(self, group_sprites):
        """Проверка коллизии нащего хитбокса"""
        for obj in group_sprites:
            if obj.rect.colliderect(self.hitbox):

                return True
        return False

    def shift_player(self, delta_x, delta_y):
        self.hitbox.center = (self.hitbox.centerx + delta_x, self.hitbox.centery + delta_y)
        self.rect.center = self.hitbox.center


    def update(self, group_sprites, field):
        """Обновление положение персонажа"""
        if self.input() and self.is_animated():
            self.animate()
            for step in range(self.step, 0, -1):
                if self.going(group_sprites, step, field):
                        break
