import pygame

from logic.field.field import Field
from logic.players import Player
from logic.seting import HEIGHT, WIDTH, screen, FPS


class Game:
    def __init__(self):
        self.start_pos = (WIDTH / 2, HEIGHT / 2)
        self.player_group = pygame.sprite.Group()
        self.field = Field(*self.start_pos)
        self.draw_field = pygame.sprite.Group()
        self.collision_sprite = pygame.sprite.Group()
        self.add_group_sprite()
        self.x_player, self.y_player = self.start_pos

    def add_group_sprite(self):
        self.player = Player(self.start_pos, self.player_group)
        self.field.create_field(self.collision_sprite, self.draw_field)

    def update_sprites(self):
        self.field.update()
        self.player_group.update(self.collision_sprite, self.field)

    def draw_sprites(self):
        self.draw_field.draw(screen)
        self.player_group.draw(screen)

    def main(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill((75, 114, 110))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.WINDOWRESIZED:
                    if screen.get_size()[0] < WIDTH:
                        pygame.display.set_mode((WIDTH, screen.get_size()[1]), pygame.RESIZABLE)
                    if screen.get_size()[1] < HEIGHT:
                        pygame.display.set_mode((screen.get_size()[0], HEIGHT), pygame.RESIZABLE)

                    ofset = self.player.hitbox.centerx - self.x_player, self.player.hitbox.centery - self.y_player
                    self.field.shift_sprites(*ofset)
                    self.player.shift_player(ofset[0] * -1, ofset[1] * -1)
                    self.player.create_player_rect()
                    self.x_player, self.y_player = self.player.hitbox.center

            pygame.draw.rect(screen, pygame.Color('black'), self.player.rect_player)
            self.update_sprites()
            self.draw_sprites()
            # Отладочная информация
            pygame.draw.line(screen, pygame.Color('black'), (0, screen.get_size()[1] / 2), (screen.get_size()[0], screen.get_size()[1] / 2))
            pygame.draw.line(screen, pygame.Color('black'), (screen.get_size()[0] / 2, 0), (screen.get_size()[0] / 2, screen.get_size()[1]))
            pygame.draw.rect(screen, pygame.Color('black'), self.player.rect_player, 1)
            pygame.draw.rect(screen, pygame.Color('black'), self.player.hitbox, 1)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
