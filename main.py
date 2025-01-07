import pygame

from logic.field.field import Field, DrawField, tmx_map
from logic.Entity.players import Player
from logic.Entity.enemy import Enemy, EnemiesGroup
from logic.seting import HEIGHT, WIDTH, screen, FPS, load_image


class Game:
    def __init__(self):
        self.start_pos = (4000, 2600) # Начальное положение персонажа
        self.player_group = pygame.sprite.Group() # Группа персонажа
        self.field = Field(*self.start_pos) # Группа поля
        self.draw_obj = DrawField() # Группа объектов поля которые нужно отрисовывать на экране
        self.enemies = EnemiesGroup(self.draw_obj, tmx_map) # Группа врагов
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
        self.player_group.update(self.collision_sprite, self.field, self.enemies, self.draw_obj)
        self.enemies.update(self.player.hitbox.center, self.collision_sprite, self.player_group)

    def draw_sprites(self):
        """Отрисовка груп спрайтов"""
        self.player_group.draw(screen)
        self.draw_obj.draw()

    def center_camera(self):
        # Двигаем поле и игрока, что бы они всегда оставались на экране
        ofset = self.player.hitbox.centerx - screen.get_width() / 2, self.player.hitbox.centery - screen.get_height() / 2
        self.field.shift_sprites(*ofset)
        self.enemies.shift(*ofset)
        self.player.shift_player(ofset[0] * -1, ofset[1] * -1)
        self.player.create_player_rect()
        self.x_player, self.y_player = self.player.hitbox.center

    def main(self):
        running = True
        clock = pygame.time.Clock()
        self.center_camera()
        while running:
            screen.fill((99, 104, 10))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.WINDOWRESIZED:
                    # Окно не может быть меньше каках то размеров
                    if screen.get_width() < WIDTH:
                        pygame.display.set_mode((WIDTH, screen.get_height()), pygame.RESIZABLE)
                    if screen.get_height() < HEIGHT:
                        pygame.display.set_mode((screen.get_width(), HEIGHT), pygame.RESIZABLE)
                    self.center_camera()

            self.update_sprites()
            self.draw_sprites()

            # Отладочная информация
            # pygame.draw.line(screen, pygame.Color('black'), (0, screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))
            # pygame.draw.line(screen, pygame.Color('black'), (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()))
            # pygame.draw.rect(screen, pygame.Color('black'), self.player.rect_player, 1)
            # pygame.draw.rect(screen, pygame.Color('black'), self.player.hitbox, 1)
            # pygame.draw.rect(screen, pygame.Color('red'), self.player.hitbox, 1)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
