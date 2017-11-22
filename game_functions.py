##
## game_functions.py
##

## Import(system)

import sys
from time import sleep
import pygame

## Import(resources)

from ship import Ship
from bullet import Bullet
from alien import Alien

## Check Events Functions

## check events
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			#QUIT
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:
			#KEYDOWN
			check_keydown_events(
				event, ai_settings, screen, ship, bullets,
				)
				
		elif event.type == pygame.KEYUP:
			#KEYUP
			check_keyup_events(event, ship)
			
		elif event.type == pygame.MOUSEBUTTONUP:
			#MOUSEBUTTONUP
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button,
				ship, aliens, bullets, mouse_x, mouse_y)

# check keyup events				
def check_keyup_events(event, ship):
	
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
		
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		
	elif event.key == pygame.K_UP:	
		ship.moving_up = False
		
	elif event.key == pygame.K_DOWN:	
		ship.moving_down = False	

#check keydown events		
def check_keydown_events(event, ai_settings, screen, ship, bullets):
	
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
		
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
		
	elif event.key == pygame.K_UP:	
		ship.moving_up = True
		
	elif event.key == pygame.K_DOWN:	
		ship.moving_down = True
		
	elif event.key == pygame.K_SPACE:
		#fire bullets
		fire_bullet(ai_settings, screen, ship, bullets)
		
	elif event.key == pygame.K_q:
		#press Q to quit
		sys.exit()
		
## Update Functions

# update screen
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
		play_button):
	
	# fill background
	screen.fill(ai_settings.bg_color)
	
	# show bullets
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	
	# show ship
	ship.blitme()
	
	# show aliens
	aliens.draw(screen)
	
	if not stats.game_active:
		
		# show play button
		play_button.draw_button()
	
	# show scoreboard
	sb.show_scoreboard()
	
	# refresh all changes on screen 
	# THIS FUNCTION IS NECESSARY
	pygame.display.flip()

# update bullets
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	
	bullets.update()
	
	for bullet in bullets.copy():
		#using copy()
		
		if bullet.rect.bottom <= 0:
			# bullet reach screen top
			bullets.remove(bullet)
	
	# check bullet(sprites) and alien(sprites) collide		
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

# update aliens	
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	
	# check fleet reach edges
	check_fleet_edges(ai_settings, aliens)
	
	aliens.update()
	
	# check aliens(sprites) and ship(non-sprite item) collide 
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
	
	# check fleet reach bottom	
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
		
def	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):

	collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)	
	# High Energy Bullets: False True 
	# Medium Energy Bullets: True True
	# Low Energy Bullets: True False
	# Irrelevant Bullets: False False
	
	if collisions:
		for aliens in collisions.values():
			# bullets are in collisions.keys()
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
		
	if len(aliens) == 0:
		# all aliens are hit
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()
		# create a new fleet
		create_fleet(ai_settings, screen, ship, aliens)
						
def fire_bullet(ai_settings, screen, ship, bullets):
	
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		
def get_number_aliens_x(ai_settings, alien_width):	
	
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))	
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	
	available_space_y = (ai_settings.screen_height -
							(3 * alien_height) -ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows	
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
		
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien_height = alien.rect.height
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.y = alien.rect.height + 2 * alien_height * row_number
	alien.rect.y = alien.y
	aliens.add(alien)
	
def create_fleet(ai_settings, screen, ship, aliens):
	
	alien = Alien(ai_settings, screen)	
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
									alien.rect.height)
	
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, 
							row_number)	

def check_fleet_edges(ai_settings, aliens):
	
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	
	if stats.ships_left > 0:
		stats.ships_left -= 1
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		sleep(0.6)
	
	else:
		stats.game_active = False 
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break
	


def check_play_button(ai_settings, screen, stats, sb, play_button,
		ship, aliens, bullets, mouse_x, mouse_y):
	
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
	
		aliens.empty()
		bullets.empty()
		
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		sb.prep_score()
		sb.prep_level()
		sb.show_scoreboard()

def check_high_score(stats, sb):
	
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
