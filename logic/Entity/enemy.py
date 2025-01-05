import pygame as pg
from logic.seting import WORLD_LAYERS, CELL_SIZE, screen, split_image, load_image
from logic.Entity.entity import Entity


class Enemy(Entity):
    sprites = None
    def __init__(self, pos, *group):
        super().__init__(pos, self.sprites, *group)
        self.image = load_image('Texture/barrel.png')
        self.rect = self.image.get_rect()