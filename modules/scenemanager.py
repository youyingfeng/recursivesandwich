class Scene:
    # Scenes form the baseline of our game. Example scenes are the splash screen, game screen, pause screen, etc
    # This needs to be extended by all individual scenes

    def __init__(self):
        pass

    def handle_events(self, events: list):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError


class SceneManager:
    # Every scene has a scene manager. The scene manager is the same (self) throughout all called classes,
    # so you wont end up with a fuckload of objects
    def __init__(self, scene: Scene):
        self.scene = scene

    def switch_to_scene(self, scene: Scene):
        self.scene = scene
        self.scene.manager = self
