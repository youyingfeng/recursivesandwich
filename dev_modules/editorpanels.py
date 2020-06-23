import pygame as pg
import json

from dev_modules.events import EditorEvents
from modules.textureset import TextureSet
from modules.leveljson import *
from dev_modules.editorlevel import *
from dev_modules.editorcamera import EditorCamera


class MapPanel:
    def __init__(self, filepath):
        self.camera = EditorCamera()
        self.level = EditorLevel(filepath)
        self.boundaries = (len(self.level.map.bg_array[0]) * Block.BLOCK_SIZE,
                           len(self.level.map.bg_array) * Block.BLOCK_SIZE)

    def click(self, point):
        # handle events given the click point
        pass

    def update(self):
        current_keys = pg.key.get_pressed()
        self.camera.update(current_keys[pg.K_UP],
                           current_keys[pg.K_DOWN],
                           current_keys[pg.K_LEFT],
                           current_keys[pg.K_RIGHT],
                           self.boundaries)

    def render(self, surface):
        surface.fill((100, 100, 100))
        self.level.render(self.camera, surface)


class PalettePanel:
    def __init__(self):
        # TODO: Render Surface != Actual position, so rect will collide
        # place Map on the left and palette on the right

        # There is the top text

        # then there are the bottom icons
        self.buttons_group = pg.sprite.Group()

    def click(self, point):
        pass

    def update(self):
        pass

    def render(self, surface):
        surface.fill((35, 88, 112))


class TextureButton:
    def __init__(self, code, coordinates):
        textureset = TextureSet()
        self.code = code
        terraintype = textureset.get_texture_from_code(code)
        self.image = terraintype.image
        self.rect = pg.Rect(coordinates,
                            (terraintype.block_width * Block.BLOCK_SIZE,
                             terraintype.block_height * Block.BLOCK_SIZE)
                            )

    def on_click(self):
        pg.event.post(
            pg.event.Event(
                EditorEvents.BLOCK_SWITCH,
                self.code
            )
        )





