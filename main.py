import pygame as pg
from modules.block import Block
from modules.camera import Camera
from modules.player import Player
from modules.map import Map

pg.font.init()  # Initialize fonts


# TODO: Bound the player and the camera within the map


# ---------- FUNCTION DEFINITIONS ---------- #

# Moves player according to user's keyboard inputs
def handle_input(player, map):
    current_keys = pg.key.get_pressed()
    player.move(current_keys[pg.K_LEFT],
                current_keys[pg.K_RIGHT],
                current_keys[pg.K_SPACE],
                map)

# ---------- GLOBAL VARIABLES ---------- #

# Fonts
main_font = pg.font.SysFont("comicsans", 50)

# Textures
# grass_img = pg.image.load('assets/textures/grass.png')
# dirt_img = pg.image.load('assets/textures/dirt.png')

WINDOW_SIZE = (800, 600)
SURFACE_SIZE = (400, 300)

def main():
    # ---------- INITIALIZATION ---------- #

    pg.init()                                                   # Initialize pygame
    window = pg.display.set_mode(WINDOW_SIZE)                   # Initialize game window
    pg.display.set_caption("The Tower", "The Tower")            # Set window caption
    game_display = pg.Surface(SURFACE_SIZE)                     # Initialize surface for drawing

    game_map = Map('assets/maps/map2.txt')                      # Game Map (as 2D array)
    map_rect = pg.Rect((0, 0), game_map.dimensions)             # Initialize Rect representing entire map
    terrain_group = game_map.terrain_group                      # Initialize terrain sprite group

    camera = Camera(SURFACE_SIZE, game_map)                     # Initialize camera

    clock = pg.time.Clock()                                     # Initialize clock

    player = Player()                                           # Initialize player
    player_sprite_group = pg.sprite.GroupSingle(player)         # Initialize player sprite group

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
        handle_input(player, game_map)                                      # Process keyboard inputs
        camera.follow_target(player)                                        # Move camera to player's position
        camera.draw(game_display, terrain_group)                            # Draw terrain sprites on game display

        player.draw(game_display, camera)  # Draw player sprite on game display

        window.blit(pg.transform.scale(game_display, WINDOW_SIZE), (0, 0))  # Renders the display onto the window
        pg.display.update()                                                 # Updates the window
        clock.tick(60)                                                      # Limits the game to 60 fps

        # Player death
        if player.is_dead(game_map):
            main()

    pg.quit()   # Quit pygame after terminating main loop
    quit()      # Terminates python instance


main()
