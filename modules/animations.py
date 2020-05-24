import pygame as pg
from .camera import Camera

class Spritesheet:
    def __init__(self, filepath: str, rows: int, columns: int, width=None, height=None):
        self.spritesheet = pg.image.load(filepath).convert_alpha()
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        if width == None:
            self.width = int(self.spritesheet.get_width() / columns)
        if height == None:
            self.height = int(self.spritesheet.get_height() / rows)

        self.clock = pg.time.Clock()


    def get_image_at_position(self, position: int):
        # positions are 0-indexed
        image_row = int(position / self.columns)
        image_column = position % self.columns
        surface = pg.Surface((self.width, self.height)).convert_alpha()
        surface.blit(self.spritesheet, (0, 0), pg.Rect((image_column * self.width,
                                                        image_row * self.height,
                                                        (image_column + 1) * self.width,
                                                        (image_row + 1) * self.height)
                                                      ))
        return surface

    def get_images_at(self, *positions: int):
        # positions goes from left to right, then go down one row.
        return [self.get_image_at_position(position) for position in positions]



class Animation:
    def __init__(self, animation_sequence: list):
        self.animation_sequence = animation_sequence
        self.index = 0
        self.frame_count = len(animation_sequence)

        self.frames_per_image = 3
        self.frame_counter = 0

    def get_current_frame(self):
        return self.animation_sequence[self.index]

    # add an update function to only call get_next_frame based on the time passed
    def update_image(self):
        if self.frame_counter >= self.frames_per_image:
            self.frame_counter = 0
            self.index += 1
            self.index = self.index % self.frame_count
            return True
        else:
            self.frame_counter += 1
            return False


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
        """Draws the image on the surface"""
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





