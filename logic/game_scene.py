import pygame
import sqlite3
from pytmx import load_pygame
from win32trace import write

import data.globals
import logic.seting as setting
from logic.Entity.Enemy import EnemiesGroup
from logic.Entity.Players import Player
from logic.Field.Field import Field, DrawField
from logic.Things.Portal import Portal
from logic.Things.ThingGroup import Things
from logic.gamescene_menus import Pause, EndGame, DeadScene
from logic.seting import HEIGHT, WIDTH, screen, FPS, CELL_SIZE
from logic.support import fade_in


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


def save_progress():
    """Сохранение результата пройденнго уровня"""
    with open('data/saves/tag_coords/tag_coords.txt', 'r+') as file:
        data_file = file.readlines()
        for n, line in enumerate(data_file):
            split_line = line.split(';')
            if int(split_line[4]) - 1 > int(data.globals.current_level.split('_')[1]):
                break
            if split_line[3] == 'False':
                split_line[3] = 'True'
                data_file[n] = ';'.join(split_line)
                break

    # Открываем файл в режиме записи, чтобы очистить его перед записью
    with open('data/saves/tag_coords/tag_coords.txt', 'w') as file:
        file.write(''.join(data_file))



def game_scene(switch_scene):
    game = Game(f'data\\maps\\{data.globals.current_level}.tmx')
    running, write_bd = True, True
    dead_scene, pause_scene, end_game = None, None, None
    game.center_camera()
    game.update_sprites()
    fade_in(game.draw_sprites)
    clock = pygame.time.Clock()
    timer = pygame.time.get_ticks() # Начало отсчета времени прохождения игроком карты
    while running:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Если окно закрыто
                running = False
                switch_scene(None)
            if event.type == pygame.WINDOWRESIZED:
                # Окно не может быть меньше каких то размеров
                if screen.get_width() < setting.WIDTH:
                    pygame.display.set_mode((WIDTH, screen.get_height()), pygame.RESIZABLE)
                if screen.get_height() < setting.HEIGHT:
                    pygame.display.set_mode((screen.get_width(), HEIGHT), pygame.RESIZABLE)
                game.center_camera()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE \
                    and dead_scene is None and end_game is None:
                pause_scene = Pause()

            if event.type == pygame.MOUSEBUTTONUP:
                result = ('', None)
                for scene in [pause_scene, dead_scene, end_game]:
                    if scene is not None:
                        result = (scene.update(pygame.mouse.get_pos()), scene)
                        break
                if result[0] == 'continue':
                    pause_scene = None
                elif result[0] == 'reset':
                    running = False
                elif result[0] == 'map':
                    if isinstance(result[1], EndGame):
                        save_progress()
                    running = False
                    switch_scene('world_map_scene')

        for scene in [pause_scene, dead_scene, end_game]:
            if scene is not None:
                game.draw_sprites()
                scene.draw(screen)
                break
        else:
            game.update_sprites()
            game.draw_sprites()

        if game.end_game():
            if write_bd:
                # Запись времени прохождения игры в БД
                con = sqlite3.connect('statictic.sqlite')
                cur = con.cursor()
                cur.execute('INSERT INTO GameStat (Name, Time, Level) VALUES (?, ?, ?)',
                            ('None', (pygame.time.get_ticks() - timer) // 1000, int(game.tmx_map.filename.split('_')[-1].split('.')[0])))
                con.commit()
                con.close()
                write_bd = False
            end_game = EndGame() # Вызов окна окончания игры
        if game.player.hp <= 0:
            dead_scene = DeadScene()  # Вызов окна смерти игрока

        # Отладочная информация
        # pygame.draw.line(screen, pygame.Color('black'), (0, screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))
        # pygame.draw.line(screen, pygame.Color('black'), (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()))
        # pygame.draw.rect(screen, pygame.Color('black'), self.player.rect_player, 1)
        # pygame.draw.rect(screen, pygame.Color('black'), self.player.hitbox, 1)
        # pygame.draw.rect(screen, pygame.Color('red'), self.player.hitbox, 1)

        pygame.display.flip()
        clock.tick(FPS)
