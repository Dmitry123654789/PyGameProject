from random import randint, choices

import pygame as pg

from logic.Game.Entity.Entity import Entity
from logic.seting import CELL_SIZE, screen, ENEMY
from logic.support import split_image, load_image


class EnemiesGroup(pg.sprite.Group):
    """Группа спрайтов содержащая врагов"""

    def __init__(self, draw_group, tmx_map):
        super().__init__()
        self.add_enemy(draw_group, tmx_map)

    def add_enemy(self, draw_group, tmx_map):
        """Добавление всех врагов"""
        for obj in tmx_map.get_layer_by_name('Points'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            Enemy(pos, draw_group, self)

    def shift(self, delta_x, delta_y):
        """Сдвиг всех спрайтов на определенную дельту"""
        for sprite in self:
            sprite.shift(delta_x, delta_y)

    def update(self, pos, collision_group, player_group):
        """Обновление группы спрайтов"""
        for sprite in self:
            sprite.update(pos, collision_group, player_group)


class Enemy(Entity):
    """Класс врага"""

    def __init__(self, pos, *group):
        color = choices(list(ENEMY.keys()), weights=[ENEMY[i][3] for i in ENEMY.keys()])[
            0]  # Цвет врвга, от этого зависят его характеристи
        self.sprites = split_image(load_image(f'images\\dog_sprites\\{color}.png'), 32, CELL_SIZE * 2)
        self.attack_sprites = split_image(load_image(f'images\\dog_sprites\\attack_{color}.png'), 32, CELL_SIZE * 2)
        super().__init__(pos, self.sprites, *group)
        self.step = ENEMY[color][0]
        self.max_hp = ENEMY[color][1]
        self.hp = self.max_hp
        self.damage = ENEMY[color][2]

        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 5 * 2 + 1)
        self.dict_direct = {(0, 1): 'down', (-1, 0): 'left', (1, 0): 'right',
                            (0, -1): 'up'}

        self.steps_required = 6  # Минимум шагов перед сменой направления
        self.steps_made = 0  # Шагов сделано в одном направлени
        self.current_direction = None  # Нынешнее направление
        self.attack = False

        self.attack_timer = 0
        self.attack_interval = 80  # Частота анимации атаки в мл

    def shift(self, delta_x, delta_y):
        """Сдвишг персонажа на определенную делльту"""
        self.hitbox.centerx -= delta_x
        self.hitbox.centery -= delta_y
        self.rect.center = self.hitbox.center

    def going(self, delta_x, delta_y, group_sprites):
        """Обработка ходьбы врага"""
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

        self.shift(*direct)
        self.animate(self.dict_direct[self.set_one(direct)])

    def set_one(self, list):
        """Узнаем направление в котором движемся"""
        for i in range(2):
            if list[i] > 0:
                list[i] = -1
            elif list[i] < 0:
                list[i] = 1
            else:
                list[i] = 0
        return tuple(list)

    def input(self, pos):
        """Задаем направление для движения"""
        # Проверяем можно ли сменить направление
        if self.current_direction is None or self.steps_made >= self.steps_required:
            self.steps_made = 0
            direct = []
            for coord, center in zip(pos, self.hitbox.center):
                if coord > center:
                    direct.append(-1)
                elif coord < center:
                    direct.append(1)
                else:
                    direct.append(0)

            if 0 not in direct:
                direct[randint(0, 1)] = 0

            self.current_direction = direct

        self.steps_made += 1

        return self.current_direction

    def is_attack(self):
        """Проверка, пришло ли время смены анимации атаки"""
        tick = pg.time.get_ticks()
        if tick - self.attack_timer >= self.attack_interval:
            self.attack_timer = tick
            return True
        return False

    def attacking(self, collision_group):
        """Атака"""
        if self.ind_sprite == 0:
            # Устанавливаем направление атаки только один раз в начале
            self.attack_direction = self.set_one(self.current_direction)

        self.image = self.attack_sprites[self.dict_direct[self.attack_direction]][self.ind_sprite]
        # Проверяем сталкиваемя ли мы с чем то
        if not self.collisions(collision_group):
            self.shift(*map(lambda x: x * -1, self.attack_direction))
        else:
            self.image = self.attack_sprites[self.dict_direct[self.attack_direction]][1]
        self.ind_sprite += 1
        if self.ind_sprite == len(self.attack_sprites[self.dict_direct[self.attack_direction]]):
            self.ind_sprite = 0
            self.attack = False

    def update(self, pos, collision_group, player_group):
        """Обновляем персонажа"""
        # Удоляем класс если здоровье упало до нуля
        if self.hp <= 0:
            self.kill()
            return

        # Атакуем если мы столкнулись с персонажем
        if self.collisions(player_group) and not self.attack:
            self.attack = True
            self.ind_sprite = 0

        if self.attack:
            if self.is_attack():
                self.attacking(collision_group)
        else:
            # Только если враг не атакует, вычисляем новое направление и движемся
            if self.is_going() and self.is_animated():
                if 0 <= self.hitbox.centerx <= screen.get_width() and 0 <= self.hitbox.centery <= screen.get_height():
                    self.going(*map(lambda x: x * randint(1, self.step), self.input(pos)), collision_group)
