import pygame
from logic.seting import *
from logic.menu import menu_scene

current_scene = None

pygame.mixer.music.load('data/sounds/music_menu.mp3')
pygame.mixer.music.play()
is_music_play = True
pygame.mixer.music.set_volume(volume_sound_background)


def switch_scene(scene):
    global current_scene
    current_scene = scene


switch_scene(menu_scene)
while current_scene is not None:
    if current_scene == 'menu_scene':
        if is_music_play is False:
            is_music_play = True
            pygame.mixer.music.play()
        switch_scene(menu_scene)
    if current_scene == 'show_story':
        pygame.mixer.music.stop()
    # запуск текущей сцены
    current_scene(switch_scene)

pygame.quit()
