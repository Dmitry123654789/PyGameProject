import pygame

import data.globals
from logic.Game.game_scene import game_scene
from logic.Menu.menu import main_menu_scene
from logic.seting import volume_sound_background
from logic.support import load_image
from logic.world_map import world_map_scene

current_scene = None
pygame.mixer.music.load('data/sounds/music_menu.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume_sound_background)

pygame.display.set_icon(load_image('images\\icon_app.png').convert_alpha())


def switch_scene(scene):
    global current_scene
    current_scene = scene


switch_scene(main_menu_scene)
while current_scene is not None:
    if current_scene == 'menu_scene':
        switch_scene(main_menu_scene)
    # if current_scene == 'show_story':
    # pygame.mixer.music.stop()
    # switch_scene(show_story)
    if current_scene == 'game_scene':
        if data.globals.is_music_play:
            pygame.mixer.music.load('data/sounds/music_batle.mp3')
            pygame.mixer.music.play(-1)
        switch_scene(game_scene)
    if current_scene == 'world_map_scene':
        switch_scene(world_map_scene)
        if not pygame.mixer.music.get_busy() and data.globals.is_music_play:
            pygame.mixer.music.load('data/sounds/music_menu.mp3')
            pygame.mixer.music.play(-1)
    # запуск текущей сцены
    current_scene(switch_scene)

pygame.quit()
