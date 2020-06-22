import pygame as pg
import json
from modules.block import *
from modules.textureset import TextureSet
from modules.leveljson import Map
from modules.entities import Player


class EditorLevel:
    def __init__(self, filepath: str):
        # loads the json file from the specified filepath
        with open(filepath) as f:
            data = json.load(open(filepath))

        self.enemies = EditorEnemies(data["enemies"])
        self.map = EditorMap(data["map"])
        starting_position = data["starting_position"]
        self.player = EditorPlayer(starting_position)

    def update(self, *args):
        pass

    def render(self, camera, surface):
        self.map.render(camera, surface)

        # renders the player image



class EditorMap(Map):
    """Essentially the same as the original Map, but Update() has been reworked to use different arguments"""
    def __init__(self, map_dict):
        super().__init__(map_dict)
        self.bg_array = map_dict["background"]
        self.decorations_array = map_dict["decorations"]
        self.terrain_array = map_dict["terrain"]

        self.bg_on = True
        self.decorations_on = True
        self.terrain_on = True

        # basically layer 0 is bg, layer 1 is decorations, and layer 2 is terrain array.
        # bg controls the bg terrain group, deco controls the mg terrain group, and terrain controls the
        # collideable and interactive terrain groups

    def update(self, *args):
        pass

    def render(self, camera, surface):
        if self.bg_on:
            for sprite in self.background_terrain_group:
                if camera.rect.colliderect(sprite.rect):
                    surface.blit(sprite.image,
                                 (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))

        if self.decorations_on:
            for sprite in self.middle_ground_terrain_group:
                if camera.rect.colliderect(sprite.rect):
                    surface.blit(sprite.image,
                                 (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))

        if self.terrain_on:
            for sprite in self.collideable_terrain_group:
                if camera.rect.colliderect(sprite.rect):
                    surface.blit(sprite.image,
                                 (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))

            for sprite in self.interactive_objects_group:
                if camera.rect.colliderect(sprite.rect):
                    surface.blit(sprite.image,
                                 (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))


class EditorEnemyManager:
    def __init__(self, enemies_list):
        self.enemies_list = enemies_list
        for enemy_dict in enemies_list:
            pass


class EditorPlayer:
    def __init__(self, coordinates):
        player = Player()
        self.image = player.image
        self.rect = player.rect
        self.blit_rect = player.blit_rect
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]

    def render(self, camera, surface):
        if camera.rect.colliderect(self.rect):
            surface.blit(self.image,
                         (self.rect.x - camera.rect.x, self.rect.y - camera.rect.y),
                         self.blit_rect)


class EditorEnemy:
    def __init__(self, type_object, coordinates):
        self.image = type_object

