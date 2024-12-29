import pygame as pg
from logic.field.field import *


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
        self.animation_interval = 10
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
    def __init__(self, pos, sprites, *group):
        super().__init__(pos, sprites, *group)
        self.step = 1 # Количество ходов за одно нажатие клавиши
        self.dict_direction = {0: (0, 1), 1: (-1, 0), 2: (1, 0), 3: (0, -1)} # Направление движения персонажа
        self.dict_key = {'down': (pg.K_DOWN, pg.K_s), 'up': (pg.K_UP, pg.K_w), 'right': (pg.K_RIGHT, pg.K_d),
                         'left': (pg.K_LEFT, pg.K_a)}

        self.vect = 'horizontal'
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 5 * 2)
        # self.vect_hitbox()
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
            if self.vect == 'horizontal':
                self.vect = 'vertical'
                self.vect_hitbox()
            self.direction = 3
        elif self.side(key, 'down'):
            if self.vect == 'horizontal':
                self.vect = 'vertical'
                self.vect_hitbox()
            self.direction = 0
        elif self.side(key, 'right'):
            if self.vect == 'vertical':
                self.vect = 'horizontal'
                self.vect_hitbox()
            self.direction = 2
        elif self.side(key, 'left'):
            self.direction = 1
            if self.vect == 'vertical':
                self.vect = 'horizontal'
                self.vect_hitbox()
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
        if not field.update_coord(self.hitbox, self.rect_player, *ofset_x_y):
            self.hitbox.center = (self.hitbox.centerx - ofset_x_y[0], self.hitbox.centery - ofset_x_y[1])
        self.rect.center = self.hitbox.center
        return True

    def collisions(self, group_sprites):
        """Проверка коллизии нащего хитбокса"""
        for obj in group_sprites:
            if obj.rect.colliderect(self.hitbox):
                return True
        return False

    def vect_hitbox(self):
        """Поворот хитбокса, взависимости от направления"""
        # if self.vect == 'horizontal':
        #     self.hitbox = self.rect.inflate(-self.rect.width / 5, -self.rect.height / 5 * 2)
        # else:
        #     self.hitbox = self.rect.inflate(-self.rect.width / 1.8, -self.rect.height / 5 * 2)


    def update(self, group_sprites, field):
        """Обновление положение персонажа"""
        if self.input() and self.is_animated():
            self.animate()
            for step in range(self.step, 0, -1):
                if self.going(group_sprites, step, field):
                    break
