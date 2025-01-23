from logic.menu import menu_scene
from logic.seting import *
# from logic.story_telling import show_story
from logic.game_scene import game_scene
from logic.support import load_image

current_scene = None

pygame.mixer.music.load('data/sounds/music_menu.mp3')
pygame.mixer.music.play()
is_music_play = True
pygame.mixer.music.set_volume(volume_sound_background)
pygame.display.set_icon(load_image('images\\icon_app.png'))

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
    # запуск текущей сцены
    current_scene(switch_scene)

pygame.quit()
