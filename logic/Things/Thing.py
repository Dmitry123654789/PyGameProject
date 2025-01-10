import pygame

from logic.seting import WORLD_LAYERS


class Thing(pygame.sprite.Sprite):
    def __init__(self, pos, image, *group):
        super().__init__(*group)
        self.image = image
        self.z = WORLD_LAYERS['Main']
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect

    def shift(self, delta_x, delta_y):
        self.hitbox.center = (self.hitbox.centerx - delta_x, self.hitbox.centery - delta_y)
        self.rect.center = self.hitbox.center
