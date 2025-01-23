import pygame
from pytmx import load_pygame

from logic.Entity.Enemy import EnemiesGroup
from logic.Entity.Players import Player
from logic.Field.Field import Field, DrawField
from logic.Things.Portal import Portal
from logic.Things.ThingGroup import Things
from logic.seting import HEIGHT, WIDTH, screen, FPS, CELL_SIZE
from logic.pause import Pause
from logic.support import fade_in, fade_out

class Game:
    """Класс для запуска игры"""

    def __init__(self, tmx_map):
        self.tmx_map = load_pygame(tmx_map)  # Загружаем основную карту мира
        self.start_pos = self.get_start_pos()  # Начальное положение персонажа
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
        ofset = (int(self.player.hitbox.centerx - screen.get_width() / 2),
                 int(self.player.hitbox.centery - screen.get_height() / 2))
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



def game_scene(switch_scene):
    game = Game('data\\maps\\world_3.tmx')
    running = True
    clock = pygame.time.Clock()
    another_scene = None
    game.center_camera()
    game.update_sprites()
    fade_in(game.draw_sprites)
    while running:
        screen.fill('black')
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
        if game.player.hp <= 0:
            pass # Нужна обработка смерти игрока

        # Отладочная информация
        # pygame.draw.line(screen, pygame.Color('black'), (0, screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))
        # pygame.draw.line(screen, pygame.Color('black'), (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()))
        # pygame.draw.rect(screen, pygame.Color('black'), self.player.rect_player, 1)
        # pygame.draw.rect(screen, pygame.Color('black'), self.player.hitbox, 1)
        # pygame.draw.rect(screen, pygame.Color('red'), self.player.hitbox, 1)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
