import pygame


class Cloud:
    def __init__(self, screen):
        self.screen = screen
        # Загрузка изображения облака и размещение
        self.image = pygame.image.load('images/cloud.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Каждое облако появляется вверху экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.right = self.screen_rect.right

    def blitme(self):
        """ Рисуем облако на его позиции """
        self.screen.blit(self.image, self.rect)
