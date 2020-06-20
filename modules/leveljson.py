import pygame as pg
import json

from modules.block import *
from modules.entities import EnemyType, Enemy
from modules.components import *
from modules.spritesheet import *

"""
* =============================================================== *
* This module contains all the necessary classes and functions    *
* required to make a level in the game.                           *
* =============================================================== *

HOW TO MAKE A NEW LEVEL
-------------------------
1.  Make a new JSON file according to the template given. Number the levels sequentially.
    JSON files must contain the following fields:
        enemies             ->          JSON array containing one dict for each enemy placed
        map                 ->          JSON object (python dict) containing 3 map layers, each represented by  
                                        a 2-dimensional array
        starting_position   ->          JSON array containing the starting position of the player
        
    Refer to the following link for the conversion tables between JSON and Python objects:
            https://docs.python.org/3/library/json.html#py-to-json-table
    
2.  Update the number_of_levels attribute in LevelManager to reflect the current amount of levels in the game.

"""


class LevelManager:
    def __init__(self):
        self.level = Level("assets/levels/level1.json")
        self.current_level = 1
        self.number_of_levels = 1

    def load_next_level(self, player, camera):
        self.current_level += 1
        if self.current_level > self.number_of_levels:
            pg.event.post(
                pg.event.Event(
                    GameEvent.GAME_COMPLETE.value
                )
            )
            return

        self.level = Level("assets/levels/level" + str(self.current_level) + ".json")
        player.rect.x = self.level.starting_position[0]
        player.rect.y = self.level.starting_position[1]
        camera.snap_to_target(player)



class Level:
    def __init__(self, filepath: str):
        # loads the json file from the specified filepath
        with open(filepath) as f:
            data = json.load(open(filepath))

        self.enemies = EnemyManager(data["enemies"])
        self.map = Map(data["map"])
        self.starting_position = data["starting_position"]

    def update(self, player):
        # TODO: rework update for map to send events instead
        self.enemies.update(self.map, player)
        self.map.update(player)

    def render(self, camera, surface):
        self.map.render(camera, surface)
        self.enemies.render(camera, surface)


class Map:
    def __init__(self, map_dict):
        # takes in the entire dict and parses it accordingly
        self.background_terrain_group = pg.sprite.Group()       # backmost layer
        self.middle_ground_terrain_group = pg.sprite.Group()    # middle layer
        self.collideable_terrain_group = pg.sprite.Group()      # front layer
        self.interactive_objects_group = pg.sprite.Group()      # front layer

        texture_set = TextureSet()

        background_layer = map_dict["background"]
        for y in range(len(background_layer)):
            for x in range(len(background_layer[0])):
                code = background_layer[y][x]

                if code != "  ":
                    if code == "1w" or code == "2w":
                        self.middle_ground_terrain_group.add(Block(texture_set.get_texture_from_code(code),
                                                                   x * Block.BLOCK_SIZE,
                                                                   y * Block.BLOCK_SIZE))
                    else:
                        self.background_terrain_group.add(Block(texture_set.get_texture_from_code(code),
                                                                x * Block.BLOCK_SIZE,
                                                                y * Block.BLOCK_SIZE))

        decorations_layer = map_dict["decorations"]
        for y in range(len(decorations_layer)):
            for x in range(len(decorations_layer[0])):
                code = decorations_layer[y][x]

                if code != "  ":
                    self.middle_ground_terrain_group.add(Block(texture_set.get_texture_from_code(code),
                                                               x * Block.BLOCK_SIZE,
                                                               y * Block.BLOCK_SIZE))

        terrain_layer = map_dict["terrain"]
        for y in range(len(terrain_layer)):
            for x in range(len(terrain_layer[0])):
                code = terrain_layer[y][x]

                # I'm leaving out cloudy boi as it really does not fit the game
                if code != "  ":
                    if code == "FB":
                        new_block = PushableBlock(texture_set.get_texture_from_code(code),
                                                  x * Block.BLOCK_SIZE,
                                                  y * Block.BLOCK_SIZE)
                        self.interactive_objects_group.add(new_block)
                        self.collideable_terrain_group.add(new_block)
                    elif code == "LB":
                        self.interactive_objects_group.add(LadderBlock(texture_set.get_texture_from_code(code),
                                                                       x * Block.BLOCK_SIZE,
                                                                       y * Block.BLOCK_SIZE)
                                                           )
                    elif code == "PB":
                        new_block = PushableBlock(texture_set.get_texture_from_code(code),
                                                  x * Block.BLOCK_SIZE,
                                                  y * Block.BLOCK_SIZE)
                        self.interactive_objects_group.add(new_block)
                        self.collideable_terrain_group.add(new_block)
                    elif code == "SP":
                        self.interactive_objects_group.add(SpikeBlock(texture_set.get_texture_from_code(code),
                                                                      x * Block.BLOCK_SIZE,
                                                                      y * Block.BLOCK_SIZE)
                                                           )
                    elif code == "GW":
                        self.interactive_objects_group.add(GatewayBlock(texture_set.get_texture_from_code(code),
                                                                        x * Block.BLOCK_SIZE,
                                                                        y * Block.BLOCK_SIZE)
                                                           )
                    elif code == "CN":
                        self.interactive_objects_group.add(Coin(texture_set.get_texture_from_code(code),
                                                                x * Block.BLOCK_SIZE,
                                                                y * Block.BLOCK_SIZE)
                                                           )
                    else:
                        self.collideable_terrain_group.add(Block(texture_set.get_texture_from_code(code),
                                                                 x * Block.BLOCK_SIZE,
                                                                 y * Block.BLOCK_SIZE)
                                                           )

        self.rect = pg.Rect(0,
                            0,
                            len(terrain_layer[0]) * Block.BLOCK_SIZE,
                            len(terrain_layer) * Block.BLOCK_SIZE)

    def update(self, player):
        self.interactive_objects_group.update(player)

    def render(self, camera, surface):
        for sprite in self.background_terrain_group:
            if camera.rect.colliderect(sprite.rect):
                surface.blit(sprite.image, (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))

        for sprite in self.middle_ground_terrain_group:
            if camera.rect.colliderect(sprite.rect):
                surface.blit(sprite.image, (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))

        for sprite in self.collideable_terrain_group:
            if camera.rect.colliderect(sprite.rect):
                surface.blit(sprite.image, (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))

        for sprite in self.interactive_objects_group:
            if camera.rect.colliderect(sprite.rect):
                surface.blit(sprite.image, (sprite.blit_rect.x - camera.rect.x, sprite.blit_rect.y - camera.rect.y))


class EnemyManager:
    def __init__(self, enemies_list: list):
        self.enemies = pg.sprite.Group()
        self.enemies_list = self.enemies.sprites()

        # takes in a list of dictionaries representing enemies
        self.enemy_type = {"Pink Guy": EnemyType()
                           }
        self.ai = EnemyAIInputComponent()
        self.physics = PhysicsComponent()
        self.renderer = RenderComponent()

        for enemy_dict in enemies_list:
            self.enemies.add(Enemy(self.enemy_type[enemy_dict["type"]],
                                   self.ai,
                                   self.physics,
                                   self.renderer,
                                   enemy_dict["coordinates"],
                                   50)
                             )
            print("kappa")

        self.enemies_list = self.enemies.sprites()

    def update(self, map, player):
        for entity in self.enemies_list:
            if entity.state == EntityState.DEAD:
                entity.kill()
                self.enemies_list = self.enemies.sprites()
            else:
                entity.update(map, player)

    def render(self, camera, surface):
        for entity in self.enemies_list:
            entity.render(camera, surface)


