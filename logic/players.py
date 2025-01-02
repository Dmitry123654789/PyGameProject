import pygame as pg
from logic.seting import *


class Entity(pg.sprite.Sprite):
    """Начальный класс любой сущности"""
    def __init__(self, pos, sprites, *group):
        super().__init__(*group)
        self.direction = 0  # down, left, right, up
        self.image = sprites['right'][1]
        self.rect = self.image.get_rect(center=pos)
        self.sprites = sprites
        self.str_direction = {0: 'down', 1: 'left', 2: 'right', 3: 'up'}

        self.ind_sprite = 0
        self.animation_timer = 0
        self.animation_interval = 43 # Частота анимации ходьбы в мл

    def animate(self):
        """Изменяет текущий спрайт"""
        self.ind_sprite += 1
        self.ind_sprite %= len(self.sprites[self.get_stste()])
        self.image = self.sprites[self.get_stste()][self.ind_sprite]

    def is_animated(self):
        """Проверка, пришло ли время анимации ходьбы"""
        tick = pygame.time.get_ticks()
        if tick - self.animation_timer >= self.animation_interval:
            self.animation_timer = tick
            return True
        return False

    def get_stste(self):
        """Получение направления(down, left, right, up)"""
        return self.str_direction[self.direction]


class Player(Entity):
    """Основной класс игрока"""
    sprites = split_image(load_image('images/dog_sprites.png'), 32, CELL_SIZE)
    attack_sprites = split_image(load_image('images/dog_sprites_attack.png'), 32, CELL_SIZE)
    def __init__(self, pos, *group):
        super().__init__(pos, self.sprites, *group)
        self.step = 8 # Количество пройденых пикселей за интервал
        self.dict_direction = {'down': (0, 1), 'left': (-1, 0), 'right': (1, 0), 'up': (0, -1)} # Направление движения персонажа(x, y)
        self.dict_key = {'down': (pg.K_DOWN, pg.K_s), 'up': (pg.K_UP, pg.K_w), 'right': (pg.K_RIGHT, pg.K_d),
                         'left': (pg.K_LEFT, pg.K_a), 'attack' : (pg.K_e, pg.K_SPACE)} # Действие: клавиши

        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 5 * 2 + 1) # Хитбокс персонажа
        self.side_rect = 240 # Размер квадрата персонажа
        self.create_player_rect()

        self.going_timer = 0
        self.going_interval = 40 # Частота ходьбы в мл

        self.attack_timer = 0
        self.attack_interval = 80 # Частота анимации атаки в мл
        self.attack = False


    def create_player_rect(self):
        """Создания куба персонажа в котором он спокойно перемещаеться"""
        self.rect_player = pg.rect.Rect(screen.get_size()[0] / 2 - self.side_rect / 2,
                                        screen.get_size()[1] / 2 - self.side_rect / 2, self.side_rect, self.side_rect)

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

    def going(self, group_sprites, step, field):
        """Передвижение персонажа"""
        ofset_x_y = (step * self.dict_direction[self.get_stste()][0], step * self.dict_direction[self.get_stste()][1])
        self.shift_player(*ofset_x_y) # Передвижение персонажа
        if self.collisions(group_sprites): # Если на нашем пути объект воращаем положение в исходное
            self.shift_player(*map(lambda x: x * -1, ofset_x_y))
            return False

        if not field.update_coord(self.hitbox, *ofset_x_y) and self.inside_react_player(*ofset_x_y):
            self.shift_player(*map(lambda x: x * -1, ofset_x_y))
            # Передвигаем все спрайты на поле
            field.shift_sprites(*ofset_x_y)
        return True
    
    def inside_react_player(self, delta_x, delta_y):
        """Находится ли персонаж в своем квадрате"""
        if not ((delta_x > 0 and self.hitbox.right > self.rect_player.right) or
                (delta_x < 0 and self.hitbox.left < self.rect_player.left) or
                (delta_y > 0 and self.hitbox.bottom > self.rect_player.bottom) or
                (delta_y < 0 and self.hitbox.top < self.rect_player.top)):
            return False
        return True

    def collisions(self, group_sprites):
        """Проверка коллизии нащего хитбокса"""
        for obj in group_sprites:
            if obj.rect.colliderect(self.hitbox):
                return True
        return False

    def shift_player(self, delta_x=0, delta_y=0):
        """Сдвиг персонажа на определенную дельту"""
        self.hitbox.center = (self.hitbox.centerx + delta_x, self.hitbox.centery + delta_y)
        self.rect.center = self.hitbox.center

    def is_going(self):
        """Проверка, пришло ли время ходьбы"""
        tick = pygame.time.get_ticks()
        if tick - self.going_timer >= self.going_interval:
            self.going_timer = tick
            return True
        return False

    def is_attack(self):
        """Проверка, пришло ли время смены анимации атаки"""
        tick = pygame.time.get_ticks()
        if tick - self.attack_timer >= self.attack_interval:
            self.attack_timer = tick
            return True
        return False

    def attacking(self, group_sprites, field):
        """Атака"""
        self.image = self.attack_sprites[self.get_stste()][self.ind_sprite]
        self.going(group_sprites, self.hitbox.width / 6, field) # Передвигаем немного спрайт
        self.ind_sprite += 1
        if self.ind_sprite == len(self.attack_sprites[self.get_stste()]):
            self.attack = False

    def update(self, group_sprites, field):
        """Обновление положение персонажа"""
        if self.attack:
            if self.is_attack():
                self.attacking(group_sprites, field)
        else:
            if self.input() and self.is_going():
                if self.is_animated():
                    self.animate()
                for step in range(self.step, 0, -1):
                    if self.going(group_sprites, step, field):
                            break
