import sys
import pygame

from alien.settings import Settings
from alien.ship import Ship
import alien.game_functions as gf
from alien.cloud import Cloud
from pygame.sprite import Group
from alien.scoreboard import Scoreboard
from alien.game_stats import GameStats
from alien.button import Button


def run_game():
    """ Инциализирует игру и создает объект экрана """
    pygame.init()
    ai_setting = Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_width))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_setting, screen, "Play")  # Создание экземпляра класса кнопки
    stats = GameStats(ai_setting)  # Создание экземпляра класса для хранения статистики
    sb = Scoreboard(ai_setting, screen, stats)  # Создание экземпляра класса для ведения статистики
    ship = Ship(ai_setting, screen)  # Создание корабля
    cloud = Cloud(screen)  # Создание облака
    bullets = Group()  # Созадание группы для хранения пуль
    aliens = Group()  # Создание группы пришельца
    # Создание флота пришельцев
    gf.create_fleet(ai_setting, screen, ship, aliens)
    # Запуск основного цикла игры
    while True:
        gf.check_events(ai_setting, screen, stats, sb, play_button, ship, aliens,
                        bullets)  # Ипортируем функции-игры, при каждом проходе цикла прорисовыввается экран
        gf.update_screen(ai_setting, screen, stats, sb, ship, aliens, cloud, bullets, play_button)
        if stats.game_active:
            ship.update()  # Движение корабля -> при нажатии и удерживание клавиши RIGHT
            gf.update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_setting, stats, sb, screen, ship, aliens, bullets)


run_game()
