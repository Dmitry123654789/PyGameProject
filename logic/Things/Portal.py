import pygame

from logic.Things.Thing import Thing
from logic.seting import load_image, CELL_SIZE, WORLD_LAYERS


class Portal(Thing):
    """Класс портала"""
    sprite = pygame.transform.scale(load_image('images\\portal_2.png'), ((CELL_SIZE / 100) * (94 / (16 / 100)), (CELL_SIZE / 100) * (72 / (16 / 100))))
    def __init__(self, pos, *group):
        super().__init__(pos, self.sprite, *group)
        self.z = WORLD_LAYERS['Down_sprites']
        self.image.set_alpha(0)
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 2)


    def update(self, enemy_group):
        # Портал появляется если все враги мертвы
        if len(enemy_group) == 0:
            self.image.set_alpha(255)