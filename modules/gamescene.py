import pygame as pg
import pygame.freetype as ft
from .leveljson import *
from .entities import Player
from .camera import Camera
from .background import *
from .headsupdisplay import HeadsUpDisplay
from .entitystate import GameEvent

"""
* =============================================================== *
* This module contains all the different scenes that make up the  *
* game.															  *
* A scene is effectively analogous to the state of the game.	  *
*	e.g. There is a scene to represent the Title Screen, the Game *
*		 screen, the Game Over screen, etc.						  *
* =============================================================== *

SCENES
-------------------------
All scenes must support the following methods, which are invoked on every cycle of the game loop:
    handle_events()		->		Processes all events currently waiting in the event queue
                                Event queue must be regularly emptied, otherwise new events 
                                will be dropped if the queue is full
    update()			->		Updates the state of the elements in the scene
    render()			->		Renders the elements of the scene onto the surface
    
Additionally, all scenes will have a manager attribute, which contains a SceneManager object to facilitate 
transitions between scenes.

SCENE MANAGER
-------------------------
- TO BE COMPLETED -
"""

# Size tuples
WINDOW_SIZE = (800, 600)
SURFACE_SIZE = (400, 300)

# Freetype font
# Initialise the FreeType font system
ft.init()
freetype = ft.Font("assets/fonts/pixChicago.ttf", 8)


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
        # TODO: Implement previous_scene as stack without dictionary
        self.scene = scene
        self.scene.manager = self
        self.previous_scene = None

    def switch_to_scene(self, scene: Scene):
        self.previous_scene = self.scene
        self.scene = scene
        self.scene.manager = self

    def go_to_previous_scene(self):
        self.scene = self.previous_scene
        self.scene.manager = self


class TitleScene(Scene):
    """Represents the title screen"""

    def __init__(self):
        super().__init__()

        # Backgrounds
        self.backgrounds = (StaticBackground("assets/textures/background/01_background.png", self.game_display),
                            StaticBackground("assets/textures/background/03 background B.png", self.game_display),
                            StaticBackground("assets/textures/background/04 background.png", self.game_display))

        # Initialize title text
        self.title = freetype.render("THE TOWER", (70, 35, 35), None, 0, 0, 32)
        self.title_blit_position = (int((self.game_display.get_width() - self.title[0].get_width()) / 2), 100)

        # Initialize instruction text
        self.text = freetype.render("Press space to begin", (200, 200, 200))
        self.text_blit_position = (int((self.game_display.get_width() - self.text[0].get_width()) / 2), 200)

        # Play BGM
        pg.mixer.music.load("assets/sound/music/Debris of the Lost.ogg")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

    def handle_events(self):
        # Clears the event queue and processes the events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # Starts the game
                    self.manager.switch_to_scene(GameScene())

    def update(self):
        pass

    def render(self, surface: pg.Surface):
        # Blit backgrounds on game_display
        for background in self.backgrounds:
            background.render()

        # Blit text on game_display
        self.game_display.blit(self.title[0], self.title_blit_position)
        self.game_display.blit(self.text[0], self.text_blit_position)

        # Blit game_display on window surface
        surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))


class GameScene(Scene):
    """Represents the actual game screen"""

    def __init__(self):
        super().__init__()

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
        self.backgrounds = (StaticBackground("assets/textures/background/01_background.png", self.game_display),
                            StaticBackground("assets/textures/background/03 background B.png", self.game_display),
                            StaticBackground("assets/textures/background/04 background.png", self.game_display))


        # Play BGM
        pg.mixer.music.load("assets/sound/music/Deep Dream.ogg")
        pg.mixer.music.set_volume(0.8)
        pg.mixer.music.play(-1)

    def handle_events(self):
        # Clears the event queue and processes the events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.mixer.music.pause()
                    self.manager.switch_to_scene(PauseScene())
            elif event.type == GameEvent.SWITCH_LEVEL.value:
                self.level_manager.load_next_level(self.player, self.camera)
                self.manager.switch_to_scene(LoadingScene())
            elif event.type == GameEvent.GAME_OVER.value:
                self.manager.switch_to_scene(GameOverScene())
            elif event.type == GameEvent.GAME_COMPLETE.value:
                # this is unnecessary
                self.manager.switch_to_scene(GameBeatenScene())

        # Processes the input for the player
        self.player.handle_input()

    def update(self):
        self.player.update(self.level_manager.level.map)
        self.level_manager.level.update(self.player)
        self.hud.update(self.player, self.camera)

        # Move camera to player's position
        self.camera.follow_target(self.player)

    def render(self, surface):
        # Blit backgrounds on game_display
        for background in self.backgrounds:
            background.render()

        # Draws the map and enemies
        self.level_manager.level.render(self.camera, self.game_display)

        # Draw player on game_display wrt camera position
        self.player.render(self.camera, self.game_display)

        # Draw GUI
        self.hud.render(self.game_display)

        # Blit game_display on window surface
        surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))

    def initialise(self):
        pass

    def cleanup(self):
        pass


