class GameStats():
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_mode = False
        self.game_level = 1
        self.high_score = self._enter_save()


    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0


    def _save_game(self):
        with open('record.txt', 'w') as record:
            record.write(str(self.high_score))

    def _enter_save(self):
        with open('record.txt', 'r') as record:
            info = int(record.readline().rstrip())
            return info
