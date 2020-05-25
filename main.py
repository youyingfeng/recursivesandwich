import pygame as pg

from modules.camera import Camera
from modules.player import Player
from modules.map import Map
from modules.animations import StaticBackground, ParallaxBackground
from modules.scenemanager import Scene, SceneManager
from modules.gamescene import GameScene


# ---------- GLOBAL VARIABLES ---------- #
WINDOW_SIZE = (800, 600)


# ---------- MAIN FUNCTION ---------- #
def main():
    # ---------- INITIALIZATION ---------- #
    pg.init()                                                   # Initialize pygame

    pg.font.init()  # Initialize fonts
    # Fonts
    main_font = pg.font.SysFont("comicsans", 50)

    window = pg.display.set_mode(WINDOW_SIZE)                   # Initialize game window
    pg.display.set_caption("The Tower", "The Tower")            # Set window caption

    clock = pg.time.Clock()                                     # Initialize clock

    manager = SceneManager(GameScene())                         # Initialise scene manager

    run = True

    # ---------- MAIN GAME LOOP ---------- #
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        manager.scene.handle_events()
        manager.scene.update()
        manager.scene.render(window)

        pg.display.update()                                                 # Updates the window
        clock.tick(60)                                                      # Limits the game to 60 fps

    # ---------- TERMINATION ---------- #
    pg.quit()   # Quit pygame after terminating main loop
    quit()      # Terminates python instance


main()
