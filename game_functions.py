import sys
import pygame

from bullet import Bullet
from enemy import Enemy
from time import sleep


def get_namber_rows(ai_settings, ship_height, enemy_height):
    """Определяет количество рядов, помещающихся на экран."""
    available_space_y = (ai_settings.screen_height - (3 * enemy_height) - ship_height)
    namber_rows = int(available_space_y / (2 * enemy_height))
    return namber_rows


def get_namber_enemys_x(ai_settings, enemy_width):
    """Вычесляет количество пришельцеы в ряду."""
    available_space_x = ai_settings.screen_width - 2 * enemy_width
    namber_enemys_x = int(available_space_x / (2 * enemy_width))
    return namber_enemys_x


def create_enemy(ai_settings, screen, enemys, enemy_namber, row_namber):
    """Создает пришельца и размещает его в ряду."""
    enemy = Enemy(ai_settings, screen)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + 2 * enemy_width * enemy_namber
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_namber
    enemys.add(enemy)


def create_fleet(ai_settings, screen, ship, enemys):
    """Создает флот пришельцев."""
    # Создание пришельца и вычесление количества пришельцев в ряду.
    enemy = Enemy(ai_settings, screen)
    namber_enemys_x = get_namber_enemys_x(ai_settings, enemy.rect.width)
    namber_rows = get_namber_rows(ai_settings, ship.rect.height, enemy.rect.height)
    # Создание первого ряда пришельцев.
    for row_namber in range(namber_rows):
        for enemy_namber in range(namber_enemys_x):
            # Создание пришельца и размещение его в ряду.
            create_enemy(ai_settings, screen, enemys, enemy_namber, row_namber)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Создание новой пули и включение ее в группу bullets.
        if len(bullets) < ai_settings.bullets_allowed:
            lazer = pygame.mixer.music.load('music/laser_gun.mp3')
            pygame.mixer.music.play()
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, enemys, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек.
        ai_settings.initialize_dynamic_settings()
        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)
        # Сброс игровой статистики.
        stats.reset_stats()
        stats.game_active = True
        # Сброс изображений счетов и уровня.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Очистка списков пришельцев и пуль.
        enemys.empty()
        bullets.empty()
        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, enemys)
        ship.center_ship()


def check_events(ai_settings, screen, stats, sb, play_button, ship, enemys, bullets):
    """Обрабатывает нажатие клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, enemys, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, stats, sb, play_button, ship, enemys, bullets):
    """Обновляет изображения на экране и отображает новый экран."""
    # screen.fill(ai_settings.bg_color)
    ship.blitme()
    enemys.draw(screen)
    sb.show_score()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Кнопка Play отображается в том случае, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, enemys, bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиции пуль
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        check_bullet_enemy_collisions(ai_settings, screen, stats, sb, ship, enemys, bullets)


def check_bullet_enemy_collisions(ai_settings, screen, stats, sb, ship, enemys, bullets):
    """Обработка коллизий пуль с пришельцами."""

    # Удаление пуль и пришельцев, участвующих в колизиях.
    collisions = pygame.sprite.groupcollide(bullets, enemys, True, True)

    if collisions:

        for enemys in collisions.values():
            stats.score += ai_settings.enemy_points * len(enemys)
            sb.prep_score()
            check_high_score(stats, sb)

    if len(enemys) == 0:
        # Если весь флот уничтожен, начинается следующий уровень.
        create_fleet(ai_settings, screen, ship, enemys)
        bullets.empty()
        ai_settings.increase_speed()
        # Увеличение уровня.
        stats.level += 1
        sb.prep_level()


def check_fleet_adges(ai_settings, enemys):
    """Реагирует на достижение пришельцем края экрана."""
    for enemy in enemys.sprites():
        if enemy.check_edges():
            change_fleet_direction(ai_settings, enemys)
            break;


def change_fleet_direction(ai_settings, enemys):
    """Опускает весь флот и меняет направление флота."""
    for enemy in enemys.sprites():
        enemy.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_enemys(ai_settings, screen, stats, sb, ship, enemys, bullets):
    """Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте."""
    check_fleet_adges(ai_settings, enemys)
    enemys.update()
    # Проверка коллизий "пришелец-корабль".
    if pygame.sprite.spritecollideany(ship, enemys):
        ship_hit(ai_settings, screen, stats, sb, ship, enemys, bullets)
        ship_hit(ai_settings, screen, stats, sb, ship, enemys, bullets)
    # Проверка пришельцев, добравшихся до нижнего края экрана.
    check_enemys_bottom(ai_settings, screen, stats, sb, ship, enemys, bullets)


def ship_hit(ai_settings, screen, stats, sb, ship, enemys, bullets):
    """Обрабатывает столкновение корабля с пришельцами."""
    if stats.ships_left > 0:
        # Уменьшает количество жизней.
        stats.ships_left -= 1
        # Обновление игровой информации. 
        sb.prep_ships()

        # Очистка списков пришельцев и пуль.
        enemys.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, enemys)
        ship.center_ship()

        # Пауза.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_enemys_bottom(ai_settings, screen, stats, sb, ship, enemys, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for enemy in enemys.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем.
            ship_hit(ai_settings, screen, stats, sb, ship, enemys, bullets)
            break;


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
