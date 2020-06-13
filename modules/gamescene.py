import pygame as pg
import pygame.freetype as ft
from .level import *
from .player import Player
from .camera import Camera
from .background import *
from .headsupdisplay import HeadsUpDisplay

# Size tuples
from .playerstate import GameEvent

WINDOW_SIZE = (800, 600)
SURFACE_SIZE = (400, 300)


# Freetype font
# Initialise the FreeType font system
ft.init()
freetype = ft.Font("assets/fonts/pixChicago.ttf", 8)


# Colour tuples
BLACK = (20, 20, 20)
WHITE = (235, 235, 235)
LIGHT_MAGENTA = (158, 99, 95)


# Hills background filepaths
hills_layer_1 = "assets/textures/Hills/Hills Layer 01.png"
hills_layer_2 = "assets/textures/Hills/Hills Layer 02.png"
hills_layer_3 = "assets/textures/Hills/Hills Layer 03.png"
hills_layer_4 = "assets/textures/Hills/Hills Layer 04.png"


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

	def handle_events(self):
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
		self.text = freetype.render("Press any key to begin", (255, 255, 255))
		self.text_blit_position = (int((self.game_display.get_width() - self.text[0].get_width()) / 2), 200)

		# Play BGM
		pg.mixer.music.load("assets/sound/music/Latin Industries.ogg")
		pg.mixer.music.set_volume(0.2)
		pg.mixer.music.play(-1)

	def handle_events(self):
		# Clears the event queue and processes the events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			elif event.type == pg.KEYDOWN:
				# On any keypress, start the game
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

		# Initialise the level
		# self.level = Level(Level1Template())

		# Initialise the level manager
		self.level_manager = LevelManager()

		# Initialize camera
		self.camera = Camera(SURFACE_SIZE, self.level_manager.level.map)

		# Initialize player
		self.player = Player()
		self.player_sprite_group = pg.sprite.GroupSingle(self.player)

		# Initialize GUI
		self.hud = HeadsUpDisplay()

		# TODO: Delegate background handling to Map, since Maps should know their background
		# Initialize backgrounds
		self.static_background = StaticBackground(hills_layer_1, self.game_display)
		self.parallax_background_1 = ParallaxBackground(hills_layer_2, self.game_display)
		self.parallax_background_2 = ParallaxBackground(hills_layer_3, self.game_display)
		self.parallax_background_3 = ParallaxBackground(hills_layer_4, self.game_display)

		# Play BGM
		pg.mixer.music.load("assets/sound/music/Pixel Peeker Polka - faster.ogg")
		pg.mixer.music.set_volume(0.5)
		pg.mixer.music.play(-1)

	def handle_events(self):
		# Clears the event queue and processes the events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			elif event.type == GameEvent.SWITCH_LEVEL.value:
				self.level_manager.load_next_level(self.player, self.camera)
			elif event.type == GameEvent.GAME_OVER.value:
				self.manager.switch_to_scene(GameOverScene())

		# Processes the input for the player
		self.player.handle_input()

	def update(self):
		self.player.update(self.level_manager.level.map)
		self.level_manager.level.update(self.player)
		self.hud.update(self.player)

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

		# Draw player on game_display wrt camera position
		self.player.render(self.camera, self.game_display)

		# Draws the map and enemies
		self.level_manager.level.render(self.camera, self.game_display)

		# Draw GUI
		self.hud.render(self.game_display)

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

	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
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


# Unused, to be worked in
class LoadingScene(Scene):
	def __init__(self):
		super().__init__()
		# takes in arguments and passes it along to the next GameScene

	def update(self, *args):
		pass

	def render(self, surface: pg.Surface):
		self.game_display.fill(BLACK)
		surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))