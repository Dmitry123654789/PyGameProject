import pygame

from logic.field.field import Field, DrawField
from logic.players import Player
from logic.seting import HEIGHT, WIDTH, screen, FPS


class Game:
    def __init__(self):
        self.start_pos = (WIDTH / 2 + 40, HEIGHT / 2) # Начальное положение персонажа
        self.player_group = pygame.sprite.Group() # Группа персонажа
        self.field = Field(*self.start_pos) # Группа поля
        self.draw_obj = DrawField() # Группа объектов поля которые нужно отрисовывать на экране
        self.collision_sprite = pygame.sprite.Group() # Группа спрайтов с которыми взамидействует персонаж
        self.x_player, self.y_player = self.start_pos # Положение персонажа на карте до изменения размеров экрана
        self.add_group_sprite()

    def add_group_sprite(self):
        """Добаваляет объект в группу"""
        self.player = Player(self.start_pos, self.player_group, self.draw_obj)
        self.field.create_field(self.collision_sprite, self.draw_obj)

    def update_sprites(self):
        """Обновление груп спрайтов"""
        self.field.update()
        self.player_group.update(self.collision_sprite, self.field)

    def draw_sprites(self):
        """Отрисовка груп спрайтов"""
        self.player_group.draw(screen)
        self.draw_obj.draw()

    def main(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill((75, 114, 110)) # Цвет моря
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.WINDOWRESIZED:
                    # Окно не может быть меньше каках то размеров
                    if screen.get_size()[0] < WIDTH:
                        pygame.display.set_mode((WIDTH, screen.get_size()[1]), pygame.RESIZABLE)
                    if screen.get_size()[1] < HEIGHT:
                        pygame.display.set_mode((screen.get_size()[0], HEIGHT), pygame.RESIZABLE)

                    # Двигаем поле и игрока, что бы они всегда оставались на экране
                    ofset = self.player.hitbox.centerx - screen.get_width() / 2, self.player.hitbox.centery - screen.get_height() / 2
                    self.field.shift_sprites(*ofset)
                    self.player.shift_player(ofset[0] * -1, ofset[1] * -1)
                    self.player.create_player_rect()
                    self.x_player, self.y_player = self.player.hitbox.center

            self.update_sprites()
            self.draw_sprites()

            # Отладочная информация
            pygame.draw.line(screen, pygame.Color('black'), (0, screen.get_size()[1] / 2), (screen.get_size()[0], screen.get_size()[1] / 2))
            pygame.draw.line(screen, pygame.Color('black'), (screen.get_size()[0] / 2, 0), (screen.get_size()[0] / 2, screen.get_size()[1]))
            pygame.draw.rect(screen, pygame.Color('black'), self.player.rect_player, 1)
            pygame.draw.rect(screen, pygame.Color('black'), self.player.hitbox, 1)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
