##
## settings.py
##

##

class Settings():
	
	def __init__(self):
		
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (225,225,225)
		
		self.ship_limit = 2
		
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3
		
		self.fleet_drop_speed = 9
		
		self.speedup_scale = 1.1
		self.scoreup_scale = 1.5
				
		# dynamic settings:
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		
		self.ship_speed_factor = 1
		self.bullet_speed_factor = 1.5
		self.alien_speed_factor = 1
		
		# -1: Move Left 1: Move Right
		self.fleet_direction = 1
		
		self.alien_points = 5
	
	def increase_speed(self):
		
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.scoreup_scale * self.alien_points)

		
