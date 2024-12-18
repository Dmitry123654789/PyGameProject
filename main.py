from logic.seting import *
from logic.players import *
import pygame


class Game:
    def __init__(self):
        self.create_group_sprite()

    def create_group_sprite(self):
        self.player = pygame.sprite.Group()
        Player(32, 32, self.player)

    def main(self):

        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill(pygame.Color('black'))
            events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                events.append(event)


            self.player.update(pygame.time.get_ticks(), events)
            self.player.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
