from logic.field import *
from logic.players import *


class Game:
    def __init__(self):
        self.player = pygame.sprite.Group()
        self.collision_sprite = pygame.sprite.Group()
        self.add_player_group_sprite()
        self.add_group_sprite()

    def add_player_group_sprite(self):
        Player((64, 32), split_image(load_image('images/dog_sprites.png'), 32, CELL_SIZE), self.player)

    def add_group_sprite(self):
        self.field = Field()
        for layer in tmx_map.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * CELL_SIZE, y * CELL_SIZE)
                    Tile(pos, pygame.transform.scale(surf, (CELL_SIZE, CELL_SIZE)), self.field)

        for obj in tmx_map.objects:
            print(obj)
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            TileObject(pos, size, self.collision_sprite)

    def update_sprites(self):
        self.player.update(self.collision_sprite)

    def draw_sprites(self):
        self.field.draw(screen)
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
