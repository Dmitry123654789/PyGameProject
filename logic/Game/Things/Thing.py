import pygame

from logic.seting import CELL_SIZE
from logic.seting import WORLD_LAYERS
from logic.support import load_image


class Thing(pygame.sprite.Sprite):
    """Начальный класс любой вещи"""

    def __init__(self, pos, image, *group):
        super().__init__(*group)
        self.image = image
        self.z = WORLD_LAYERS['Main']
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect

    def shift(self, delta_x, delta_y):
        # Сдвиг объекта на какую-то дельту
        self.hitbox.center = (self.hitbox.centerx - delta_x, self.hitbox.centery - delta_y)
        self.rect.center = self.hitbox.center


class Portal(Thing):
    """Класс портала"""
    sprite = pygame.transform.scale(load_image('images\\portal_2.png'),
                                    ((CELL_SIZE / 100) * (94 / (16 / 100)), (CELL_SIZE / 100) * (72 / (16 / 100))))

    def __init__(self, pos, *group):
        super().__init__(pos, self.sprite, *group)
        self.z = WORLD_LAYERS['Down_sprites']
        self.image.set_alpha(0)
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 2)

    def update(self, enemy_group):
        # Портал появляется если все враги мертвы
        if len(enemy_group) == 0:
            self.image.set_alpha(255)


class HealthBottle(Thing):
    """Класс бутылка восполняющей здоровье"""
    sprite = pygame.transform.scale(load_image('images\\bottle.png'), (CELL_SIZE, CELL_SIZE))

    def __init__(self, pos, *group):
        super().__init__(pos, self.sprite, *group)
        self.health = 15  # То на сколько лечится игрок

    def update(self, player_group):
        if self.health == 0:
            self.kill()
