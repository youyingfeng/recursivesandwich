import pygame as pg
import pygame.freetype as ft
import json

from dev_modules.events import EditorEvents
from modules.textureset import TextureSet
from modules.leveljson import *
from dev_modules.editorlevel import *
from dev_modules.editorcamera import EditorCamera

ft.init()
freetype = ft.Font("assets/fonts/pixChicago.ttf", 8)


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
        self.load_save_sub_panel = LoadSaveSubPanel()
        self.load_save_sub_surface = pg.Surface((125, 60))

        self.texture_selector_sub_panel = TextureSelectorSubPanel()
        self.texture_selector_sub_surface = pg.Surface((125, 240))

        # There is the top text

        # then there are the bottom icons
        self.buttons_group = pg.sprite.Group()

    def click(self, point):
        if point[1] < 60:
            self.load_save_sub_panel.click(point)

    def update(self):
        pass

    def render(self, surface):
        self.load_save_sub_panel.render(self.load_save_sub_surface)
        surface.blit(self.load_save_sub_surface, (0, 0))

        self.texture_selector_sub_panel.render(self.texture_selector_sub_surface)
        surface.blit(self.texture_selector_sub_surface, (0, 60))


class LoadSaveSubPanel:
    def __init__(self):
        # I could probably shove this in individual buttons, but im gonna save on the indirection first
        self.load = freetype.render("load file", (235, 235, 235))
        self.save = freetype.render("save file", (235, 235, 235))
        self.new = freetype.render("new file", (235, 235, 235))

        self.load_rect = self.load[1]
        self.save_rect = self.save[1]
        self.new_rect = self.new[1]

        self.load_pos = (10, 10)
        self.save_pos = (10, 25)
        self.new_pos = (10, 40)

        self.load_rect.topleft = self.load_pos
        self.save_rect.topleft = self.save_pos
        self.new_rect.topleft = self.new_pos

        print(self.load_rect)
        print(self.save_rect)
        print(self.new_rect)

        self.colliding_rect_list = (self.load_rect,
                                    self.save_rect,
                                    self.new_rect)

    def click(self, coordinates):
        if self.load_rect.collidepoint(coordinates):
            print("kek")
        elif self.save_rect.collidepoint(coordinates):
            print("kekkle")
        elif self.new_rect.collidepoint(coordinates):
            print("kappa")

    def render(self, surface):
        surface.fill((35, 88, 112))
        surface.blit(self.load[0], self.load_pos)
        surface.blit(self.save[0], self.save_pos)
        surface.blit(self.new[0], self.new_pos)


class TextureSelectorSubPanel:
    def __init__(self):
        self.camera = EditorCamera()
        textureset = TextureSet()
        next_x = 10
        next_y = 10

        self.button_array = []
        for code in textureset.code_to_texture_dictionary.keys():
            terraintype = textureset.get_texture_from_code(code)
            self.button_array.append(TextureButton(code,
                                                   (next_x, next_y),
                                                   terraintype))
            next_y += terraintype.block_height * Block.BLOCK_SIZE + 10

    def click(self, coordinates):
        for button in self.button_array:
            if button.collidepoint(coordinates):
                button.on_click()
                return

    def render(self, surface):
        surface.fill((35, 88, 112))
        for button in self.button_array:
            if self.camera.rect.colliderect(button.rect):
                surface.blit(button.image,
                             (button.rect.x - self.camera.rect.x,
                              button.rect.y - self.camera.rect.y))


class TextureButton:
    def __init__(self, code, coordinates, terraintype):
        self.code = code
        self.image = pg.transform.scale(terraintype.image.convert_alpha(),
                                        (int(terraintype.block_width * Block.BLOCK_SIZE),
                                         int(terraintype.block_height * Block.BLOCK_SIZE))
                                        )
        self.rect = pg.Rect(coordinates,
                            (int(terraintype.block_width * Block.BLOCK_SIZE),
                             int(terraintype.block_height * Block.BLOCK_SIZE))
                            )

    def collidepoint(self, coordinates):
        return self.rect.collidepoint(coordinates)

    def on_click(self):
        pg.event.post(
            pg.event.Event(
                EditorEvents.BLOCK_SWITCH,
                self.code
            )
        )





