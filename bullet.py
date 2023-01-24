import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
	"""
	Класс для управления пулями корабля
	"""
	def __init__(self, ai_settings, screen, ship):
		super(Bullet, self).__init__()
		self.screen = screen

		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.get_rect().top
		self.y = float(self.rect.y)
		self.color = 60, 60, 60
		self.speed_factor = ai_settings.bullet_speed_factor

	def update(self):
		"""Перемещает пулю вверх по экрану"""
		self.y -= self.speed_factor
		self.rect.y = self.y

	def draw_bullet(self):
		"""Вывод пули"""
		pygame.draw.rect(self.screen, self.color, self.rect)
