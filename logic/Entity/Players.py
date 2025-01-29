import pygame as pg

from logic.Things.ThingGroup import HealthBottle
from logic.Things.Blood import Blood
from logic.seting import WORLD_LAYERS, CELL_SIZE, screen
from logic.support import split_image, load_image
from logic.Entity.Entity import Entity


class Player(Entity):
    """Основной класс игрока"""
    sprites = split_image(load_image('images\\dog_sprites.png'), 32, CELL_SIZE * 2)
    attack_sprites = split_image(load_image('images\\dog_sprites_attack.png'), 32, CELL_SIZE * 2)

    def __init__(self, pos, *group):
        super().__init__(pos, self.sprites, *group)
        self.step = 16  # Количество пройденых пикселей за интервал
        self.damage = 1000
        self.max_hp = 100
        self.hp = self.max_hp

        self.dict_direction = {'down': (0, 1), 'left': (-1, 0), 'right': (1, 0),
                               'up': (0, -1)}  # Направление движения персонажа(x, y)
        self.dict_key = {'down': (pg.K_DOWN, pg.K_s), 'up': (pg.K_UP, pg.K_w), 'right': (pg.K_RIGHT, pg.K_d),
                         'left': (pg.K_LEFT, pg.K_a), 'attack': (pg.K_e, pg.K_SPACE)}  # Действие: клавиши

        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 5 * 2 + 1)  # Хитбокс персонажа
        self.side_rect = 240  # Размер квадрата персонажа
        self.create_player_rect()

        self.going_timer = 0
        self.going_interval = 40  # Частота ходьбы в мл

        self.damage_timer = 0
        self.damage_interval = 250  # Частота получения урона

        self.attack_timer = 0
        self.attack_interval = 80  # Частота анимации атаки в мл
        self.attack = False
        self.attack_hitbox = pg.rect.Rect(0, 0, 0, 0)

        self.z = WORLD_LAYERS['Main']
        self.rect_player = None
        self.image = self.sprites['down']

    def create_player_rect(self):
        """Создания куба персонажа в котором он спокойно перемещаеться"""
        self.rect_player = pg.rect.Rect(screen.get_width() / 2 - self.side_rect / 2,
                                        screen.get_height() / 2 - self.side_rect / 2, self.side_rect, self.side_rect)

    def side(self, key, side):
        """Проверка нажатия клавиши нужного нам направления"""
        return any(key[i] for i in self.dict_key[side])

    def input(self):
        """Отслеживание нажатия клавиш"""
        key = pg.key.get_pressed()

        if self.side(key, 'attack') and not self.attack:
            self.ind_sprite = 0
            self.attack = True

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

    def going(self, group_sprites, step, field, enemies, things_group):
        """Передвижение персонажа"""
        ofset_x_y = (step * self.dict_direction[self.get_stste()][0], step * self.dict_direction[self.get_stste()][1])
        self.shift_player(*ofset_x_y)  # Передвижение персонажа
        if self.collisions(group_sprites):  # Если на нашем пути объект воращаем положение в исходное
            self.shift_player(*map(lambda x: x * -1, ofset_x_y))
            return False

        if not field.update_coord(self.hitbox, *ofset_x_y) and self.inside_react_player(*ofset_x_y):
            self.shift_player(*map(lambda x: x * -1, ofset_x_y))
            # Передвигаем все спрайты на поле

            enemies.shift(*ofset_x_y)
            field.shift_sprites(*ofset_x_y)
            things_group.shift(*ofset_x_y)
        return True

    def inside_react_player(self, delta_x, delta_y):
        """Находится ли персонаж в своем квадрате"""
        if not ((delta_x > 0 and self.hitbox.right > self.rect_player.right) or
                (delta_x < 0 and self.hitbox.left < self.rect_player.left) or
                (delta_y > 0 and self.hitbox.bottom > self.rect_player.bottom) or
                (delta_y < 0 and self.hitbox.top < self.rect_player.top)):
            return False
        return True

    def shift_player(self, delta_x=0, delta_y=0):
        """Сдвиг персонажа на определенную дельту"""
        self.hitbox.center = (self.hitbox.centerx + delta_x, self.hitbox.centery + delta_y)
        self.rect.center = self.hitbox.center

    def is_attack(self):
        """Проверка, пришло ли время смены анимации атаки"""
        tick = pg.time.get_ticks()
        if tick - self.attack_timer >= self.attack_interval:
            self.attack_timer = tick
            return True
        return False

    def is_damage(self):
        """Проверка, пришло ли время получения урона"""
        tick = pg.time.get_ticks()
        if tick - self.damage_timer >= self.damage_interval:
            return True
        return False

    def attacking(self, field, enemies, draw_obj):
        """Атака"""
        self.image = self.attack_sprites[self.get_stste()][self.ind_sprite]
        self.ind_sprite += 1
        if self.ind_sprite == len(self.attack_sprites[self.get_stste()]):
            self.attack = False
            self.attack_hitbox = self.hitbox.inflate(abs(self.hitbox.width * self.dict_direction[self.get_stste()][0]),
                                                     abs(self.hitbox.height * self.dict_direction[self.get_stste()][1]))
            # self.attack_hitbox = self.hitbox.inflate(10000000, 10000000)
            self.attack_hitbox.x += self.hitbox.width / 2 * self.dict_direction[self.get_stste()][0]
            self.attack_hitbox.y += self.hitbox.height / 2 * self.dict_direction[self.get_stste()][1]
            self.collisions_enemy_attack(enemies, draw_obj, field)
            self.damage_timer = pg.time.get_ticks()

    def collisions_enemy_attack(self, group_sprites, draw_obj, field):
        """Проверка коллизии хитбокса атаки"""
        for obj in group_sprites:
            if obj.hitbox.colliderect(self.attack_hitbox):
                obj.hp -= self.damage
                Blood(obj.hitbox.center, draw_obj, field)

    def collisions_enemy(self, group_sprites, draw_obj, field):
        for obj in group_sprites:
            if obj.hitbox.colliderect(self.hitbox):
                self.hp -= obj.damage
                self.hp = max(self.hp, 0)
                self.damage_timer = pg.time.get_ticks()
                Blood(self.hitbox.center, draw_obj, field)

    def collision_health_bottle(self, group):
        for obj in group:
            if not isinstance(obj, HealthBottle):
                continue
            if obj.hitbox.colliderect(self.hitbox):
                self.hp += obj.health
                self.hp = min(self.hp, self.max_hp)
                obj.health = 0

    def update(self, group_sprites, field, enemies, draw_obj, things_group):
        """Обновление положение персонажа"""
        self.collision_health_bottle(things_group)
        if self.attack:
            if self.is_attack():
                self.attacking(field, enemies, draw_obj)
                self.going(group_sprites,
                           (self.hitbox.width if self.get_stste() in ['right', 'left'] else self.hitbox.height) / 6,
                           field, enemies, things_group)

        else:
            if self.is_damage():
                self.collisions_enemy(enemies, draw_obj, field)
            if self.input() and self.is_going():
                if self.is_animated():
                    self.animate(self.get_stste())
                for step in range(self.step, 0, -1):
                    if self.going(group_sprites, step, field, enemies, things_group):
                        return