class GameOverScene(Scene):
    """Represents the "Game Over" screen"""

    def __init__(self):
        super().__init__()

        # Initialize title
        self.title = freetype.render("GAME OVER", (235, 235, 235), None, 0, 0, 32)
        self.title_blit_position = (int((self.game_display.get_width() - self.title[0].get_width()) / 2), 100)

        # Initialize subtitle
        self.subtitle = freetype.render("Press F to pay respects", (235, 235, 235))
        self.subtitle_blit_position = (int((self.game_display.get_width() - self.subtitle[0].get_width()) / 2), 200)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_f:
                # TODO: HANDLE THIS BETTER TO ENSURE NO MEMORY BLOAT
                self.manager.switch_to_scene(GameScene())

    def update(self):
        pass

    def render(self, surface: pg.Surface):
        # Fill game_display with black
        self.game_display.fill((0, 0, 0))

        # Blit title and subtitle on game_display
        self.game_display.blit(self.title[0], self.title_blit_position)
        self.game_display.blit(self.subtitle[0], self.subtitle_blit_position)

        # Blit game_display on window surface
        surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))


class GameBeatenScene(Scene):
    def __init__(self):
        super().__init__()
        # Initialize title
        self.title = freetype.render("VICTORY", (0, 0, 0), None, 0, 0, 32)
        self.title_blit_position = (int((self.game_display.get_width() - self.title[0].get_width()) / 2), 100)

        # Initialize subtitle
        self.subtitle = freetype.render("Press space to quit", (0, 0, 0))
        self.subtitle_blit_position = (int((self.game_display.get_width() - self.subtitle[0].get_width()) / 2), 200)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pg.quit()
                    quit()

    def update(self, *args):
        pass

    def render(self, surface: pg.Surface):
        # Fill game_display with black
        self.game_display.fill((235, 235, 235))

        # Blit title and subtitle on game_display
        self.game_display.blit(self.title[0], self.title_blit_position)
        self.game_display.blit(self.subtitle[0], self.subtitle_blit_position)

        # Blit game_display on window surface
        surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))


class PauseScene(Scene):
    def __init__(self):
        super().__init__()
        self.text = freetype.render("Press any key to unpause", (255, 255, 255))
        self.text_blit_position = (int((self.game_display.get_width() - self.text[0].get_width()) / 2), 200)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                pg.mixer.music.unpause()
                # Resume the game by going back to the previous scene
                self.manager.go_to_previous_scene()

    def update(self, *args):
        pass

    def render(self, surface: pg.Surface):
        self.game_display.fill((0, 0, 0))
        self.game_display.blit(self.text[0], self.text_blit_position)
        surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))


class LoadingScene(Scene):
    def __init__(self):
        super().__init__()
        self.text = freetype.render("Loading...", (255, 255, 255))
        self.text_blit_position = (int((self.game_display.get_width() - self.text[0].get_width()) / 2), 200)
        self.wait_frames = 90

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == GameEvent.GAME_COMPLETE.value:
                self.manager.switch_to_scene(GameBeatenScene())

    def update(self, *args):
        if self.wait_frames <= 0:
            self.manager.go_to_previous_scene()
        else:
            self.wait_frames -= 1

    def render(self, surface: pg.Surface):
        self.game_display.fill((0, 0, 0))

        self.game_display.blit(self.text[0], self.text_blit_position)
        surface.blit(pg.transform.scale(self.game_display, WINDOW_SIZE), (0, 0))
