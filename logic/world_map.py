import pygame.event

from logic.seting import *

pygame.init()


class Point(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, level, status, *group):
        super().__init__(*group)
        self.images = [pygame.transform.scale(load_image('images/point_unlocked.png'), (75, 75)),
                       pygame.transform.scale(load_image('images/point_locked.png'), (75, 75))]
        self.image = self.images[0 if status else 1]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.is_collide = 0
        self.level = level
        self.unlock = status

    def draw(self, surface):
        surface.blit(self.image, self.rect.move(0, -self.is_collide))

    def update(self, mouse_pos, scroll_x, scroll_y):
        # rect_scaled = pygame.Rect(
        #     (self.rect.x - scroll_x - virtual_surface.get_width() // 12),
        #     (self.rect.y - scroll_y - virtual_surface.get_height() // 2.91),
        #     self.rect.w,
        #     self.rect.h)
        rect_scaled = pygame.Rect((self.rect.x - scroll_x) // 1.22,
                                  (self.rect.y - scroll_y) // 1.4, self.rect.w, self.rect.h)

        n = (int(mouse_pos[0] * (virtual_surface.get_width() / screen.get_width())),
             int(mouse_pos[1] * (virtual_surface.get_height() / screen.get_height())))
        if rect_scaled.collidepoint(n):
            self.is_collide = 20
        else:
            self.is_collide = 0

    def click(self):
        if self.is_collide != 0 and self.unlock:
            return True


def world_map_scene(switch_scene):
    world_map = load_image('images/world_map.png')
    clock = pygame.time.Clock()
    running = True

    all_sprite = pygame.sprite.Group()
    tag_group = pygame.sprite.Group()

    with open('data/saves/tag_coords/tag_coords.txt', 'r') as file:
        for coords in file.readline().split(','):
            coords = coords.replace('(', '').replace(')', '')
            coords = coords.split(';')
            Point(int(coords[0]), int(coords[1]), str(coords[2]), True if coords[3] == 'True' else False, all_sprite,
                  tag_group)
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
                for sprite in tag_group:
                    if sprite.click():
                        print(1)
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
        max_scroll_x = (world_map.get_width() * zoom - screen.get_width()) // 1.2
        max_scroll_y = (world_map.get_height() * zoom - screen.get_height()) // 1.2

        scroll_x = max(0, min(max_scroll_x, scroll_x))
        scroll_y = max(0, min(max_scroll_y, scroll_y))

        # новый размер карты с учетом масштаба
        scaled_width = int(world_map.get_width() * zoom)
        scaled_height = int(world_map.get_height() * zoom)

        tag_group.update(pygame.mouse.get_pos(), scroll_x, scroll_y)
        for sprite in tag_group:
            sprite.draw(world_map_scaled)

        # подгоняем карту под нужный размер
        scaled_map = pygame.transform.scale(world_map_scaled, (scaled_width, scaled_height))

        virtual_surface.blit(scaled_map,
                             (virtual_surface.get_width() // 2 - scaled_map.get_width() // 2 - scroll_x,
                              virtual_surface.get_height() // 2 - scaled_map.get_height() // 2 - scroll_y))
        screen.blit(virtual_surface, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
