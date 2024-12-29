import pygame

from logic.seting import screen


class Tile(pygame.sprite.Sprite):
    """Клас клетки хранит изображение"""
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


    def set_darkness(self):
        """Затемнение"""
        darkness = pygame.Surface(self.rect.size)
        darkness.fill(pygame.Color('black'))
        darkness.set_alpha(100)
        self.image.blit(darkness, (0, 0))


class TileObject(pygame.sprite.Sprite):
    """Клас клетки хранит только полигон(хитбокс)"""
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(*pos, *size)
