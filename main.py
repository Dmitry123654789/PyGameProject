import pygame

from logic.field import *
from logic.players import *
from logic.menu import *


class Game:
    def __init__(self):
        # self.create_group_sprite()
        self.current_scene = None

    def create_group_sprite(self):
        self.player = pygame.sprite.Group()
        Player(64, 32, self.player)

    def update_sprites(self):
        self.player.update(field)

    def draw_sprites(self):
        # field.draw(screen)
        self.player.draw(screen)

    # функция для переключения сцены
    def switch_scene(self, scene):
        self.current_scene = scene
        self.main()

    def main(self):

        # переключает сцены
        # if self.current_scene is menu_scene:
        #     self.switch_scene(menu_scene)
        # if self.current_scene is setting_scene:
        #     self.switch_scene()
        # elif self.current_scene is game_scene
        if self.current_scene is None:
            pygame.quit()
        else:
            # запуск текущей сцены
            self.current_scene()

    # while running:
    #     screen.fill(pygame.Color('black'))
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #     self.update_sprites()
    #     self.draw_sprites()
    #     pygame.display.flip()
    #     clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.switch_scene(menu_scene)
