import pygame as pg

# Initialise pygame
pg.init()

# Programme name
pg.display.set_caption("The Tower", "The Tower")

# Initialise game window
window = pg.display.set_mode((800, 600))

# Initialise surface for drawing
display = pg.Surface((400, 300))


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

# TODO: split classes into individual files

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Override
        self.image = pg.Surface([50, 50])
        self.image.fill([255, 0, 0])

        self.rect = pg.Rect(-25, -25, 25, 25)


class Block(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()


# Camera function to enable the camera to follow player
class Camera(object):
    def __init__(self, camera_func, level_width, level_height):
        self.camera_func = camera_func
        self.state = pg.Rect(0, 0, level_width, level_height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect  # l = left,  t = top
    _, _, w, h = camera  # w = width, h = height
    return pg.Rect(-l + 400, -t + 300, w, h)

game_map = load_map('map')

all_sprites_list = pg.sprite.Group()

# Initialises player
player = Player()
all_sprites_list.add(player)

# Initialise clock
clock = pg.time.Clock()

# Initialise camera
camera = Camera(simple_camera, 1920, 1080)

grass_img = pg.image.load('grass.png')
dirt_img = pg.image.load('dirt.png')

# ---------- Main loop ----------
run = True
while run:
    # clear screen by filling it with blue
    display.fill((146, 244, 255))

    # process the input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # Get keys pressed
    current_keys = pg.key.get_pressed()

    # TODO: refactor to allow custom controls
    if current_keys[pg.K_LEFT]:
        player.rect.x -= 5
    if current_keys[pg.K_RIGHT]:
        player.rect.x += 5
    if current_keys[pg.K_UP]:
        player.rect.y -= 5
    if current_keys[pg.K_DOWN]:
        player.rect.y += 5

    # update the game by one step

    # renders the map
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img, (x * 16 + camera.state.x, y * 16 + camera.state.y))
            if tile == '2':
                display.blit(grass_img, (x * 16 + camera.state.x, y * 16 + camera.state.y))
            if tile != '0':
                tile_rects.append(pg.Rect(x * 16 + camera.state.x, y * 16 + camera.state.y, 16, 16))
            x += 1
        y += 1

    # render the changes
    camera.update(player)

    window.fill([0, 0, 0])
    # all_sprites_list.draw(window)



    window.blit(pg.transform.scale(display, (800, 600)), (0, 0))
    for sprite in all_sprites_list:
        window.blit(sprite.image, camera.apply(sprite))
    pg.display.update()

    # Limit to 60 fps
    clock.tick(60)

# Quit pygame after terminating main loop
pg.quit()

# Terminates python instance
quit()
