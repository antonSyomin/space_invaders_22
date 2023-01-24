import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
	pygame.init()
	ai_settings = Settings()
	stats = GameStats(ai_settings)
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	gf.create_fleet(ai_settings, screen, ship, aliens)
	sb = Scoreboard(ai_settings, screen, stats)
	play_button = Button(screen, ai_settings, "PLay")

	#Запуск основного цикла игры
	while True:
		gf.check_events(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)
			#Отслеживание событий клавиатуры и мыши
			gf.check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)
		gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb)


run_game()

