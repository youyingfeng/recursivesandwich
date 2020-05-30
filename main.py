import pygame as pg
from modules.gamescene import Scene, SceneManager, TitleScene


WINDOW_SIZE = (800, 600)


def main():

    pg.mixer.pre_init(44100, 16, 2, 512)
    # Initialize pygame
    pg.init()

    # Initialize window
    window = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("The Tower", "The Tower")

    # Initialize clock
    clock = pg.time.Clock()

    # Game loop runs when this is true
    run = True

    # Initialise scene manager with TitleScene
    manager = SceneManager(TitleScene())

    # Game loop
    while run:
        # TODO: probably should shove this inside handle_events()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        manager.scene.handle_events()
        manager.scene.update()
        manager.scene.render(window)

        # Updates the window
        pg.display.update()

        # Limits the game to 60 fps
        clock.tick(60)

    # Quit pygame
    pg.quit()

    # Quit program
    quit()


main()