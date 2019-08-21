import sys
import pygame
from alien.bullet import Bullet
from alien.aliens import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ Реагирует на нажатие клавиш """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """ Регирует на отпускание клавиш """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """ Обрабатывает нажатия и события клавиш """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y =pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """ Запускает игру при нажатии Play """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        # Скрывает указатель мыши
        pygame.mouse.set_visible(False)
        # Сброс игровой статистики
        stats.reset_stats()
        stats.game_active = True
        # Сброс изображения счетов и уровней
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Очистка пришельцев и пуль
        aliens.empty()
        bullets.empty()
        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_setting, screen, stats, sb, ship, aliens, cloud, bullets, play_button):
    """ Обновляет изображение на экране и отображает новый экран """
    # при каждом проходе цикла прорисовывает новый экран
    screen.fill(ai_setting.bd_color)  # Прорисовывается цвет фона
    # Все пули выводяться позади изображения корабля и облака
    for bullet in bullets.sprites():
        bullet.draw_bulet()
    ship.blitme()
    aliens.draw(screen)
    cloud.blitme()
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # Отображение последнего прорисованного экрана
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Обновляет позции и уничтожает старые пули """
    bullets.update()
    # Удаление пуль вышедщих за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        check_bullet_aliens_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_aliens_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Обнаружение коллизий пуль с пришельцами """
    # При обноружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # Начисляет очки за сбитого пришельца
    if collisions:
        # Проходится по циклу, чтобы при одновременном попадании начислялось верное кол-во очков
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # Уничтожение сущ-щих пуль повышение скорости и создание нового флота
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullets(ai_settings, screen, ship, bullets):
    """ Выпускает пулю, если максимум ещё не достигнут """
    # Создание новой пули и включение ее в группу bullets.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """ Вычисляет кол-во пришельцев в ряду """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """ Определяет кол-во рядов, помещающихся на экране """
    available_space_y = (ai_settings.screen_height - alien_height - ship_height)
    number_rows = int(available_space_y/alien_height)
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Создает пришельца и размещает его в ряду """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """ Создает флот пришельцев """
    # Создание пришельца и вычисление кол-ва пришельцев в одном ряду
    # Интервал между соседними равен одной ширине пришельца
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Создание флота пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Создание пришельца и размещение его в ряду
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """ Реагирует на достижение пришельцем экрана """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ Опускает весь флот и меняет направление """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """ Обрабатывает столкновения корябля с пришельцами """
    if stats.ships_left > 0:
        # Уменьшение ships_left
        stats.ships_left -= 1
        # Обновление информации
        sb.prep_ships()

        # Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """ Проверяет добрались ли до конца экрана пришельцы """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит тоже что и при столкновении с кораблём
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """ Проверяет, достиг ли флот экрана, после чего
     обновляет позиции всех пришельцев """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка колизий "пришелец-корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_high_score(stats, sb):
    """ Проверяет, появился ли новый рекорд """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
