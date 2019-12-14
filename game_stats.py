import pygame
class GameStats():
	"""Остслеживание статистики для игры Alien Invasion."""
	def __init__(self, ai_settings):
		"""Инициализирует статистику."""
		self.ai_settings = ai_settings
		self.reset_stats()
		# игра запускается в неактивном состоянии.
		self.game_active = False
		music_menu = pygame.mixer.music.load("music/Erotomania.OGG")
		music_menu = pygame.mixer.music.set_volume(0.4)
		pygame.mixer.music.play()
		# Рекорд не должен сбрасываться
		self.high_score = 0

	def reset_stats(self):
		"""Инициализирует статистику, изменяющуюся в ходе игры."""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0	
		self.level = 1