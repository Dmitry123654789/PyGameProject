import pygame


class Tile(pygame.sprite.Sprite):
    """Клас клетки, хранит изображение"""
    def __init__(self, pos, surf, z, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


    def set_darkness(self):
        """Затемнение"""
        darkness = pygame.Surface(self.rect.size)
        darkness.fill(pygame.Color('black'))
        darkness.set_alpha(100)
        self.image.blit(darkness, (0, 0))

    def shift(self, delta_x, delta_y):
        self.rect.center = (self.rect.centerx - delta_x, self.rect.centery - delta_y)

class TileObject(pygame.sprite.Sprite):
    """Клас клетки, хранит только полигон(хитбокс)"""
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(*pos, *size)
        self.hitbox = self.rect

    def shift(self, delta_x, delta_y):
        self.rect.center = (self.rect.centerx - delta_x, self.rect.centery - delta_y)