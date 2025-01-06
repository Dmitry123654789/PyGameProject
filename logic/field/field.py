from pytmx import load_pygame

from logic.Entity.enemy import Enemy
from logic.Entity.players import Player
from logic.seting import *
from logic.field.Tiles import *

tmx_map = load_pygame('data/world_2.tmx')


class Field(pygame.sprite.Group):
    """Основной класс поля игры"""
    def __init__(self, now_x, now_y):
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, tmx_map.width * CELL_SIZE, tmx_map.height * CELL_SIZE)
        self.now_coord = [now_x, now_y] # Фактические координаты игрока на поле

    def create_field(self, collision_group, draw_field):
        """Создание поля"""

        # Добавляем все видимые слои тайтлов
        for layer in ['Grass', 'Wall', 'Up_layer', 'Down_layer']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                pos = (x * CELL_SIZE, y * CELL_SIZE)
                Tile(pos, pygame.transform.scale(surf, (CELL_SIZE, CELL_SIZE)), WORLD_LAYERS[layer], self, draw_field)

        # Добавляем слой теней
        for obj in tmx_map.get_layer_by_name('Shadow'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            img = pygame.transform.scale(obj.image, size).convert_alpha()
            img.set_alpha(150)
            Tile(pos, img, WORLD_LAYERS['Shadow'], self, draw_field)

        # Добавляем слои спрайтов
        for sprites in ['Up_sprites', 'Down_sprites', 'Sprites']:
            for obj in tmx_map.get_layer_by_name(sprites):
                pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
                size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
                Tile(pos, pygame.transform.scale(obj.image, size),  WORLD_LAYERS[sprites], self, draw_field)

        # Добавляем слой полигонов (хитбоксов)
        for obj in tmx_map.get_layer_by_name('Polygon'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            TileObject(pos, size, self, collision_group)


    def shift_sprites(self, delta_x, delta_y):
        """Сдвиг всех спрайтов на определенную делльту"""
        for sprite in self.sprites():
            sprite.shift(delta_x, delta_y)

    def update_coord(self, pos_player, delta_x=0, delta_y=0):
        # Обновляем наши фактические координаты на поле
        self.now_coord[0] += delta_x
        self.now_coord[1] += delta_y
        # Подошел ли персонаж к концу карты
        if delta_x > 0 and self.now_coord[0] + (screen.get_size()[0] - pos_player.x) >= self.rect.width or \
                delta_y > 0 and self.now_coord[1] + (screen.get_size()[1] - pos_player.y) >= self.rect.height or \
                delta_x < 0 and self.now_coord[0] - pos_player.centerx <= 0 or \
                delta_y < 0 and self.now_coord[1] - pos_player.centery <= 0:
            return True
        return False


class DrawField(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        bg_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS['Main']]
        main_sprites = sorted([sprite for sprite in self if sprite.z == WORLD_LAYERS['Main']], key=lambda sprite: sprite.rect.centery)
        fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['Main']]
        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in layer:
                self.display_surface.blit(sprite.image, sprite.rect.topleft)
                if isinstance(sprite, (Enemy, Player)):
                    pygame.draw.rect(self.display_surface, (255, 0, 0), (sprite.rect.x + sprite.rect.width / 10, sprite.rect.y, sprite.rect.width * 0.8, 5))
                    pygame.draw.rect(self.display_surface, (69, 15, 8), (sprite.rect.x + sprite.rect.width / 10, sprite.rect.y, sprite.rect.width * 0.8 * ((sprite.hp / (sprite.max_hp / 100)) / 100) , 5))
                    pygame.draw.rect(self.display_surface, (0, 255, 0), sprite.hitbox, 1)