import pygame.event

from logic.seting import *

pygame.init()


class Point:
    pass


def world_map_scene(switch_scene):
    world_map = load_image('images/world_map.png')
    clock = pygame.time.Clock()
    running = True

    scroll_x = 0
    scroll_y = 0
    scroll_x_speed = 0
    scroll_y_speed = 0
    moving = False
    start_pos = (0, 0)
    zoom = 1
    while running:
        world_map_scaled = world_map.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                moving = True
                start_pos = pygame.mouse.get_pos()
                # обработка нажатия на локацию
            # перемещение карты мышью
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                moving = False
            # перемещение карты клавишами
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    switch_scene('menu_scene')
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    scroll_x_speed -= 10
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    scroll_x_speed += 10
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    scroll_y_speed -= 10
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    scroll_y_speed += 10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    scroll_x_speed += 10
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    scroll_x_speed -= 10
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    scroll_y_speed += 10
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    scroll_y_speed -= 10
            elif event.type == pygame.MOUSEWHEEL:
                print(event.y)

        scroll_x += scroll_x_speed * zoom
        scroll_y += scroll_y_speed * zoom

        if moving:  # если происходит перемещение при помощи мыши
            current_pos = pygame.mouse.get_pos()
            scroll_x += start_pos[0] - current_pos[0]
            scroll_y += start_pos[1] - current_pos[1]
            start_pos = current_pos

        # ограничение смещения
        max_scroll_x = (world_map.get_width() * zoom - virtual_surface.get_width()) // 2
        max_scroll_y = (world_map.get_height() * zoom - virtual_surface.get_height()) // 2

        scroll_x = max(-max_scroll_x, min(max_scroll_x, scroll_x))
        scroll_y = max(-max_scroll_y, min(max_scroll_y, scroll_y))

        # новый размер карты с учетом масштаба
        scaled_width = int(world_map.get_width() * zoom)
        scaled_height = int(world_map.get_height() * zoom)

        # подгоняем карту под нужный размер
        scaled_map = pygame.transform.scale(world_map_scaled, (scaled_width, scaled_height))

        virtual_surface.blit(scaled_map, (virtual_surface.get_width() // 2 - scaled_map.get_width() // 2 - scroll_x,
                                          virtual_surface.get_height() // 2 - scaled_map.get_height() // 2 - scroll_y))
        screen.blit(virtual_surface, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
