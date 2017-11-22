##
## alien_invasion.py
##

## Setting Window Position

# Available in Windows 8.1

window_pos_x = 100
window_pos_y = 50
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_pos_x, window_pos_y)

## Import(system)

import sys
import pygame
from pygame.sprite import Group

## Import(resources)

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


## Run Game Function

def run_game():
	
	# Initialize
	pygame.init()
	# Create Game Window
	pygame.display.set_caption("Alien Invasion")
	
	# Settings
	ai_settings = Settings()
	
	# Screen 
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height)
		)
	
	# Play Button
	play_button = Button(ai_settings, screen, "Play")
	
	# Statastics
	stats = GameStats(ai_settings)
	
	# Scoreboard
	sb = Scoreboard(ai_settings, screen, stats)
	
	# Ship
	ship = Ship(ai_settings, screen)
	
	# Bullets
	bullets = Group()
	
	# Aliens
	aliens = Group()	
	
	# Fleet Initialize
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# Main Loop
	while True:
		
		# Monitoring Keyboard and Mouse Events
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
		
		if stats.game_active:
						
			# Update Game Elements
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
		
		# Update Screen
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


## Run Game

run_game()
