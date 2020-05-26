import pygame as pg
from .block import Block

# Textures
grass_img = pg.image.load('assets/textures/grass.png')
dirt_img = pg.image.load('assets/textures/dirt.png')


# Loads game_map as a 2D array from a .txt file
def load_map(path: str) -> list:
    file = open(path, 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


# Reads a game map and adds Blocks accordingly to the Sprite Group
def make_terrain_group(map) -> pg.sprite.Group:
    terrain_group = pg.sprite.RenderPlain()
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == '1':
                terrain_group.add(Block(grass_img, x * Block.BLOCK_SIZE, y * Block.BLOCK_SIZE))
            elif map[y][x] == '2':
                terrain_group.add(Block(dirt_img, x * Block.BLOCK_SIZE, y * Block.BLOCK_SIZE))
    return terrain_group


# Returns the dimensions of the map as a tuple
def get_map_size(map) -> tuple:
    return len(map[0]) * Block.BLOCK_SIZE, len(map) * Block.BLOCK_SIZE


class Map:
    def __init__(self, map_path):
        game_map = load_map(map_path)
        self.terrain_group = make_terrain_group(game_map)
        self.dimensions = get_map_size(game_map)
        self.rect = pg.Rect((0, 0), self.dimensions)

    def is_within_map_boundaries(self, sprite: pg.sprite.Sprite) -> bool:
        return self.rect.colliderect(sprite.rect)