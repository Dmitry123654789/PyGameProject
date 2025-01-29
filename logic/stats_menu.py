import pygame
import sqlite3

from logic.seting import screen


class StatisticButton(pygame.sprite.Sprite):
    def __init__(self, pos, numb, *group):
        super().__init__(*group)
        self.pos = pos
        self.image = pygame.surface.Surface((90, 32))
        self.image.fill((163, 163, 163))
        self.numb = numb
        self.image.blit(pygame.font.Font('data/font.otf', 15).render(f'Уровен {self.numb + 1}',
                                                                     True, pygame.Color('black')), (10, 10))
        self.rect = self.image.get_rect(topleft=pos)
        self.select = False

    def collision(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def update(self, pos):
        if self.rect.collidepoint(pos):
            self.image.fill((100, 100, 100))
            self.select = True
        else:
            self.image.fill((163, 163, 163))
            self.select = False
        self.image.blit(pygame.font.Font('data/font.otf', 15).render(f'Уровень {self.numb + 1}',
                                                                     True, pygame.Color('black')), (10, 10))


class Statistics(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.add_button()
        self.con = sqlite3.connect('statictic.sqlite')

    def add_button(self):
        for i in range(4):
            if i == 0:
                but = StatisticButton((0, 0), i, self)
                but.select = True
                but.update((0, 0))
            else:
                StatisticButton((0, 0), i, self)

    def update(self, pos):
        collide = []
        for sprite in self.sprites():
            collide.append(sprite.collision(pos))
        if any(collide):
            for sprite in self.sprites():
                sprite.update(pos)

    def draw(self, surface):
        screen2 = pygame.surface.Surface((screen.get_width() // 2, screen.get_height() // 2))
        screen2.set_alpha(100)
        screen2.fill(pygame.color.Color('white'))
        screen2.blit(pygame.font.Font('data/font.otf', 25).render('Назад: Esc', True, pygame.Color('black')),
                     (10, 10))

        surface.blit(screen2, (screen.get_width() // 3 + 30, screen.get_height() // 3))
        for n, sprite in enumerate(self.sprites()):
            sprite.rect.x = screen.get_width() // 3 + 40 + n * sprite.rect.width + n * 2
            sprite.rect.y = screen.get_height() // 3 + 40
            surface.blit(sprite.image, sprite.rect)
            if sprite.select:
                cur = self.con.cursor()
                result = cur.execute("SELECT Time, Name FROM GameStat "
                                     "WHERE Level = ? "
                                     "ORDER BY Time", (sprite.numb + 1,)).fetchall()
                for i in range(10):
                    if i >= len(result):
                        text = f'{i + 1}. __.__.__'
                    else:
                        hours = result[i][0] // 60 // 60
                        miutes = result[i][0] // 60 % 60
                        text = f'{i + 1}. {str(hours).zfill(2)}.{str(miutes).zfill(2)}.{str(result[i][0] % 60).zfill(2)}'
                    surface.blit(pygame.font.Font('data/font.otf', 20).render(text, True, pygame.Color('black')),
                                 (screen.get_width() // 3 + 50, screen.get_height() // 3 + 90 + 20 * i))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'Close'
