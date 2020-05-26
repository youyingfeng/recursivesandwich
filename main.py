import pygame as pg
from modules.gamescene import Scene, SceneManager, TitleScene


WINDOW_SIZE = (800, 600)


def main():

    # Initialize pygame
    pg.init()

    # Initialize window
    window = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("The Tower", "The Tower")

    # Initialize clock
    clock = pg.time.Clock()

    run = True

    # Initialise scene manager with TitleScene
    manager = SceneManager(TitleScene())

    # Main game loop
    while run:
        # TODO: probably should shove this inside handle_events()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        manager.scene.handle_events()
        manager.scene.update()
        manager.scene.render(window)

        pg.display.update()	# Updates the window
        clock.tick(60)		# Limits the game to 60 fps

    pg.quit()
    quit()


main()