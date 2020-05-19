import pygame as pg
# TODO: split classes into individual files

class Player:


# Initialise window settings
pg.display.set_caption("The Tower", "The Tower")

# Main surface
pg.display.set_mode((800, 600))

# Main loop
run = True
while run:
    # process the input
    pg.time.delay(100)

    # update the game by one step
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # render the changes

# Quit pygame after terminating main loop
pg.quit()

# Terminates python instance
quit()