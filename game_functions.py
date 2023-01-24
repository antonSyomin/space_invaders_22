import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_key_down_events(event, ai_settings, screen, ship, bullets):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_RIGHT:
			ship.moving_right = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_LEFT:
			ship.moving_left = True
		elif event.key == pygame.K_UP:
			ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			ship.moving_down = True
		elif event.key == pygame.K_SPACE and len(bullets) < ai_settings.bullets_allowed:
			fire_bullets(ai_settings, screen, ship, bullets)


def check_key_up_events(event, ship):
	if event.type == pygame.KEYUP:
		if event.key == pygame.K_RIGHT:
			ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			ship.moving_left = False
		elif event.key == pygame.K_UP:
			ship.moving_up = False
		elif event.key == pygame.K_DOWN:
			ship.moving_down = False


def check_events(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, play_button, aliens, ship, bullets, mouse_x, mouse_y, sb)

		check_key_up_events(event, ship)
		check_key_down_events(event, ai_settings, screen, ship, bullets)


def check_play_button(ai_settings, screen, stats, play_button, aliens, ship, bullets, mouse_x, mouse_y, sb):
	if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
		stats.reset_stats()
		stats.game_active = True
		aliens.empty()
		bullets.empty()
		pygame.mouse.set_visible(False)
		sb.prep_score()
		sb.prep_level()
		sb.prep_high_score()
		sb.prep_ships()
		#создаем новый флот и возвращаем корабль в центр
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb):
	screen.fill(ai_settings.get_bg_color())
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blit_me()
	aliens.draw(screen)
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	pygame.display.flip()


def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
	available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows


def create_alien(ai_settings, screen, aliens, row_number, alien_number):
	alien = Alien(ai_settings, screen)
	alien.y = alien.rect.height + 2 * alien.rect.width * row_number
	alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.y
	aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
	"""Создает флот пришельцев"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, row_number, alien_number)


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_collisions(ai_settings, aliens, bullets, screen, ship, stats, sb)


def check_bullet_collisions(ai_settings, aliens, bullets, screen, ship, stats, sb):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
			check_high_score(stats, sb)

	if len(aliens) == 0:
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
	stats.ships_left -= 1
	if stats.ships_left > 0:
		#очищаем поле от пришельцев и пуль
		aliens.empty()
		bullets.empty()
		sb.prep_ships()
		#создаем флот заново и выравниваем корабль по центру
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		ai_settings.initialize_dynamic_settings()
	#пауза на подумать
	sleep(0.5)


def fire_bullets(ai_settings, screen, ship, bullets):
	new_bullet = Bullet(ai_settings, screen, ship)
	bullets.add(new_bullet)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)


def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break


def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1


def check_high_score(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

