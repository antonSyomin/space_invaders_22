class Settings:
	"""
	Класс для хранения настроек игры Alien Invasion.
	"""

	def __init__(self):
		#Параметры экрана
		self.screen_width = 1200
		self.screen_height = 800
		self._bg_color = (230, 230, 230)

		#настройки корабля
		self.ship_limit = 3

		#настройки пули
		self.bullet_width = 150
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 5

		#настройки пришельцев
		self.fleet_drop_speed = 10
		self.speedup_scale = 1.1
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.alien_speed_factor = 0.5
		self.ship_speed_factor = 1.2
		self.bullet_speed_factor = 5
		self.fleet_direction = 1
		self.alien_points = 50

	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)

	def get_bg_color(self) -> tuple[int, int, int]:
		return self._bg_color

