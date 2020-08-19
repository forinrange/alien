


class Settings():
	"""Класс для хранения всех настроек игры Alien Invasion."""
	def __init__(self):
		"""Инициализирует статические  настройки игры."""
		# Параметры экрана
		self.screen_width = 1600
		self.screen_height = 1000
		self.bg_color = (230, 230, 230)
		
		self.ship_speed_factor = 2
		self.ship_limit = 3
		# Параметры пули
		self.bullet_speed_factor = 2
		# self.bullet_width = 5
		# self.bullet_height = 10
		#self.bullet_color = (255,69,0)
		self.bullets_allowed = 20
		# Настройка пришельцев
		self.enemy_speed_factor = 4
		self.fleet_drop_speed = 7
		# Темп ускорения игры.
		self.speedup_scale = 0.1
		# Темп роста стоимости пришельцев
		self.score_scale = 1.5
		self.initialize_dynamic_settings()
		
		# fleet_direction = 1 обозначает движение вправо; а - 1 - влево.
		self.fleet_direction = 1
		# Подсчет очков
		self.enemy_points = 50


	def initialize_dynamic_settings(self):
		"""Инициализирует настройки, изменяющиеся в ходе игры."""
		self.ship_speed_factor = 2
		self.bullet_speed_factor = 2
		self.enemy_speed_factor = 1
		# fleet_direction = 1 обозначает движение вправо; а - 1 - влево.
		self.fleet_direction = 1

	def increase_speed(self):
		"""Увеличивает настройки скорости и стоимости пришельцев."""
		self.ship_speed_factor += self.speedup_scale
		self.bullet_speed_factor += self.speedup_scale   
		self.enemy_speed_factor += self.speedup_scale
		self.enemy_points = int(self.enemy_points * self.score_scale) 
		#print(self.enemy_points)
	