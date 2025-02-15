import pygame

from logic.seting import WORLD_LAYERS


class Entity(pygame.sprite.Sprite):
    """Начальный класс любой сущности"""

    def __init__(self, pos, sprites, *group):
        super().__init__(*group)
        self.direction = 0  # down, left, right, up
        self.image = sprites['right'][1]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect
        self.sprites = sprites
        self.str_direction = {0: 'down', 1: 'left', 2: 'right', 3: 'up'}

        self.ind_sprite = 0
        self.animation_timer = 0
        self.animation_interval = 43  # Частота анимации ходьбы в мл

        self.going_timer = 0
        self.going_interval = 40  # Частота ходьбы в мл

        self.z = WORLD_LAYERS['Main']

        self.max_hp = 100
        self.hp = self.max_hp

    def collisions(self, group_sprites):
        """Проверка коллизии нащего хитбокса"""
        for obj in group_sprites:
            if obj.hitbox.colliderect(self.hitbox):
                return True
        return False

    def animate(self, state):
        """Изменяет текущий спрайт"""
        self.ind_sprite += 1
        self.ind_sprite %= len(self.sprites[state])
        self.image = self.sprites[state][self.ind_sprite]

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

    def is_going(self):
        """Проверка, пришло ли время ходьбы"""
        tick = pygame.time.get_ticks()
        if tick - self.going_timer >= self.going_interval:
            self.going_timer = tick
            return True
        return False
