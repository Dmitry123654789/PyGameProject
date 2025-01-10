import pygame

from logic.Things.Thing import Thing
from logic.seting import load_image, CELL_SIZE


class HealthBottle(Thing):
    sprite = pygame.transform.scale(load_image('images/bottle.png'), (CELL_SIZE, CELL_SIZE))

    def __init__(self, pos, *group):
        super().__init__(pos, self.sprite, *group)
        self.health = 15

    def update(self, player_group):
        if self.health == 0:
            self.kill()
