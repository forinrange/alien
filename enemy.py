import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """Класс, представляющий противников пришельцев."""

    def __init__(self, ai_settings, screen):
        """Инициализурует пришельца и задает его начальную позицию."""
        super(Enemy, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения пришельца и назначение атрибута rect.
        self.image = pygame.image.load('images/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, 86))
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции пришельца.
        self.x = float(self.rect.x)

    def blitme(self):
        """Выводит пришельца в текушем положении."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Перемещает пришельцев влево и вправо."""
        self.x += (self.ai_settings.enemy_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
