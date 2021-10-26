class Settings():
    def __init__(self):
        self.FPS = 33.333333333
        # screen
        self.screen_width = 1280
        self.screen_height = 720
        self.caption = 'Alien'
        self.bg_color = (0, 0, 0)
        # ship
        self.ship_limit = 3

        # weapon
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (0, 175, 175)
        self.bullets_allowed = 3

        # fleet
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # dynamic settings
        self.speedup_scale = 1.15
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # speed and direction of all object in game
        self.ship_speed = 5
        self.bullet_speed = 7.75
        self.allien_speed = 1
        self.fleet_direction = 1
        self.allien_points = 50

    def increase_speed(self):
        # update speed and direction on scale value

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.allien_speed *= self.speedup_scale
        self.allien_points = int(self.allien_points * self.score_scale)
