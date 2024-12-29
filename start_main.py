import pygame
from logic.seting import *
from logic.menu import menu_scene

current_scene = None



def switch_scene(scene):
    global current_scene
    current_scene = scene


switch_scene(menu_scene)
while current_scene is not None:
    if current_scene == 'menu_scene':
        switch_scene(menu_scene)

    # запуск текущей сцены
    current_scene(switch_scene)

pygame.quit()
