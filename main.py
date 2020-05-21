import pygame as pg

# TODO: Currently character gets stuck due to a fucked up collision handling.

# TODO: Camera structure
# Since the map can be structured as a rect, and the player is a rect also,
# make the camera class to follow the player around and only draw stuff in the rect.
# possibly using collision. Block detection in a rect is possible.

# Load Textures
grass_img = pg.image.load('assets/textures/grass.png')
dirt_img = pg.image.load('assets/textures/dirt.png')

# ---------- FUNCTION DECLARATIONS ---------- #
def load_map(path: str):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


def handle_input(player, terrain):
    current_keys = pg.key.get_pressed()
    player.move(current_keys[pg.K_UP],
              current_keys[pg.K_DOWN],
              current_keys[pg.K_LEFT],
              current_keys[pg.K_RIGHT],
              terrain
              )


def add_blocks_to_group(group: pg.sprite.Group, map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == '1':
                group.add(Block(grass_img, x * 20, y * 20))


def get_colliding_sides(sprite: pg.sprite.Sprite, group: pg.sprite.Group):
    # This gets the colliding sides.
    top, bottom, left, right = False, False, False, False
    for colliding_sprite in pg.sprite.spritecollide(sprite, group, False):
        if colliding_sprite.rect.top < sprite.rect.top < colliding_sprite.rect.bottom:
            top = True
        if colliding_sprite.rect.top < sprite.rect.bottom < colliding_sprite.rect.bottom:
            bottom = True
        if colliding_sprite.rect.left < sprite.rect.left < colliding_sprite.rect.right:
            left = True
        if colliding_sprite.rect.left < sprite.rect.right < colliding_sprite.rect.right:
            right = True
    return top, bottom, left, right


def enforce_collision_x(sprite: pg.sprite.Sprite, group: pg.sprite.Group):
    # applied after a movement to make sure that the sprite does not clip
    # This method is a bit inefficient though
    # Checks each axis individually
    for colliding_sprite in pg.sprite.spritecollide(sprite, group, False):
        if colliding_sprite.rect.left < sprite.rect.left < colliding_sprite.rect.right:
            sprite.rect.left = colliding_sprite.rect.right
        if colliding_sprite.rect.left < sprite.rect.right < colliding_sprite.rect.right:
            sprite.rect.right = colliding_sprite.rect.left


def enforce_collision_y(sprite: pg.sprite.Sprite, group: pg.sprite.Group):
    for colliding_sprite in pg.sprite.spritecollide(sprite, group, False):
        if colliding_sprite.rect.top < sprite.rect.top < colliding_sprite.rect.bottom:
            sprite.rect.top = colliding_sprite.rect.bottom
        if colliding_sprite.rect.top < sprite.rect.bottom < colliding_sprite.rect.bottom:
            sprite.rect.bottom = colliding_sprite.rect.top



# ---------- CLASS DECLARATIONS ---------- #
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite = pg.image.load('assets/sprites/player.png').convert()
        self.image = pg.transform.scale(self.sprite, (20, 40))
        self.image.set_colorkey((255, 255, 255))

        self.rect = pg.Rect(0, 0, 20, 40)

        self.velocity = 1

    def move(self, up: bool, down: bool, left: bool, right: bool, terrain):
        # moves the player first, then check for collision. if collided, make them such that they are touching.
        if up:
            self.rect.y -= self.velocity
        if down:
            self.rect.y += self.velocity
        enforce_collision_y(self, terrain)
        if left:
            self.rect.x -= self.velocity
        if right:
            self.rect.x += self.velocity
        enforce_collision_x(self, terrain)


    def draw(self, surface: pg.Surface):
        """Draws the player on the specified surface"""
        surface.blit(self.image, (self.rect.x, self.rect.y))




class Block(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pg.transform.scale(image.convert(), (20, 20))
        self.rect = pg.Rect(x, y , 20, 20)


# ---------- GLOBAL VARIABLES ---------- #

WINDOW_SIZE = (800, 600)
SURFACE_SIZE = (400, 300)


# ---------- ACTUAL GAME STARTS HERE ---------- #

# Initialise pygame
pg.init()

# Programme name
pg.display.set_caption("The Tower", "The Tower")

# Initialise game window
window = pg.display.set_mode(WINDOW_SIZE)

# Initialise surface for drawing, which is scaled
game_display = pg.Surface(SURFACE_SIZE)

# Loads the game map as a 2D array
game_map = load_map('map2')

# Adds the blocks to a sprite group
terrain_group = pg.sprite.RenderPlain()
add_blocks_to_group(terrain_group, game_map)



# Starts the clock to limit to 60fps
clock = pg.time.Clock()

# Initialise characters
player = Player()
player_sprite_group = pg.sprite.GroupSingle(player)


## ideas for camera
## initialise the map as a big rect, then make the camera follow the character

# ---------- MAIN LOOP ----------
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # Fills the game display with a color
    game_display.fill((146, 255, 255))

    # Draws the map
    terrain_group.draw(game_display)

    # Process keyboard inputs
    handle_input(player, terrain_group)

    # Render the player character
    player.draw(game_display)

    # Renders the display onto the window
    window.blit(pg.transform.scale(game_display, WINDOW_SIZE), (0, 0))

    # Updates the window
    pg.display.update()

    # Limits the game to 60 fps
    clock.tick(60)

# Quit pygame after terminating main loop
pg.quit()

# Terminates python instance
quit()
