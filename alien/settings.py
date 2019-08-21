class Settings:
    """ Класс для хранения всех настроек игры """

    def __init__(self):
        """ Инициализирует статические настройки игры """
        # Параметры экрана
        self.screen_width = 600
        self.screen_height = 150
        self.bd_color = (127, 199, 255)

        # Настройки корабля
        self.ship_limit = 2

        # Настройки пули
        self.bullet_width = 1
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4  # Ограничение кол-ва пуль 5-ю

        # Настройка пришельца
        self.fleet_drop_speed = 10  # Величина снижения флота

        # Темп ускорения игры
        self.speedup_scale = 1.3
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Настройки изменяющиеся в ходе игры """
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1.3
        self.alien_speed_factor = 0.5

        # fleet_direction = 1 -> движение вправо,-1 влево
        self.fleet_direction = 1

        # Очки за убийство пришельца
        self.alien_points = 50

    def increase_speed(self):
        """ Уведичивает настройки игры и стоимость пришельцев """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
