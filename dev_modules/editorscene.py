import pygame as pg


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
        self.filepath = ""
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
                        self.manager.switch_to_scene()
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

    def handle_events(self):
        pass

    def update(self):
        pass

    def render(self, surface: pg.Surface):
        pass
