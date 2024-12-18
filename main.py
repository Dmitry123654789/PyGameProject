from logic.field import *
from logic.players import *


class Game:
    def __init__(self):
        self.create_group_sprite()

    def create_group_sprite(self):
        self.player = pygame.sprite.Group()
        Player(32, 32, self.player)

        self.field = Field()

    def main(self):

        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.field.update()
            self.player.update(pygame.time.get_ticks())
            self.player.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
