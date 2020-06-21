import pygame as pg
from modules.spritesheet import Tileset, TerrainType


# This is basically hardcoding, but there is no choice here
# Can implement reading from JSON to make this more modular
class TextureSet:
    """Contains a dictionary of the types of tiles and its corresponding TerrainType objects,
    and allows for the retrieval for the corresponding TerrainType object of the specified tile type"""
    def __init__(self):
        ruby = Tileset("assets/textures/environment/animated/ruby.png")
        tileset = Tileset("assets/textures/environment/static/terrain.png")
        decorations = Tileset("assets/textures/environment/static/decorations.png")
        self.textures = {
            # ------------------------------ INTERACTIVE BLOCKS ------------------------------ #
            "SPIKES_UPRIGHT": TerrainType(decorations.get_image_at(pg.Rect(208, 196, 16, 16)), 0, 0.4, 1, 0.6),
            "ENTRANCE/EXIT": TerrainType(tileset.get_image_at(pg.Rect(1584, 464, 32, 28)), 0, -0.5, 1, 1.5),
            "COIN": TerrainType(ruby.get_image_at(pg.Rect(0, 0, 15, 16)), 0, 0, 15/16, 1),
            "FALLING_BLOCK": TerrainType(tileset.get_image_at(pg.Rect(208, 672, 32, 32))),
            "MOVING_BLOCK": TerrainType(pg.image.load("assets/textures/cloud.png")),
            "LADDER": TerrainType(decorations.get_image_at(pg.Rect(184, 16, 32, 32))),
            "PUSHABLE": TerrainType(decorations.get_image_at(pg.Rect(209, 113, 13, 13))),

            # ------------------------------ COLLIDEABLE BLOCKS ------------------------------ #
            "CORNER_BOTTOM_LEFT":   TerrainType(tileset.get_image_at(pg.Rect(160, 720, 32, 32))),
            "CORNER_BOTTOM_RIGHT":  TerrainType(tileset.get_image_at(pg.Rect(512, 720, 32, 32))),
            "CORNER_TOP_LEFT_1":    TerrainType(tileset.get_image_at(pg.Rect(160, 448, 32, 32))),
            "CORNER_TOP_LEFT_2":    TerrainType(tileset.get_image_at(pg.Rect(192, 448, 32, 32))),
            "CORNER_TOP_LEFT_3":    TerrainType(tileset.get_image_at(pg.Rect(160, 480, 32, 32))),
            "CORNER_TOP_LEFT_4":    TerrainType(tileset.get_image_at(pg.Rect(192, 480, 32, 32))),
            "CORNER_TOP_RIGHT_1":   TerrainType(tileset.get_image_at(pg.Rect(480, 448, 32, 32))),
            "CORNER_TOP_RIGHT_2":   TerrainType(tileset.get_image_at(pg.Rect(512, 448, 32, 32))),
            "CORNER_TOP_RIGHT_3":   TerrainType(tileset.get_image_at(pg.Rect(480, 480, 32, 32))),
            "CORNER_TOP_RIGHT_4":   TerrainType(tileset.get_image_at(pg.Rect(512, 480, 32, 32))),
            "WALL_LEFT":            TerrainType(tileset.get_image_at(pg.Rect(160, 672, 32, 32))),
            "WALL_RIGHT":           TerrainType(tileset.get_image_at(pg.Rect(512, 672, 32, 32))),
            "CEILING":              TerrainType(tileset.get_image_at(pg.Rect(240, 448, 32, 32))),
            "FLOOR":                TerrainType(tileset.get_image_at(pg.Rect(240, 720, 32, 32))),

            # ------------------------------ NON-COLLIDEABLE BLOCKS ------------------------------ #
            "BG_FILLER":               TerrainType(tileset.get_image_at(pg.Rect(48, 544, 32, 32))),
            "BG_WALL":              TerrainType(tileset.get_image_at(pg.Rect(1328, 472, 32, 32))),
            "BG_WALL_BOTTOM_HALF":  TerrainType(tileset.get_image_at(pg.Rect(1328, 488, 32, 16)), 0, 0.5, 1, 0.5),
            "BG_WINDOW_DOUBLE":    TerrainType(tileset.get_image_at(pg.Rect(1088, 240, 144, 128)), 0, 0, 4.5, 4),
            # single window adds one extra pixel to eliminate a hole
            "BG_WINDOW_SINGLE":     TerrainType(tileset.get_image_at(pg.Rect(1472, 96, 65, 64)), -0.5, -0.40625, 2, 2),
            # barred window adds one extra pixel to eliminate a hole
            "BG_WINDOW_BARRED":     TerrainType(tileset.get_image_at(pg.Rect(1552, 119, 32, 42)), 0, -0.28125, 1, 1.28125),
            "BG_SHELF_POTIONS":     TerrainType(decorations.get_image_at(pg.Rect(16, 64, 32, 64)), 0, -1, 1, 2),
            "BG_SHELF_BOOKS":       TerrainType(decorations.get_image_at(pg.Rect(16, 144, 32, 64)), 0, -1, 1, 2),
            "BG_SHELF_EMPTY":       TerrainType(decorations.get_image_at(pg.Rect(64, 144, 32, 64)), 0, -1, 1, 2),
            "BG_BANNER_RED_LARGE_1":  TerrainType(decorations.get_image_at(pg.Rect(304, 305, 112, 80)), -0.25, 0, 3.5, 2.5),
            "BG_BANNER_RED_LARGE_2": TerrainType(decorations.get_image_at(pg.Rect(496, 209, 112, 80)), -0.25, 0, 3.5, 2.5),

        }

        # TODO: Sort this in alphabetical order
        self.code_to_texture_dictionary = {"f1": "FLOOR",
                                           "l1": "WALL_LEFT",
                                           "r1": "WALL_RIGHT",
                                           "c1": "CEILING",
                                           "xx": "BG_FILLER",
                                           "bl": "CORNER_BOTTOM_LEFT",
                                           "br": "CORNER_BOTTOM_RIGHT",
                                           "k1": "CORNER_TOP_LEFT_1",
                                           "k2": "CORNER_TOP_LEFT_2",
                                           "k3": "CORNER_TOP_LEFT_3",
                                           "k4": "CORNER_TOP_LEFT_4",
                                           "k5": "CORNER_TOP_RIGHT_1",
                                           "k6": "CORNER_TOP_RIGHT_2",
                                           "k7": "CORNER_TOP_RIGHT_3",
                                           "k8": "CORNER_TOP_RIGHT_4",
                                           "SP": "SPIKES_UPRIGHT",
                                           "GW": "ENTRANCE/EXIT",
                                           "CN": "COIN",
                                           "FB": "FALLING_BLOCK",
                                           "MB": "MOVING_BLOCK",
                                           "LB": "LADDER",
                                           "PB": "PUSHABLE",
                                           "wl": "BG_WALL",
                                           "wb": "BG_WALL_BOTTOM_HALF",
                                           "2w": "BG_WINDOW_DOUBLE",
                                           "1w": "BG_WINDOW_SINGLE",
                                           "bw": "BG_WINDOW_BARRED",
                                           "s1": "BG_SHELF_POTIONS",
                                           "s2": "BG_SHELF_BOOKS",
                                           "s3": "BG_SHELF_EMPTY",
                                           "b1": "BG_BANNER_RED_LARGE_1",
                                           "b2": "BG_BANNER_RED_LARGE_2"
                                           }

    def get_texture_from_code(self, code) -> TerrainType:
        """Returns the corresponding TerrainType object associated with the specified tile"""
        return self.textures[self.code_to_texture_dictionary[code]]