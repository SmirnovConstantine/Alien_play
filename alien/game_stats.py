class GameStats():
    """ Отслеживание статистики в игре """

    def __init__(self, ai_settings):
        """ Инициализирует стистику в игре """
        self.ai_settings = ai_settings
        self.reset_stats()
        # Игра запускается в неактивном состоянии
        self.game_active = False
        # Рекорд игры не должен сбрасываться
        self.high_score = 0

    def reset_stats(self):
        """ Инициализирует статистику измен-ся в ходе игры """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
