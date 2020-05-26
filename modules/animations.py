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
        surface = pg.Surface((self.width, self.height))
        surface.blit(self.spritesheet, (0, 0), pg.Rect((image_column * self.width,
                                                        image_row * self.height,
                                                        (image_column + 1) * self.width,
                                                        (image_row + 1) * self.height)
                                                      ))
        surface.set_colorkey((0, 0, 0))
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