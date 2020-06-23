import pygame as pg
import pygame.freetype as ft

from dev_modules.events import EditorEvents
from dev_modules.editorpanels import PalettePanel, MapPanel


class Scene:
    """Represents a scene in the program, which is analogous to the state of the game"""

    def __init__(self):
        self.manager = SceneManager(self)
        self.game_display = pg.Surface((525, 300))

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


class MapLoaderScene(Scene):
    def __init__(self):
        super().__init__()
        self.filepath = "assets/levels/"
        self.focus = True

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                pass
            elif self.focus is True:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.manager.switch_to_scene(MapEditorScene(self.filepath))
                    elif event.key == pg.K_BACKSPACE:
                        # array slicing is safe from null pointers
                        self.filepath = self.filepath[:-1]
                    else:
                        self.filepath += event.unicode

    def update(self):
        pass

    def render(self, surface):
        surface.fill((100, 100, 100))
        # blit the text onto the surface


class MapEditorScene(Scene):
    def __init__(self, filepath):
        super().__init__()
        self.palette_display = pg.Surface((125, 300))
        self.map_display = pg.Surface((400, 300))

        self.palette_panel = PalettePanel()
        self.map_panel = MapPanel(filepath)

    def handle_events(self):
        # use events to coordinate the current selected block
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                point = [event.pos[0], event.pos[1]]
                if point[0] < 125:
                    self.palette_panel.click(point)
                else:
                    point[0] -= 125
                    self.map_panel.click(point)
            elif event.type == EditorEvents.BLOCK_SWITCH:
                pass

    def update(self):
        self.map_panel.update()
        # pass

    def render(self, surface: pg.Surface):
        self.palette_panel.render(self.palette_display)
        self.map_panel.render(self.map_display)

        self.game_display.blit(self.palette_display, (0, 0))
        self.game_display.blit(self.map_display, (125, 0))

        surface.blit(pg.transform.scale(self.game_display, (1050, 600)), (0, 0))
