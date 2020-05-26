import pygame as pg
import pygame.freetype as ft
from .map import Map
from .player import Player
from .camera import Camera
from .background import StaticBackground, ParallaxBackground, ScrollingBackground


# Size tuples
WINDOW_SIZE = (800, 600)
SURFACE_SIZE = (400, 300)


# Freetype font
ft.init()
freetype = ft.Font("assets/fonts/pixChicago.ttf", 8)


# Colour tuples
BLACK = (20, 20, 20)
WHITE = (235, 235, 235)
LIGHT_MAGENTA = (158, 99, 95)


# Hills background filepaths
hills_layer_1 = "assets/textures/Hills Layer 01.png"
hills_layer_2 = "assets/textures/Hills Layer 02.png"
hills_layer_3 = "assets/textures/Hills Layer 03.png"
hills_layer_4 = "assets/textures/Hills Layer 04.png"


'''Scenes form the baseline of our game. Examples: Splash screen, game screen, pause screen, etc.
Every individual scene inherits from this class. The render and update function for each scene is
called repeatedly in the main game loop. All sprites within the scene must be blitted on the
game_display attribute, and the game_display must be blitted onto the window surface in each
call of the render function.'''


class Scene:
	"""Represents a scene in the program, which is analogous to the state of the game"""
	def __init__(self):
		self.manager = SceneManager(self)
		self.game_display = pg.Surface(SURFACE_SIZE)

	def handle_events(self, events: list):
		raise NotImplementedError

	def update(self):
		raise NotImplementedError

	def render(self, surface: pg.Surface):
		raise NotImplementedError


class SceneManager:
	"""Handles scene transitions from one scene to another"""
	def __init__(self, scene: Scene):
		self.scene = scene
		self.scene.manager = self

	def switch_to_scene(self, scene: Scene):
		self.scene = scene
		self.scene.manager = self


class TitleScene(Scene):
	"""Represents the title screen"""
	def __init__(self):
		super().__init__()

		# Backgrounds
		self.static_background = StaticBackground(hills_layer_1, self.game_display)
		self.scrolling_background_1 = ScrollingBackground(hills_layer_2, self.game_display)
		self.scrolling_background_2 = ScrollingBackground(hills_layer_3, self.game_display)
		self.scrolling_background_3 = ScrollingBackground(hills_layer_4, self.game_display)

		# Initialize title text
		self.title = freetype.render("THE TOWER", LIGHT_MAGENTA, None, 0, 0, 32)
		self.title_blit_position = (int((self.game_display.get_width() - self.title[0].get_width()) / 2), 100)

		# Initialize instruction text
		self.text = freetype.render("Press Space to Start", (255, 255, 255))
		self.text_blit_position = (int((self.game_display.get_width() - self.text[0].get_width()) / 2), 200)

	def handle_events(self, events: list = None):
		# If space is pressed switch to GameScene
		current_keys = pg.key.get_pressed()
		if current_keys[pg.K_SPACE]:
			self.manager.switch_to_scene(GameScene())

	def update(self):
		# Update positions of all scrolling backgrounds
		self.scrolling_background_1.update(0.2)
		self.scrolling_background_2.update(0.5)
		self.scrolling_background_3.update(0.8)

	def render(self, surface: pg.Surface):
		# Blit backgrounds on game_display
		self.static_background.draw()
		self.scrolling_background_1.draw()
		self.scrolling_background_2.draw()
		self.scrolling_background_3.draw()

		# Blit text on game_display
		self.game_display.blit(self.title[0], self.title_blit_position)
		self.game_display.blit(self.text[0], self.text_blit_position)

		# Blit game_display on window surface
		surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))


class GameScene(Scene):
	"""Represents the actual game screen"""
	def __init__(self):
		super().__init__()

		# Game Map (as 2D array)
		self.game_map = Map('assets/maps/map2.txt')

		# Initialize camera
		self.camera = Camera(SURFACE_SIZE, self.game_map)

		# Initialize player
		self.player = Player()
		self.player_sprite_group = pg.sprite.GroupSingle(self.player)

		# Initialize terrain sprite group
		self.terrain_group = self.game_map.terrain_group

		# Initialize all sprites group
		self.all_sprites_group = pg.sprite.Group()
		self.all_sprites_group.add(self.player)
		self.all_sprites_group.add(self.terrain_group.sprites())

		# Initialize backgrounds
		self.static_background = StaticBackground(hills_layer_1, self.game_display)
		self.parallax_background_1 = ParallaxBackground(hills_layer_2, self.game_display)
		self.parallax_background_2 = ParallaxBackground(hills_layer_3, self.game_display)
		self.parallax_background_3 = ParallaxBackground(hills_layer_4, self.game_display)

	def handle_events(self, events: list = None):
		# Move player along game_map if direction keys are pressed
		current_keys = pg.key.get_pressed()
		self.player.move(
			current_keys[pg.K_LEFT],
			current_keys[pg.K_RIGHT],
			current_keys[pg.K_SPACE],
			self.game_map)

	def update(self):
		# If player dies switch to GameOverScene
		if self.player.is_dead(self.game_map):
			self.manager.switch_to_scene(GameOverScene())

		# Move camera to player's position
		self.camera.follow_target(self.player)

		# Update parallax backgrounds wrt camera position
		self.parallax_background_1.update(self.camera, 0.2)
		self.parallax_background_2.update(self.camera, 0.5)
		self.parallax_background_3.update(self.camera, 0.8)

	def render(self, surface):
		# Blit backgrounds on game_display
		self.static_background.draw()
		self.parallax_background_1.draw()
		self.parallax_background_2.draw()
		self.parallax_background_3.draw()

		# Draw terrain on game_display wrt camera position
		self.camera.draw(self.game_display, self.terrain_group)

		# Draw player on game_display wrt camera position
		self.player.draw(self.game_display, self.camera)

		# Blit game_display on window surface
		surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))


class GameOverScene(Scene):
	"""Represents the "Game Over" screen"""
	def __init__(self):
		super().__init__()

		# Initialize title
		self.title = freetype.render("GAME OVER", WHITE, None, 0, 0, 32)
		self.title_blit_position = (int((self.game_display.get_width() - self.title[0].get_width()) / 2), 100)

		# Initialize subtitle
		self.subtitle = freetype.render("Press F to pay respects", WHITE)
		self.subtitle_blit_position = (int((self.game_display.get_width() - self.subtitle[0].get_width()) / 2), 200)

	def handle_events(self, events: list = None):
		# If f gets pressed switch to GameScene
		current_keys = pg.key.get_pressed()
		if current_keys[pg.K_f]:
			self.manager.switch_to_scene(GameScene())

	def update(self):
		pass

	def render(self, surface: pg.Surface):
		# Fill game_display with black
		self.game_display.fill(BLACK)

		# Blit title and subtitle on game_display
		self.game_display.blit(self.title[0], self.title_blit_position)
		self.game_display.blit(self.subtitle[0], self.subtitle_blit_position)

		# Blit game_display on window surface
		surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))








