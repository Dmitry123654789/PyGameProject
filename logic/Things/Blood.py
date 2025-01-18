import pygame

from logic.seting import load_image, WORLD_LAYERS, CELL_SIZE
from logic.Things.Thing import Thing

def get_sprites(img):
    sprites = []
    for x in range(6):
        sprites.append(
            pygame.transform.scale(img.subsurface(pygame.rect.Rect(32 * x, 0, 32, 32)), (CELL_SIZE * 2, CELL_SIZE * 2)))
    return sprites


class Blood(Thing):
    sprites = get_sprites(load_image('images\\blood.png'))

    def __init__(self, pos, *groups):
        super().__init__(pos, self.sprites[0], *groups)
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect

        self.blood_interval = 50
        self.blood_ind = 0
        self.blood_timer = pygame.time.get_ticks()

        self.z = WORLD_LAYERS['Down_sprites']

    def update(self):
        if self.blood_ind == len(self.sprites) - 1:
            self.kill()

        if pygame.time.get_ticks() - self.blood_interval > self.blood_timer:
            self.image = self.sprites[self.blood_ind]
            self.blood_ind += 1
            self.blood_timer = pygame.time.get_ticks()
