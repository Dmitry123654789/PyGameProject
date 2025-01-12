from logic.Entity.Enemy import Enemy
from logic.Entity.Players import Player
from logic.seting import *
from logic.Field.Tiles import *


class Field(pygame.sprite.Group):
    """Основной класс поля игры"""
    def __init__(self, now_x, now_y, tmx_map):
        super().__init__()
        self.tmx_map = tmx_map
        self.rect = pygame.rect.Rect(0, 0, self.tmx_map.width * CELL_SIZE, self.tmx_map.height * CELL_SIZE)
        self.now_coord = [now_x, now_y] # Фактические координаты игрока на поле

    def create_field(self, collision_group, draw_field):
        """Создание поля"""
        # Добавляем все видимые слои тайтлов
        for layer in ['Grass', 'Wall', 'Up_layer', 'Down_layer']:
            for x, y, surf in self.tmx_map.get_layer_by_name(layer).tiles():
                pos = (x * CELL_SIZE, y * CELL_SIZE)
                Tile(pos, pygame.transform.scale(surf, (CELL_SIZE, CELL_SIZE)), WORLD_LAYERS[layer], self, draw_field)

        # Добавляем слой теней
        for obj in self.tmx_map.get_layer_by_name('Shadow'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            img = pygame.transform.scale(obj.image, size).convert_alpha()
            img.set_alpha(150)
            Tile(pos, img, WORLD_LAYERS['Shadow'], self, draw_field)

        # Добавляем слои спрайтов
        for sprites in ['Up_sprites', 'Down_sprites', 'Sprites']:
            for obj in self.tmx_map.get_layer_by_name(sprites):
                pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
                size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
                Tile(pos, pygame.transform.scale(obj.image, size),  WORLD_LAYERS[sprites], self, draw_field)

        # Добавляем слой спрайтов содержащий порталы
        for obj in self.tmx_map.get_layer_by_name('Portal'):
            pos = obj.x / 16 * CELL_SIZE, obj.y / 16 * CELL_SIZE
            size = (CELL_SIZE / 100) * (obj.width / (16 / 100)), (CELL_SIZE / 100) * (obj.height / (16 / 100))
            Tile(pos, pygame.transform.scale(obj.image, size), WORLD_LAYERS['Down_layer'], self, draw_field)

        # Добавляем слой полигонов (хитбоксов)
        for obj in self.tmx_map.get_layer_by_name('Polygon'):
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
        if delta_x > 0 and self.now_coord[0] + (screen.get_width() - pos_player.x) >= self.rect.width or \
                delta_y > 0 and self.now_coord[1] + (screen.get_height() - pos_player.y) >= self.rect.height or \
                delta_x < 0 and self.now_coord[0] - pos_player.centerx <= 0 or \
                delta_y < 0 and self.now_coord[1] - pos_player.centery <= 0:
            return True
        return False


class DrawField(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        """Отрисовка"""
        # Сортируем по высоте
        bg_sprites = sorted([sprite for sprite in self if sprite.z < WORLD_LAYERS['Main']], key=lambda x: x.z)
        main_sprites = sorted([sprite for sprite in self if sprite.z == WORLD_LAYERS['Main']], key=lambda sprite: sprite.rect.centery)
        fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['Main']]
        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in layer:
                self.display_surface.blit(sprite.image, sprite.rect.topleft)
                # Если это враг или игрок рисуем полоску здоровья
                if isinstance(sprite, (Enemy, Player)) and sprite.hp > 0:
                    pygame.draw.rect(self.display_surface, (255, 0, 0), (sprite.rect.x + sprite.rect.width / 10, sprite.rect.y, sprite.rect.width * 0.8, 5))
                    pygame.draw.rect(self.display_surface, (50, 200, 50), (sprite.rect.x + sprite.rect.width / 10, sprite.rect.y, sprite.rect.width * 0.8 * ((sprite.hp / (sprite.max_hp / 100)) / 100) , 5))
                    # pygame.draw.rect(self.display_surface, (0, 255, 0), sprite.hitbox, 1)