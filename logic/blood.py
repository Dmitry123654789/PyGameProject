import pygame

from logic.seting import load_image, WORLD_LAYERS, CELL_SIZE


def get_sprites(img):
    sprites = []
    for x in range(6):
        sprites.append(pygame.transform.scale(img.subsurface(pygame.rect.Rect(32 * x, 0, 32, 32)), (CELL_SIZE * 2, CELL_SIZE * 2)))
    return sprites


class Blood(pygame.sprite.Sprite):
    sprites = get_sprites(load_image('images/blood.png'))
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect

        self.blood_interval = 50
        self.blood_ind = 0
        self.blood_timer = pygame.time.get_ticks()

        self.z = WORLD_LAYERS['Down_sprites']



    def shift(self, delta_x, delta_y):
        self.hitbox.center = (self.hitbox.centerx - delta_x, self.hitbox.centery - delta_y)
        self.rect.center = self.hitbox.center

    def update(self):
        if self.blood_ind == len(self.sprites):
            self.image = pygame.surface.Surface((0, 0))
            return

        if pygame.time.get_ticks() - self.blood_interval > self.blood_timer:
            self.image = self.sprites[self.blood_ind]
            self.blood_ind += 1
            # if self.blood_ind == len(self.sprites) - 2:
            #     self.blood_interval = 500
            self.blood_timer = pygame.time.get_ticks()

