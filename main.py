from logic.field import *
from logic.players import *


class Game:
    def __init__(self):
        self.player = pygame.sprite.Group()
        self.field = Field()
        self.draw_field = pygame.sprite.Group()
        self.collision_sprite = pygame.sprite.Group()
        self.add_group_sprite()

    def add_group_sprite(self):
        self.p = Player((screen.get_size()[0] / 2, screen.get_size()[1] / 2), split_image(load_image('images/dog_sprites.png'), 32, CELL_SIZE), self.player)
        self.field.create_field(self.collision_sprite, self.draw_field)


    def update_sprites(self):
        # self.field.update()
        self.player.update(self.collision_sprite, self.field)

    def draw_sprites(self):
        self.draw_field.draw(screen)
        self.player.draw(screen)

    def main(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.draw.rect(screen, pygame.Color('black'), self.p.rect_player)
            self.update_sprites()
            self.draw_sprites()

            pygame.display.flip()
            clock.tick(FPS)

        pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
