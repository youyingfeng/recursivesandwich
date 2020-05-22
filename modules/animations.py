import pygame as pg

class Spritesheet:
    def __init__(self, file_path):
        # TODO: wrap in try-catch block
        self.sheet = pg.image.load(file_path).convert()

    def get_image_at(self, rectangle, colorkey=None):
        # Let the sheet span from 0,0 to whatever its bounds.
        # The rectangle is a rect floating within this span
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

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






