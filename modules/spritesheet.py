import pygame as pg

"""
* =============================================================== *
* This module contains all the necessary utility functions        *
* required to load textures into the game.                        *
* The Spritesheet class allows you to load animations (sequences  *
* of frames) from spritesheets.                                   *
* The Tileset class allows you to load static textures from a     *
* spritesheet.                                                    *
* =============================================================== *

ADDING NEW TEXTURES TO THE TEXTURESET
--------------------------------------
1.  Add a new entry to the "textures" dictionary, with the string literal of the terrain type as the key
    and a TerrainType object containing the texture as the value
    Optional arguments can also be passed to the TerrainType constructor to specify the hitbox of the object 
    (this technically allows for larger objects to be instantiated)
2.  Add a new entry to the "code_to_textures_dictionary", with the string representation of the tile in the 
    .txt map file as the key, and the string literal of the terrain type as the value
"""


class Spritesheet:
    """Utility class to load animation sequences from a spritesheet"""
    def __init__(self, filepath: str, rows: int, columns: int, width=None, height=None):
        self.spritesheet = pg.image.load(filepath)
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        if width is None:
            self.width = int(self.spritesheet.get_width() / columns)
        if height is None:
            self.height = int(self.spritesheet.get_height() / rows)
        self.clock = pg.time.Clock()

    def get_image_at_position(self, position: int) -> pg.Surface:
        """Returns an image at the specified position, representing a single frame of an animation"""
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

    def get_images_at(self, *positions: int) -> list:
        """Returns a sequence of Surfaces representing the specified sequence of frames,
            which represents an animation sequence"""
        # Positions goes from left to right, then go down one row
        return [self.get_image_at_position(position) for position in positions]


# -------------------- Type objects to store hitboxes of different textures -------------------- #
# This level of complication is really just to make life easier
class TerrainType:
    """Stores a texture and its corresponding hitbox dimensions"""
    def __init__(self, image: pg.Surface, block_pos_x=0, block_pos_y=0, block_width=1, block_height=1):
        # All numbers are relative to the size of a normal block
        # (i.e. must be between 0 and 1, where 1 is the size of an actual block)
        self.image = image
        self.block_pos_x = block_pos_x
        self.block_pos_y = block_pos_y
        self.block_width = block_width
        self.block_height = block_height


class Tileset:
    """Utility class to load static textures from a spritesheet"""
    def __init__(self):
        self.spritesheet = pg.image.load("assets/textures/Dungeon/dungeon_spritesheet.png")

    def get_image_at(self, rectangle, colorkey=None) -> pg.Surface:
        """Loads the image at the area specified by the given rectangle"""
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()

        # TODO: Convert to subsurface
        image.blit(self.spritesheet, (0, 0), rect)

        if colorkey is None:
            image.set_colorkey((0, 0, 0))
        else:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pg.RLEACCEL)

        return image


# This is basically hardcoding, but there is no choice here
# Can implement reading from JSON to make this more modular
class TextureSet:
    """Contains a dictionary of the types of tiles and its corresponding TerrainType objects,
    and allows for the retrieval for the corresponding TerrainType object of the specified tile type"""
    def __init__(self):
        tileset = Tileset()
        temp_texture = pg.Surface((16, 16)).fill((255, 0, 255))
        self.textures = {"FLOOR_LEFT_EDGE": TerrainType(tileset.get_image_at(pg.Rect(32, 0, 16, 16))),
                         "FLOOR_CENTER_EDGE": TerrainType(tileset.get_image_at(pg.Rect(48, 0, 16, 16))),
                         "FLOOR_RIGHT_EDGE": TerrainType(tileset.get_image_at(pg.Rect(64, 0, 16, 16))),
                         "SPIKES_UPRIGHT": TerrainType(tileset.get_image_at(pg.Rect(80, 96, 16, 16)), 0, 0.4, 1, 0.6),
                         "ENTRANCE/EXIT": TerrainType(tileset.get_image_at(pg.Rect(224, 32, 16, 16))),
                         "COIN": TerrainType(tileset.get_image_at(pg.Rect(240, 0, 16, 16))),
                         "FALLING BLOCK": TerrainType(tileset.get_image_at(pg.Rect(96, 0, 16, 16))),
                         "MOVING BLOCK": TerrainType(pg.image.load("assets/textures/cloud.png"))
                         }

        self.code_to_texture_dictionary = {"2": "FLOOR_LEFT_EDGE",
                                           "3": "FLOOR_CENTER_EDGE",
                                           "4": "FLOOR_RIGHT_EDGE",
                                           "s": "SPIKES_UPRIGHT",
                                           "e": "ENTRANCE/EXIT",
                                           "c": "COIN",
                                           "f": "FALLING BLOCK",
                                           "m": "MOVING BLOCK"
                                           }

    def get_texture_from_code(self, code) -> TerrainType:
        """Returns the corresponding TerrainType object associated with the specified tile"""
        if code == "x":
            pass
        else:
            return self.textures[self.code_to_texture_dictionary[code]]