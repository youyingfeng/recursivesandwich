import pygame as pg
import pygame.freetype as freetype

from .player import Player
from .camera import Camera
from .map import Map
from .animations import StaticBackground, ParallaxBackground, ScrollingBackground

from .scenemanager import Scene, SceneManager

# Globals
WINDOW_SIZE = (800, 600)
SURFACE_SIZE = (400, 300)


class TitleScene(Scene):
    def __init__(self):
        self.manager = SceneManager(self)

        self.game_display = pg.Surface(SURFACE_SIZE)  # Initialize surface for drawing

        self.static_background = StaticBackground("assets/textures/Hills Layer 01.png", self.game_display)
        self.scrolling_background_1 = ScrollingBackground("assets/textures/Hills Layer 02.png", self.game_display)
        self.scrolling_background_2 = ScrollingBackground("assets/textures/Hills Layer 03.png", self.game_display)
        self.scrolling_background_3 = ScrollingBackground("assets/textures/Hills Layer 04.png", self.game_display)

        freetype.init()
        self.font = freetype.Font("assets/fonts/pixChicago.ttf", 8)

        self.title = self.font.render("THE TOWER", (158, 99, 95), None, 0, 0, 32)
        self.title_blit_position = (int((self.game_display.get_width() - self.title[0].get_width()) / 2),
                                   100)

        self.text = self.font.render("Press Space to Start", (255, 255, 255))
        self.text_blit_position = (int((self.game_display.get_width() - self.text[0].get_width()) / 2),
                                   200)

    def handle_events(self, events: list = None):
        current_keys = pg.key.get_pressed()
        if current_keys[pg.K_SPACE]:
            self.manager.switch_to_scene(GameScene())

    def update(self):
        self.scrolling_background_1.update(0.2)
        self.scrolling_background_2.update(0.5)
        self.scrolling_background_3.update(0.8)

    def render(self, surface: pg.Surface):
        self.static_background.draw()
        self.scrolling_background_1.draw()
        self.scrolling_background_2.draw()
        self.scrolling_background_3.draw()

        self.game_display.blit(self.title[0], self.title_blit_position)
        self.game_display.blit(self.text[0], self.text_blit_position)

        surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))


class GameScene(Scene):
    def __init__(self):
        self.manager = SceneManager(self)

        self.game_display = pg.Surface(SURFACE_SIZE)                     # Initialize surface for drawing

        self.game_map = Map('assets/maps/map2.txt')  # Game Map (as 2D array)

        self.camera = Camera(SURFACE_SIZE, self.game_map)  # Initialize camera

        self.player = Player()  # Initialize player
        self.player_sprite_group = pg.sprite.GroupSingle(self.player)  # Initialize player sprite group

        self.terrain_group = self.game_map.terrain_group  # Initialize terrain sprite group

        self.all_sprites_group = pg.sprite.Group()  # Initialize all sprites group
        self.all_sprites_group.add(self.player)
        self.all_sprites_group.add(self.terrain_group.sprites())

        self.static_background = StaticBackground("assets/textures/Hills Layer 01.png", self.game_display)
        self.parallax_background_1 = ParallaxBackground("assets/textures/Hills Layer 02.png", self.game_display)
        self.parallax_background_2 = ParallaxBackground("assets/textures/Hills Layer 03.png", self.game_display)
        self.parallax_background_3 = ParallaxBackground("assets/textures/Hills Layer 04.png", self.game_display)

    def handle_events(self, events: list = None):
        current_keys = pg.key.get_pressed()
        self.player.move(current_keys[pg.K_LEFT], current_keys[pg.K_RIGHT], current_keys[pg.K_SPACE], self.game_map)

    def update(self):
        if self.player.is_dead(self.game_map):
            #transition to a new state
            self.manager.switch_to_scene(GameOverScene())

        self.camera.follow_target(self.player)                          # Move camera to player's position

        self.parallax_background_1.update(self.camera, 0.2)
        self.parallax_background_2.update(self.camera, 0.5)
        self.parallax_background_3.update(self.camera, 0.8)

    def render(self, surface):
        self.static_background.draw()
        self.parallax_background_1.draw()
        self.parallax_background_2.draw()
        self.parallax_background_3.draw()

        self.camera.draw(self.game_display, self.terrain_group)  # Draw terrain sprites on game display

        self.player.draw(self.game_display, self.camera)  # Draw player sprite on game display

        surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0)) # Renders the display onto the window



class GameOverScene(Scene):
    def __init__(self):
        self.manager = SceneManager(self)
        self.game_display = pg.Surface(SURFACE_SIZE)  # Initialize surface for drawing

        freetype.init()
        self.font = freetype.Font("assets/fonts/pixChicago.ttf", 8)

        self.title = self.font.render("get rekt son", (235, 235, 235), None, 0, 0, 32)
        self.title_blit_position = (int((self.game_display.get_width() - self.title[0].get_width()) / 2),
                                    100)

        self.subtitle = self.font.render("Press F to pay respects", (235, 235, 235))
        self.subtitle_blit_position = (int((self.game_display.get_width() - self.subtitle[0].get_width()) / 2),
                                       200)

    def handle_events(self, events: list = None):
        current_keys = pg.key.get_pressed()
        if current_keys[pg.K_f]:
            self.manager.switch_to_scene(GameScene())

    def update(self):
        pass

    def render(self, surface: pg.Surface):
        self.game_display.fill((20, 20, 20))

        self.game_display.blit(self.title[0], self.title_blit_position)
        self.game_display.blit(self.subtitle[0], self.subtitle_blit_position)

        surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))  # Renders the display onto the window








