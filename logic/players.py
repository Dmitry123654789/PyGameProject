from logic.seting import *
import pygame


class Player(pygame.sprite.Sprite):
    image = load_image("dog_sprites.png")
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.up_sprite = split_image_to_surfaces(self.image, 32, CELL_SIZE, 11, 3, 5)
        self.down_sprite = split_image_to_surfaces(self.image, 32, CELL_SIZE, 11, 0, 5)
        self.right_sprite = split_image_to_surfaces(self.image, 32, CELL_SIZE, 11, 2, 5)
        self.left_sprite = split_image_to_surfaces(self.image, 32, CELL_SIZE, 11, 1, 5)
        self.lst_start_img = [self.up_sprite[1], self.down_sprite[1], self.right_sprite[1], self.left_sprite[1]]
        self.ind_sprite = 0
        self.image = self.right_sprite[-1]
        self.animation_timer = 0
        self.animation_interval = 50
        self.step = 8
        self.direction = 0

    def input(self, events):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.image = self.up_sprite[self.ind_sprite]
            self.rect.y -= self.step
            self.direction = 0
        elif key[pygame.K_DOWN]:
            self.image = self.down_sprite[self.ind_sprite]
            self.rect.y += self.step
            self.direction = 1
        elif key[pygame.K_RIGHT]:
            self.image = self.right_sprite[self.ind_sprite]
            self.rect.x += self.step
            self.direction = 2
        elif key[pygame.K_LEFT]:
            self.image = self.left_sprite[self.ind_sprite]
            self.rect.x -= self.step
            self.direction = 3
        else:
            self.image = self.lst_start_img[self.direction]


        for event in events:
            if event.type == pygame.KEYUP:
                print('a')
                if event.key == pygame.K_UP:
                    self.image = self.up_sprite[1]
                elif event.key == pygame.K_DOWN:
                    self.image = self.down_sprite[1]
                elif event.key == pygame.K_RIGHT:
                    self.image = self.right_sprite[1]
                elif event.key == pygame.K_LEFT:
                    self.image = self.left_sprite[1]


    def update(self, tick, events):
        if tick - self.animation_timer >= self.animation_interval:
            self.ind_sprite += 1
            self.ind_sprite %= len(self.right_sprite)
            self.animation_timer = tick
            self.input(events)
