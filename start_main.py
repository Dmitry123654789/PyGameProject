import pygame
from logic.seting import *
from logic.menu import menu_scene
current_scene = None


# Загрузка изображения иконки
def switch_scene(scene):
    global current_scene
    current_scene = scene




switch_scene(menu_scene)
while current_scene is not None:
    # цикл не удалять, нужен в дальнейшем
    current_scene(switch_scene)

pygame.quit()
