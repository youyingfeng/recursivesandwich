import pygame as pg
from .camera import Camera


class Background:
    # TODO: Implement varargs to allow for proper overriding as this does not fulfil LSP
    def __init__(self, filepath: str, surface: pg.Surface):
        self.surface = surface
        self.image = pg.image.load(filepath).convert()
        self.background = pg.transform.scale(self.image, 
            (self.image.get_width() * int(surface.get_height() / self.image.get_height()), surface.get_height()))

    # Updates the scrolling of the background based on its position relative to the Map
    def update(self):
        raise NotImplementedError

    # Draws the background onto the surface attribute
    def draw(self):
        raise NotImplementedError


class StaticBackground(Background):
    def __init__(self, filepath: str, surface: pg.Surface):
        super().__init__(filepath, surface)
        self.blit_coordinates = ((self.surface.get_width() - self.background.get_width()) / 2, 0)

    def draw(self):
        self.surface.blit(self.background, self.blit_coordinates)

    def update(self):
        pass


# Used for GameScene
class ParallaxBackground(Background):
    def __init__(self, filepath: str, surface: pg.Surface):
        super().__init__(filepath, surface)
        self.image = pg.image.load(filepath).convert_alpha()
        self.background = pg.transform.scale(self.image,
            (self.image.get_width() * int(surface.get_height() / self.image.get_height()), surface.get_height()))
        
        # The x-coordinate of the position where the background will be blitted
        self.blit_position = 0

        self.BACKGROUND_WIDTH = self.background.get_width()
        self.BACKGROUND_HEIGHT = self.background.get_height()

    def update(self, camera: Camera, speed: float):
        """This function updates the background's blit_position relative to the camera's position.
        Instead of scrolling, we place two backgrounds side by side, then use modulo to place
        a Rect representing the camera in the correct spot, then blit BG on the Rec, then blit
        Rect on the surface."""
        current_x_position = camera.rect.left
        self.blit_position = - int(current_x_position * speed) % self.BACKGROUND_WIDTH

    def draw(self):
        self.surface.blit(self.background, (self.blit_position, 0))
        self.surface.blit(self.background, (self.blit_position - self.BACKGROUND_WIDTH, 0))


# Used for TitleScene
class ScrollingBackground(ParallaxBackground):
    def __init__(self, filepath: str, surface: pg.Surface):
        super().__init__(filepath, surface)

    def update(self, speed: float):
        # Updates blit_position by a set amount every time this is called
        # blit_position is now a float to allow slower updates
        self.blit_position = (self.blit_position - speed) % self.BACKGROUND_WIDTH

    def draw(self):
        integer_blit_position = int(self.blit_position)
        self.surface.blit(self.background, (integer_blit_position, 0))
        self.surface.blit(self.background, (integer_blit_position - self.BACKGROUND_WIDTH, 0))




