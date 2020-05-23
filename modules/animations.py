import pygame as pg
from .camera import Camera

class Spritesheet:
    def __init__(self, file_path):
        # TODO: wrap in try-catch block
        self.sheet = pg.image.load(file_path).convert_alpha()

    def get_image_at(self, rectangle, colorkey=None):
        # Let the sheet span from 0,0 to whatever its bounds.
        # The rectangle is a rect floating within this span
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.get_image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class Animation():
# Stores a sequence of sprites to be animated.
    def __init__(self, animation_sequence):
        self.animation_sequence = animation_sequence
        self.current_frame_index = 0
        self.number_of_frames = len(animation_sequence)

    def update(self):
        # temporary - tick based animations - move to next frame everytime this is called.
        # ideally, should use time based animations - move only after a certain time
        # This function is called everytime a draw call happens, to update the image within the sprite.
        if self.current_frame_index == self.number_of_frames - 1:
            self.current_frame_index = 0
        else:
            self.current_frame_index += 1
        return self.animation_sequence[self.current_frame_index]

    def get_image(self):
        return self.animation_sequence[self.current_frame_index]


# For Background
# Background has two methods: update and draw. Takes a Map in the constructor
# Update takes a player and updates the scrolling of the bg based on its position relative to the Map
# Draw draws the background onto the specified surface

class StaticBackground:
    def __init__(self, filepath: str, surface: pg.Surface):
        # Preprocessing so that i dont have to do cancer math every time
        self.surface = surface
        self.image = pg.image.load(filepath).convert()
        self.background = pg.transform.scale(self.image,
                                        (self.image.get_width()
                                            * int(surface.get_height()
                                                  / self.image.get_height()),
                                         surface.get_height()))
        self.BLIT_COORDINATES = ((self.surface.get_width() - self.background.get_width()) / 2, 0)


    def draw(self):
        self.surface.blit(self.background, self.BLIT_COORDINATES)

class ParallaxBackground:
    def __init__(self, filepath: str, surface: pg.Surface):
        # structure of the bg is 2 rect surfaces side by side
        self.image = pg.image.load(filepath).convert_alpha()
        self.background = pg.transform.scale(self.image,
                                             (self.image.get_width()
                                                * int(surface.get_height()
                                                        / self.image.get_height()),
                                              surface.get_height()))

        self.surface = surface                  # This is the surface that the BG will be drawn on
        self.blit_position = 0                  # This is the x-coordinate of the position where the BG will be blitted

        # Constants to make math easier on system, since calling this 60 times per second is wasteful
        self.BACKGROUND_WIDTH = self.background.get_width()
        self.BACKGROUND_HEIGHT = self.background.get_height()

    def update(self, camera: Camera, speed: float):
        """Updates the position where the image should be blitted to make the image "move" with the camera"""
        # target is the rect of the camera
        # updates the position of the background relative to the camera position

        # What i can do is instead of scrolling, place 2 bg side by side, then use modulo to place a rect representing
        # camera in the correct spot, then blit bg on the rect and then blit rect on the surface
        current_x_position = camera.rect.left
        self.blit_position = - int(current_x_position * speed) % self.BACKGROUND_WIDTH

    def draw(self):
        """Draws the image onto the background"""
        self.surface.blit(self.background, (self.blit_position, 0))
        self.surface.blit(self.background, (self.blit_position - self.BACKGROUND_WIDTH, 0))





