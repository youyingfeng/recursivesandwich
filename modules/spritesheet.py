import pygame as pg 


'''A Spritesheet is an image containing all the individual frames of a Sprite,
which can be extracted for animation.'''


# -------------------- Type objects to store hitboxes of different textures -------------------- #
# This level of complication is really just to make life easier
class TerrainType:
    def __init__(self, image: pg.Surface, block_pos_x=0, block_pos_y=0, block_width=1, block_height=1):
        # All numbers are relative to the size of a normal block (i.e. must be between 0 and 1, where 1 is the size of an actual block)
        self.image = image
        self.block_pos_x = block_pos_x
        self.block_pos_y = block_pos_y
        self.block_width = block_width
        self.block_height = block_height


class Spritesheet:
    def __init__(self, filepath: str, rows: int, columns: int, width=None, height=None):
        self.spritesheet = pg.image.load(filepath)
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        if width == None:
            self.width = int(self.spritesheet.get_width() / columns)
        if height == None:
            self.height = int(self.spritesheet.get_height() / rows)
        self.clock = pg.time.Clock()

    # Returns an image representing a single tile from a spritesheet
    def get_image_at_coordinates(self, row, col):
        image_row = row
        image_column = col

        # Create a new transparent Surface
        surface = pg.Surface((self.width, self.height)).convert()
        surface.set_colorkey((0, 0, 0))

        # Blit frame into the transparent Surface, scaled to Surface size
        surface.blit(self.spritesheet, (0, 0), 
            pg.Rect((image_column * self.width,
                    image_row * self.height,
                    (image_column + 1) * self.width,
                    (image_row + 1) * self.height)))
        return surface

    # Returns an image representing a single frame of an animation
    def get_image_at_position(self, position: int) -> pg.Surface:
        # Positions are 0-indexed
        image_row = int(position / self.columns)
        image_column = position % self.columns

        # Create a new transparent Surface
        surface = pg.Surface((self.width, self.height)).convert()
        surface.set_colorkey((0, 0, 0))

        # Blit frame into the transparent Surface, scaled to Surface size
        surface.blit(self.spritesheet, (0, 0), 
            pg.Rect((image_column * self.width,
                    image_row * self.height,
                    (image_column + 1) * self.width,
                    (image_row + 1) * self.height)))
        return surface

    '''Returns a list of frames within the animation,
    to be passed into the Animation constructor'''
    def get_images_at(self, *positions: int) -> list:
        # Positions goes from left to right, then go down one row
        return [self.get_image_at_position(position) for position in positions]


class Tileset:
    def __init__(self):
        self.spritesheet = pg.image.load("assets/textures/Dungeon/dungeon_spritesheet.png")

    def get_image_at(self, rectangle, colorkey=None) -> pg.Surface:
        '''Loads image from x,y,x+offset,y+offset'''
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.spritesheet, (0, 0), rect)

        if colorkey is None:
            image.set_colorkey((0, 0, 0))
        else:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pg.RLEACCEL)

        return image


# TODO: Make a textureset manually getting each tile from the right position.
# This is basically hardcoding, but there is no choice here
# Can implement reading from JSON to make this more modular
class TextureSet:
    def __init__(self):
        tileset = Tileset()
        temp_texture = pg.Surface((16, 16)).fill(255, 0, 255)
        self.textures = {"FLOOR_LEFT_EDGE": TerrainType(tileset.get_image_at(pg.Rect(32, 0, 16, 16))),
                         "FLOOR_CENTER_EDGE": TerrainType(tileset.get_image_at(pg.Rect(48, 0, 16, 16))),
                         "FLOOR_RIGHT_EDGE": TerrainType(tileset.get_image_at(pg.Rect(64, 0, 16, 16))),
                         "SPIKES_UPRIGHT": TerrainType(tileset.get_image_at(pg.Rect(80, 96, 16, 16)), 0, 0.4, 1, 0.6),
                         "ENTRANCE/EXIT": TerrainType(temp_texture),
                         "COIN": TerrainType(tileset.get_image_at(pg.Rect(240, 0, 16, 16)))
                         }

        self.code_to_texture_dictionary = {"2": "FLOOR_LEFT_EDGE",
                                           "3": "FLOOR_CENTER_EDGE",
                                           "4": "FLOOR_RIGHT_EDGE",
                                           "s": "SPIKES_UPRIGHT",
                                           "e": "ENTRANCE/EXIT",
                                           "c": "COIN"
                                           }

    def get_texture_from_code(self, code) -> TerrainType:
        if code == "x":
            pass
        else:
            return self.textures[self.code_to_texture_dictionary[code]]