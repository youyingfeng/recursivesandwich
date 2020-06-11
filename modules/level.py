import pygame as pg
from .block import *
from .components import *
from .player import *
from .spritesheet import *


# =============================================================== #
# This file contains all high-level classes and methods required  #
# in an ordinary game level.                                      #
# =============================================================== #


# TODO: Shove this into a new class Tileset with a dict

# Original tiles
grass_img = pg.image.load('assets/textures/grass.png')
dirt_img = pg.image.load('assets/textures/dirt.png')


# Dungeon spritesheet
dungeon = Spritesheet("assets/textures/Dungeon/dungeon_spritesheet.png", 14, 23)


class LevelManager:
    def __init__(self, level):
        self.level = level
        self.level.manager = self

    def switch_to_level(self, level):
        self.level = level
        self.level.manager = self


class Level:
    def __init__(self):
        # map should contain the dimensions, the terrain group of sprites, and the list of sprites. (is rect necessary)
        self.map = Map("assets/maps/map3.txt")
        # TODO: make enemymanager retrieve enemies from a json file
        self.enemies = EnemyManager()
        self.enemies.add_enemy((700, 100, 50), (500, 100, 30))
        # make a background manager to manage multiple backgrounds at once. set static scrolling speeds.
        self.background = None

        self.manager = None

        # textures should be loaded from a singleton.

    def update(self, player):
        self.enemies.update(self.map, player)
        self.map.update(player)

    def render(self, camera, surface):
        self.map.render(camera, surface)
        self.enemies.render(camera, surface)


class Map:
    def __init__(self, map_path):
        self.textureset = TextureSet()
        # -------------------- PREPROCESSING --------------------#
        file = open(map_path, 'r')
        data = file.read()
        file.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))

        # -------------------- DECLARATIONS -------------------- #
        self.terrain_group = pg.sprite.RenderPlain()
        self.hazardous_terrain_group = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        # Add blocks into the terrain group according to the map
        for y in range(len(game_map)):
            for x in range(len(game_map[0])):

                # Refers to the position of the tile on the tileset
                # 'x' represents empty space in the map
                tile_position_str = game_map[y][x]
                if tile_position_str != "x":
                    if tile_position_str == "s":
                        new_block = HazardousBlock(self.textureset.get_texture_from_code(tile_position_str),
                                                   x * Block.BLOCK_SIZE,
                                                   y * Block.BLOCK_SIZE)
                        self.terrain_group.add(new_block)
                        self.hazardous_terrain_group.add(new_block)

                    elif tile_position_str == "c":
                        new_coin = Coin(self.textureset.get_texture_from_code(tile_position_str),
                                                   x * Block.BLOCK_SIZE,
                                                   y * Block.BLOCK_SIZE)
                        self.terrain_group.add(new_coin)
                        self.coin_group.add(new_coin)

                    else:
                        self.terrain_group.add(Block(self.textureset.get_texture_from_code(tile_position_str),
                                                     x * Block.BLOCK_SIZE,
                                                     y * Block.BLOCK_SIZE))

        # Stores the dimensions of the map, assuming it is a perfect rectangle
        self.dimensions = (len(game_map[0]) * Block.BLOCK_SIZE, len(game_map) * Block.BLOCK_SIZE)
        self.rect = pg.Rect((0,0), self.dimensions)

    def update(self, player, *args):
        self.hazardous_terrain_group.update(player)
        self.coin_group.update(player)

    def render(self, camera, surface):
        for sprite in self.terrain_group:
            if camera.rect.colliderect(sprite.rect):
                surface.blit(sprite.image, (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))


class EnemyManager:
    def __init__(self):
        self.sprite_group = pg.sprite.Group()
        self.sprite_list = self.sprite_group.sprites()

        # SINGLETONS TO BE PASSED
        self.type_object = EnemyType()
        self.ai = EnemyAIInputComponent()
        self.physics = PhysicsComponent()
        self.renderer = RenderComponent()

    def add_enemy(self, *coordinates):
        # creates a new sprite and adds to the group
        for coords in coordinates:
            self.sprite_group.add(Enemy(self.type_object,
                                        self.ai,
                                        self.physics,
                                        self.renderer,
                                        coords))
            self.sprite_list = self.sprite_group.sprites()

    def update(self, map, player):
        for entity in self.sprite_list:
            if entity.state == PlayerState.DEAD:
                entity.kill()
                self.sprite_list = self.sprite_group.sprites()
            else:
                entity.update(map, player)

    def render(self, camera, surface):
        for entity in self.sprite_list:
            entity.render(camera, surface)


