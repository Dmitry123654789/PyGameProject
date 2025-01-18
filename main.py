from logic.field import *
from logic.players import *


class Game:
    def __init__(self):
        self.create_group_sprite()

    def create_group_sprite(self):
        self.player = pygame.sprite.Group()
        Player(64, 32, self.player)

    def update_sprites(self):
        self.player.update(field)

    def draw_sprites(self):
        # field.draw(screen)
        self.player.draw(screen)

    def main(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update_sprites()
            self.draw_sprites()
            pygame.display.flip()
            clock.tick(FPS)

        pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
