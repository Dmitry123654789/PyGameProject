import pygame

from logic.Game.Things.Thing import Thing
from logic.seting import CELL_SIZE
from logic.support import load_image


class HealthBottle(Thing):
    """Класс бутылка восполняющей здоровье"""
    sprite = pygame.transform.scale(load_image('images\\bottle.png'), (CELL_SIZE, CELL_SIZE))

    def __init__(self, pos, *group):
        super().__init__(pos, self.sprite, *group)
        self.health = 15 # То на сколько лечится игрок

    def update(self, player_group):
        if self.health == 0:
            self.kill()
