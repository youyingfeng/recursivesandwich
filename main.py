import pygame as pg
from modules.block import Block
from modules.camera import Camera
from modules.player import Player


# ---------- FUNCTION DEFINITIONS ---------- #

# Loads the game map as a 2D array from a .txt file
def load_map(path: str):
    file = open(path, 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


# Moves player according to user's keyboard inputs
def handle_input(player, terrain):
    current_keys = pg.key.get_pressed()
    player.move(current_keys[pg.K_LEFT],
                current_keys[pg.K_RIGHT],
                current_keys[pg.K_SPACE],
                terrain)


# Reads a game map and adds Blocks accordingly to the Sprite Group
def add_blocks_to_group(group: pg.sprite.Group, map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == '1':
                group.add(Block(grass_img, x * Block.BLOCK_SIZE, y * Block.BLOCK_SIZE))
            elif map[y][x] == '2':
                group.add(Block(dirt_img, x * Block.BLOCK_SIZE, y * Block.BLOCK_SIZE))


# ---------- GLOBAL VARIABLES ---------- #

# Textures
grass_img = pg.image.load('assets/textures/grass.png')
dirt_img = pg.image.load('assets/textures/dirt.png')

# Game Map (as 2D array)
game_map = load_map('assets/maps/map2.txt')

WINDOW_SIZE = (800, 600)
SURFACE_SIZE = Camera.SURFACE_SIZE


# ---------- INITIALIZATION ---------- #

pg.init()                                                   # Initialize pygame
window = pg.display.set_mode(WINDOW_SIZE)                   # Initialize game window
pg.display.set_caption("The Tower", "The Tower")            # Set window caption
game_display = pg.Surface(SURFACE_SIZE)                     # Initialize surface for drawing
map_rect = pg.Rect(0, 0, len(game_map[0]), len(game_map))   # Initialize Rect representing entire map
camera = Camera()                                           # Initialize camera
clock = pg.time.Clock()                                     # Initialize clock

player = Player()                                           # Initialize player
player_sprite_group = pg.sprite.GroupSingle(player)         # Initialize player sprite group

terrain_group = pg.sprite.Group()                           # Initialize terrain sprite group
add_blocks_to_group(terrain_group, game_map)

all_sprites_group = pg.sprite.Group()                       # Initialize all sprites group
all_sprites_group.add(player)
all_sprites_group.add(terrain_group.sprites())


# ---------- MAIN GAME LOOP ---------- #

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    game_display.fill((146, 255, 255))                                  # Fill game display with light-blue color
    handle_input(player, terrain_group)                                 # Process keyboard inputs
    camera.update(player)                                               # Move camera to player's position
    camera.draw(game_display, all_sprites_group)                        # Draw all sprites on game display
    window.blit(pg.transform.scale(game_display, WINDOW_SIZE), (0, 0))  # Renders the display onto the window
    pg.display.update()                                                 # Updates the window
    clock.tick(60)                                                      # Limits the game to 60 fps

pg.quit()   # Quit pygame after terminating main loop
quit()      # Terminates python instance
