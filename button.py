import pygame.font


class Button:
	def __init__(self, screen, ai_settings, msg):
		self.screen = screen
		self.screen_rect = screen.get_rect()

		#устанавливаем размер и другие свойства кнопок
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		#построение прямоугольника кнопки
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		#сообщение кнопки
		self.prep_msg(msg)

	def prep_msg(self, msg):
		self.msg_image = self.font.render(msg, True, self.text_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		# Отображение пустой кнопки и вывод сообщения.
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)

