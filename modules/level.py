import pygame as pg
from .block import *
from .entities import *
from .spritesheet import *

"""
* =============================================================== *
* This module contains all the necessary classes and functions    *
* required to make a level in the game.                           *
* =============================================================== *

HOW TO MAKE A NEW LEVEL
-------------------------
1.  Make a new LevelTemplate class that has the following public attributes:
        map: Map                    ->      Represents the Map to be loaded into the game
        enemies: EnemyManager       ->      Represents the enemies to be spawned in the game
        starting_position: tuple    ->      Starting position of the player in the form (x, y)
2.  Add your new LevelTemplate class to the level_template_list in the LevelManager class
    Do remember to place it in the exact order that you want the level to appear in

"""


class LevelManager:
    """Handles the changing of game levels"""
    def __init__(self):
        self.level_template_list = (Level1Template(),
                                    Level2Template())
        self.level = Level(self.level_template_list[0])
        self.level.level_manager = self
        self.current_index = 0

    def load_next_level(self, player, camera):
        """Loads the next level in the list"""
        self.current_index += 1
        if self.current_index < len(self.level_template_list):
            level_template = self.level_template_list[self.current_index]
            self.level = Level(level_template)
            self.level.level_manager = self

            # Move the player to the correct position
            player.rect.x = level_template.starting_position[0]
            player.rect.y = level_template.starting_position[1]

            # TODO: Shove this outside since this kinda violates single responsibility
            # TODO: or make this function handle fadein fadeouts too
            camera.snap_to_target(player)

    def fade_in(self, surface):
        pass


# --- By right this shit should be stored in a JSON --- #
class Level1Template:
    def __init__(self):
        self.map = Map("assets/maps/map3.txt")
        self.enemies = EnemyManager()
        # self.enemies.add_enemy((700, 100, 50),
        #                        (500, 100, 30))
        self.starting_position = (100, 200)


class Level2Template:
    def __init__(self):
        self.map = Map("assets/maps/map2.txt")
        self.enemies = EnemyManager()
        self.enemies.add_enemy((700, 100, 50),
                               (500, 100, 30))
        self.starting_position = (100, 200)


class Level:
    def __init__(self, level_template):
        # map should contain the dimensions, the terrain group of sprites, and the list of sprites. (is rect necessary)
        self.map = level_template.map
        # TODO: make enemymanager retrieve enemies from a json file
        self.enemies = level_template.enemies
        # make a background manager to manage multiple backgrounds at once. set static scrolling speeds.
        self.background = None

        self.level_manager = None

        # textures should be loaded from a singleton.

    def update(self, player):
        self.enemies.update(self.map, player)
        self.map.update(player, self)

    def render(self, camera, surface):
        self.map.render(camera, surface)
        self.enemies.render(camera, surface)


class Map:
    """
    In-game representation of the specified map
    Handles the updating and rendering of the terrain blocks
    """
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
        self.falling_group = pg.sprite.Group()
        self.gateway_group = pg.sprite.GroupSingle()
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
                        self.coin_group.add(new_coin)

                    elif tile_position_str == "e":
                        new_gateway = GatewayBlock(self.textureset.get_texture_from_code(tile_position_str),
                                                   x * Block.BLOCK_SIZE,
                                                   y * Block.BLOCK_SIZE)
                        self.gateway_group.add(new_gateway)

                    elif tile_position_str == "f":
                        new_falling_block = FallingBlock(self.textureset.get_texture_from_code(tile_position_str),
                                                   x * Block.BLOCK_SIZE,
                                                   y * Block.BLOCK_SIZE)
                        self.terrain_group.add(new_falling_block)
                        self.falling_group.add(new_falling_block)

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
        self.gateway_group.update(player)
        self.falling_group.update(player)

    def render(self, camera, surface):
        for sprite in self.terrain_group:
            if camera.rect.colliderect(sprite.rect):
                surface.blit(sprite.image, (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))

        for sprite in self.coin_group:
            if camera.rect.colliderect(sprite.rect):
                surface.blit(sprite.image, (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))

        for sprite in self.gateway_group:
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
            if entity.state == EntityState.DEAD:
                entity.kill()
                self.sprite_list = self.sprite_group.sprites()
            else:
                entity.update(map, player)

    def render(self, camera, surface):
        for entity in self.sprite_list:
            entity.render(camera, surface)
