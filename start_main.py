import pygame

from logic.game_scene import game_scene
from logic.menu import menu_scene
from logic.seting import volume_sound_background
from logic.world_map import world_map_scene
from logic.support import load_image

current_scene = None

pygame.mixer.music.load('data/sounds/music_menu.mp3')
pygame.mixer.music.play()
is_music_play = True
pygame.mixer.music.set_volume(volume_sound_background)
pygame.init()

pygame.display.set_icon(load_image('images\\icon_app.png').convert_alpha())

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
        # switch_scene(show_story)
    if current_scene == 'game_scene':
        pygame.mixer.music.stop()
        switch_scene(game_scene)
    if current_scene == 'world_map_scene':
        switch_scene(world_map_scene)
    # запуск текущей сцены
    current_scene(switch_scene)

pygame.quit()
