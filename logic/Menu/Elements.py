import pygame

import data.globals
from logic.seting import screen
from logic.support import load_image


class MenuButton(pygame.sprite.Sprite):
    """Класс, создает кнопку для главного меню"""

    def __init__(self, pos, text, namb, *group):
        super().__init__(*group)
        self.namb = namb  # Порядковый номер кнопки
        self.text = text  # eng, rus
        self.lang = self.text[0]
        self.font = pygame.font.Font('data\\font.otf', screen.get_height() // 100 * 5)
        self.image = self.font.render(self.lang, True, '#FAFAFA')
        self.rect = self.image.get_rect(topleft=pos)

    def collision(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def update(self):
        self.font = pygame.font.Font('data\\font.otf', screen.get_height() // 100 * 5)
        self.image = self.font.render(self.lang, True, '#FAFAFA')
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() // 2 - self.rect.width // 2
        self.rect.y = screen.get_height() // 3.2 + 40 + (self.font.get_height() + 40) * self.namb

    def update_language(self, text):
        self.lang = self.text[text]


class Speaker(pygame.sprite.Sprite):
    """Класс, отслеживающий включение и выключение музыки"""
    speaker = pygame.transform.scale(load_image('images\\speaker.png'), (50, 50))
    mute_speaker = pygame.transform.scale(load_image('images\\mute_speaker.png'), (50, 50))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = self.speaker
        self.rect = self.image.get_rect()
        self.index = 0
        if not data.globals.is_music_play:
            self.update_value()

    def update(self):
        self.rect.center = screen.get_width() - 75, 75

    def update_value(self):
        self.index += 1
        self.index %= 2
        if self.index:
            self.image = self.mute_speaker
            return True
        self.image = self.speaker
        return False
