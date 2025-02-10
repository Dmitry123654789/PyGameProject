import sqlite3

import pygame
from pytmx import load_pygame

import data.globals
import logic.seting as setting
from data.languages.language import game_elements
from logic.Game.Entity.Enemy import EnemiesGroup
from logic.Game.Entity.Players import Player
from logic.Game.Field.Field import Field, DrawField
from logic.Game.Things.Thing import Portal
from logic.Game.Things.ThingGroup import Things
from logic.Game.gamescene_menus import Pause, EndGame, DeadScene
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
        """Отрисовка поля"""
        self.player_group.draw(screen)
        self.draw_obj.draw()
        screen.blit(pygame.font.Font('data/font.otf', screen.get_width() // 35).render(
            f'{game_elements["enemy"][data.globals.LANGUAGE_INDEX]}: {len(self.enemies.sprites())}',
            True, 'black'), (0, 0))

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


def save_progress(timer, name):
    """Сохранение результата пройденнго уровня"""
    level = int(data.globals.current_level.split('_')[1])
    with open('data/saves/tag_coords/tag_coords.txt', 'r+') as file:
        data_file = file.readlines()
        for n, line in enumerate(data_file):
            split_line = line.split(';')
            if int(split_line[4]) - 1 > level:
                break
            if split_line[3] == 'False':
                split_line[3] = 'True'
                data_file[n] = ';'.join(split_line)
                break

    # Открываем файл в режиме записи, чтобы очистить его перед записью
    with open('data/saves/tag_coords/tag_coords.txt', 'w') as file:
        file.write(''.join(data_file))

    # Запись времени прохождения игры в БД
    con = sqlite3.connect('data\\statictic.sqlite')
    cur = con.cursor()
    cur.execute('INSERT INTO GameStat (Name, Time, Level) VALUES (?, ?, ?)',
                (name, timer // 1000, level))
    con.commit()
    con.close()

def draw_timer(timer):
    timer //= 1000
    hours = timer // 60 // 60
    minutes = timer // 60 % 60
    text = f'{game_elements["time"][data.globals.LANGUAGE_INDEX]}: {str(hours).zfill(2)}.{str(minutes).zfill(2)}.{str(timer % 60).zfill(2)}'
    render_text = pygame.font.Font('data/font.otf', screen.get_width() // 35).render(text, True, 'black')
    screen.blit(render_text, (screen.get_width() - render_text.get_width() - 10, 10))


def game_scene(switch_scene):
    game = Game(f'data\\maps\\{data.globals.current_level}.tmx')
    running, write = True, True
    dead_scene, pause_scene, end_game = None, None, None
    game.center_camera()
    game.update_sprites()
    fade_in(game.draw_sprites)
    clock = pygame.time.Clock()
    timer = pygame.time.get_ticks()  # Начало отсчета времени прохождения игроком карты
    pause_timer = 0
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and dead_scene is None and end_game is None:
                    pause_scene = Pause()
                    pause_timer = pygame.time.get_ticks()
                if not end_game is None:
                    end_game.tex_box.update_text(event)

            if event.type == pygame.MOUSEBUTTONUP:
                result = ('', None)
                for scene in [pause_scene, dead_scene, end_game]:
                    if scene is not None:
                        result = (scene.update(pygame.mouse.get_pos()), scene)
                        break
                if result[0] == 'continue':
                    pause_scene = None
                    timer += pygame.time.get_ticks() - pause_timer
                elif result[0] == 'reset':
                    running = False
                elif result[0] == 'map':
                    running = False
                    switch_scene('world_map_scene')
                    pygame.mixer.music.pause()
                elif result[0] == 'map_end' and end_game.tex_box.text != '':
                    save_progress(timer, end_game.tex_box.text)
                    running = False
                    switch_scene('world_map_scene')
                    pygame.mixer.music.pause()

                if isinstance(result[1], EndGame):
                    end_game.tex_box.update_select(event.pos)

        for scene in [pause_scene, dead_scene, end_game]:
            if scene is not None:
                game.draw_sprites()
                scene.draw(screen)
                break
        else:
            game.update_sprites()
            game.draw_sprites()

        if game.end_game():
            pygame.font.Font('data/font.otf', screen.get_width() // 35)
            if write:
                write = False
                end_game = EndGame()  # Вызов окна окончания игры
                timer = pygame.time.get_ticks() - timer
            draw_timer(timer)
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
