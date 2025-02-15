import pygame

SIZE = WIDTH, HEIGHT = 800, 600
FPS = 240
CELL_SIZE = 30
WORLD_LAYERS = {
    'Grass': 0,
    'Shadow': 6,
    'Wall': 2,
    'Down_layer': 3,
    'Down_sprites': 4,
    'Main': 5,
    'Sprites': 5,
    'Up_sprites': 6,
    'Up_layer': 7
}

# Враги
ENEMY = {
    # Цвет: шаг, здоровье, урон, шанс
    'orange': (4, 100, 10, 50),
    'brown': (6, 150, 15, 30),
    'dark': (8, 200, 25, 10)
}

volume_sound_background = 0.1

pygame.init()
virtual_surface = pygame.Surface(
    (2560, 1440), pygame.SRCALPHA)  # поверхность, на которой отрисовывается все изначально
pygame.display.set_caption('Bark and Battle')
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
screen.fill(pygame.Color('black'))
