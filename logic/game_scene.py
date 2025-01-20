import pygame
from pytmx import load_pygame

from logic.Entity.Enemy import EnemiesGroup
from logic.Entity.Players import Player
from logic.field.Field import Field, DrawField
from logic.Things.Portal import Portal
from logic.Things.ThingGroup import Things
from logic.seting import HEIGHT, WIDTH, screen, FPS, CELL_SIZE
from logic.pause import Pause


class Game:
    """Класс для запуска игры"""

    def __init__(self, tmx_map, color):
        self.tmx_map = load_pygame(tmx_map)  # Загружаем основную карту мира
        self.start_pos = self.get_start_pos()  # Начальное положение персонажа
        self.color = color  # Цвет заднего фона
        self.player_group = pygame.sprite.Group()  # Группа персонажа
        self.field = Field(*self.start_pos, self.tmx_map)  # Группа поля
        self.draw_obj = DrawField()  # Группа объектов поля которые нужно отрисовывать на экране
        self.enemies = EnemiesGroup(self.draw_obj, self.tmx_map)  # Группа врагов
        self.collision_sprite = pygame.sprite.Group()  # Группа спрайтов с которыми взамидействует персонаж
        self.thihgs_group = Things(self.draw_obj, self.tmx_map)  # Группа различных объектов на поле
        self.x_player, self.y_player = self.start_pos  # Положение персонажа на карте до изменения размеров экрана
        self.add_group_sprite()

    def get_start_pos(self):
        """Узнает начальную позицию персонажа"""
        obj = self.tmx_map.get_layer_by_name('Point_player')[0]
        pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
        return pos

    def add_group_sprite(self):
        """Добаваляет объекты в группы"""
        self.player = Player(self.start_pos, self.player_group, self.draw_obj)
        self.field.create_field(self.collision_sprite, self.draw_obj)

    def update_sprites(self):
        """Обновление груп спрайтов"""
        self.field.update()
        self.player_group.update(self.collision_sprite, self.field, self.enemies, self.draw_obj, self.thihgs_group)
        self.enemies.update(self.player.hitbox.center, self.collision_sprite, self.player_group)
        self.thihgs_group.update(self.player_group, self.enemies)

    def draw_sprites(self):
        """Отрисовка груп спрайтов"""
        self.player_group.draw(screen)
        self.draw_obj.draw()

    def center_camera(self):
        """Двигаем поле и игрока, что бы они всегда оставались на экране"""
        ofset = self.player.hitbox.centerx - screen.get_width() / 2, self.player.hitbox.centery - screen.get_height() / 2
        self.field.shift_sprites(*ofset)
        self.enemies.shift(*ofset)
        self.thihgs_group.shift(*ofset)
        self.player.shift_player(ofset[0] * -1, ofset[1] * -1)
        self.player.create_player_rect()
        self.x_player, self.y_player = self.player.hitbox.center

    def end_game(self):
        """Проверка убиты ли все враги и ли пришел персонаж к порталу"""
        for sprite in self.thihgs_group:
            if isinstance(sprite, Portal) and len(self.enemies) == 0:
                if sprite.hitbox.colliderect(self.player.hitbox):
                    return True
        return False

    # def main(self):
    #     running = True
    #     clock = pygame.time.Clock()
    #     self.center_camera()
    #     while running:
    #         screen.fill(self.color)
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 # Если окно закрыто
    #                 running = False
    #             if event.type == pygame.WINDOWRESIZED:
    #                 # Окно не может быть меньше каках то размеров
    #                 if screen.get_width() < WIDTH:
    #                     pygame.display.set_mode((WIDTH, screen.get_height()), pygame.RESIZABLE)
    #                 if screen.get_height() < HEIGHT:
    #                     pygame.display.set_mode((screen.get_width(), HEIGHT), pygame.RESIZABLE)
    #                 self.center_camera()
    #
    #         self.update_sprites()
    #         self.draw_sprites()
    #         if self.end_game():
    #             ...  # Нужна обработка конца игры
    #
    #         # Отладочная информация
    #         # pygame.draw.line(screen, pygame.Color('black'), (0, screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))
    #         # pygame.draw.line(screen, pygame.Color('black'), (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()))
    #         # pygame.draw.rect(screen, pygame.Color('black'), self.player.rect_player, 1)
    #         # pygame.draw.rect(screen, pygame.Color('black'), self.player.hitbox, 1)
    #         # pygame.draw.rect(screen, pygame.Color('red'), self.player.hitbox, 1)
    #
    #         pygame.display.flip()
    #         clock.tick(FPS)
    #
    #     pygame.quit()


def game_scene(switch_scene):
    "(99, 104, 10), (244, 254, 250)"
    game = Game('data\\maps\\world_1.tmx', (244, 254, 250))
    running = True
    clock = pygame.time.Clock()
    another_scene = None
    game.center_camera()
    while running:
        screen.fill(game.color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Если окно закрыто
                running = False
                switch_scene(None)
            if event.type == pygame.WINDOWRESIZED:
                # Окно не может быть меньше каках то размеров
                if screen.get_width() < WIDTH:
                    pygame.display.set_mode((WIDTH, screen.get_height()), pygame.RESIZABLE)
                if screen.get_height() < HEIGHT:
                    pygame.display.set_mode((screen.get_width(), HEIGHT), pygame.RESIZABLE)
                game.center_camera()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                another_scene = Pause()

            # if another_scene is not None:
            #     if another_scene.handle_event(event) == 'Close':
            #         another_scene = None
        game.update_sprites()
        game.draw_sprites()
        if another_scene is not None:
            another_scene.draw(screen)
        if game.end_game():
            pass  # Нужна обработка конца игры

        # Отладочная информация
        # pygame.draw.line(screen, pygame.Color('black'), (0, screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))
        # pygame.draw.line(screen, pygame.Color('black'), (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()))
        # pygame.draw.rect(screen, pygame.Color('black'), self.player.rect_player, 1)
        # pygame.draw.rect(screen, pygame.Color('black'), self.player.hitbox, 1)
        # pygame.draw.rect(screen, pygame.Color('red'), self.player.hitbox, 1)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    # game.main()
