import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
	"""
	Корабль, которым управляет игрок
	"""

	def __init__(self, ai_settings, screen):
		super().__init__()
		self._screen = screen

		self._ai_settings = ai_settings
		self.image = pygame.image.load("images/ship.bmp")
		self.rect = self.image.get_rect()
		self._screen_rect = self._screen.get_rect()
		#каждый новый корабль появляется внизу экрана
		self.rect.centerx = self._screen_rect.centerx
		self.rect.bottom = self._screen_rect.bottom
		self._center_x = float(self.rect.centerx)
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self) -> None:
		"""
		Движение корабля влево и вправо.
		Чтобы корабль стоял на месте при одновременном нажатии ← и →,
		используется if, а не elif
		:return: None
		"""
		if self.moving_left and self.rect.left > self._screen_rect.left:
			self._center_x -= self._ai_settings.ship_speed_factor
		if self.moving_right and self.rect.right < self._screen_rect.right:
			self._center_x += self._ai_settings.ship_speed_factor
		if self.moving_up and self.rect.top > self._screen_rect.top:
			self.rect.bottom -= 1
		if self.moving_down and self.rect.bottom < self._screen_rect.bottom:
			self.rect.bottom += 1
		self.rect.centerx = self._center_x

	def get_rect(self):
		return self.rect

	def center_ship(self):
		"""Размещает корабль в центре нижней стороны."""
		self.rect.center = self._screen_rect.center
		self.rect.bottom = self._screen_rect.bottom

	def blit_me(self):
		"""Нарисовать корбаль в текущей позиции"""
		self._screen.blit(self.image, self.rect)


