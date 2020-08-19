import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


# from detonation import Detonation
# from animatesprite import AnimateSprite


def run_game():
    # нициализирует pygame, settings и объект экрана.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    background_image = pygame.image.load("background.jpg").convert()
    background_image = pygame.transform.scale(background_image, (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    clock = pygame.time.Clock()
    fps = 90

    # Создание кнопки Play.
    play_button = Button(ai_settings, screen, "Play")

    # Создание корабля, группы пуль и группы пришельцев.
    ship = Ship(ai_settings, screen)

    bullets = Group()
    enemys = Group()

    # Создание экземпляров GameStats и Scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, enemys)

    def load_image(name):
        fullname = 'images' + '/' + name
        try:
            if name[-2:] == 'jpg' or name[-2:] == 'png':
                image = pygame.image.load(fullname).convert()
            else:
                image = pygame.image.load(fullname).convert_alpha()
        except:
            print('Cannot load image:', name)
            raise SystemExit()
        return image

    class AnimateSprite(pygame.sprite.Sprite):
        def __init__(self, image, columns, rows, x, y):
            super().__init__()
            self.frames = []
            self.cut_image(image, columns, rows)
            self.frame_number = 0
            self.image = self.frames[self.frame_number]
            self.rect = self.rect.move(x, y)
            self.add(all_sprites)

        def cut_image(self, image, columns, rows):
            """Разрезает картинку спрайта на равные части"""
            self.rect = pygame.Rect(0, 0, image.get_width() // columns, image.get_height() // rows)

            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(image.subsurface(pygame.Rect(frame_location, self.rect.size)))

        def update(self):
            self.frame_number = (self.frame_number + 1) % len(self.frames)
            self.image = self.frames[self.frame_number]

    all_sprites = pygame.sprite.Group()
    deton = AnimateSprite(load_image("deton.png"), 8, 6, 400, 700)

    # Запуск основного цикла игры.
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, enemys, bullets)
        screen.blit(background_image, [0, 0])
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(fps)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, enemys, bullets)
            gf.update_enemys(ai_settings, screen, stats, sb, ship, enemys, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, play_button, ship, enemys, bullets)

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()


run_game()
