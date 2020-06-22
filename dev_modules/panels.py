import pygame as pg
import json

from modules.textureset import TextureSet
from modules.leveljson import *


class MapPanel:
    def __init__(self, filepath):
        self.camera = EditorCamera()

    def click(self, point):
        # handle events given the click point
        pass

    def update(self):
        pass

    def render(self, surface):
        surface.fill((80, 150, 100))


class PalettePanel:
    def __init__(self):
        # TODO: Render Surface != Actual position, so rect will collide
        # place Map on the left and palette on the right
        textureset = TextureSet()

    def click(self, point):
        pass

    def update(self):
        pass

    def render(self, surface):
        surface.fill((35, 88, 112))


class EditorCamera:
    def __init__(self):
        self.rect = pg.Rect(0, 0, 400, 300)

    def scroll(self, up: bool, down: bool, left: bool, right: bool, boundaries: list):
        if up is True:
            self.rect.y -= 5
        if down is True:
            self.rect.y += 5
        if left is True:
            self.rect.x -= 5
        if right is True:
            self.rect.x += 5

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > boundaries[0]:
            self.rect.right = boundaries[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > boundaries[1]:
            self.rect.bottom = boundaries[1]
