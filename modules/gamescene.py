import pygame as pg

from .player import Player
from .camera import Camera
from .map import Map
from .animations import StaticBackground, ParallaxBackground

from .scenemanager import Scene, SceneManager

# Globals
WINDOW_SIZE = (800, 600)
SURFACE_SIZE = (400, 300)


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

    def handle_events(self, events=None):
        current_keys = pg.key.get_pressed()
        self.player.move(current_keys[pg.K_LEFT], current_keys[pg.K_RIGHT], current_keys[pg.K_SPACE], self.game_map)

    def update(self):
        if self.player.is_dead(self.game_map):
            #transition to a new state
            self.manager.switch_to_scene(GameScene())


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
