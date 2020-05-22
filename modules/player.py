import pygame as pg
from modules.camera import Camera


# Global player attributes
MAX_HEALTH = 100

# Player images
player_img = pg.image.load('assets/sprites/player.png')


class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.sprite = player_img.convert()
        self.image = pg.transform.scale(self.sprite, (20, 40))
        self.image.set_colorkey((255, 255, 255))
        self.rect = pg.Rect(0, 0, 20, 40)
        self.xvelocity = 3
        self.yvelocity = 5
        self.gravity = 1.3  # keep small as it updates every tick
        self.isJumping = False
        self.health = 100 # maximum 100

    # To be called in the camera.draw() method only
    def draw(self, surface: pg.Surface, camera):
        surface.blit(self.image, (self.rect.x - camera.rect.x, self.rect.y - camera.rect.y))
        self.healthbar(surface, camera)

    def healthbar(self, surface: pg.Surface, camera):
        SCALE = 2
        X_OFFSET = 10
        Y_OFFSET = 20
        THICKNESS = 5
        pg.draw.rect(surface,
                     (255, 0, 0), # red
                     (self.rect.x - camera.rect.x - X_OFFSET,
                      self.rect.y - camera.rect.y - Y_OFFSET,
                      self.image.get_width() * SCALE,
                      THICKNESS))
        pg.draw.rect(surface,
                     (0, 255, 0), # green
                     (self.rect.x - camera.rect.x - X_OFFSET,
                      self.rect.y - camera.rect.y - Y_OFFSET,
                      self.image.get_width() * (self.health / MAX_HEALTH) * SCALE,
                      THICKNESS))

    # Moves the player first, then if collided with terrain, enforces collision
    def move(self, left: bool, right: bool, jump: bool, terrain):
        if self.isJumping:  # block further jump inputs but allow left and right
            self.yvelocity += self.gravity
            self.rect.y += self.yvelocity
            landed = self.enforce_collision_y(terrain)

            if landed:
                self.isJumping = False
                self.yvelocity = 5
            if left:
                self.rect.x -= self.xvelocity
            if right:
                self.rect.x += self.xvelocity
            self.enforce_collision_x(terrain)

        else:
            if jump:
                self.yvelocity = -10
                self.isJumping = True

            self.rect.y += self.yvelocity
            self.enforce_collision_y(terrain)

            if left:
                self.rect.x -= self.xvelocity
            if right:
                self.rect.x += self.xvelocity
            self.enforce_collision_x(terrain)

    # Collisions
    def enforce_collision_x(self, group: pg.sprite.Group):
        # Collision methods applied after a movement to make sure that the sprite does not clip.
        # Methods are a bit inefficient - checks each axis individually.
        for colliding_sprite in pg.sprite.spritecollide(self, group, False):
            if colliding_sprite.rect.left < self.rect.left < colliding_sprite.rect.right:
                self.rect.left = colliding_sprite.rect.right
            if colliding_sprite.rect.left < self.rect.right < colliding_sprite.rect.right:
                self.rect.right = colliding_sprite.rect.left

    def enforce_collision_y(self, group: pg.sprite.Group):
        all_colliding_sprites = pg.sprite.spritecollide(self, group, False)
        for colliding_sprite in all_colliding_sprites:
            if colliding_sprite.rect.top < self.rect.top < colliding_sprite.rect.bottom:
                self.rect.top = colliding_sprite.rect.bottom
            if colliding_sprite.rect.top < self.rect.bottom < colliding_sprite.rect.bottom:
                self.rect.bottom = colliding_sprite.rect.top
        return len(all_colliding_sprites) > 0

    # Checks if player is dead
    def is_dead(self):
        # Collects all possibilities in which a player can lose a life
        return self.rect.bottom > Camera.SURFACE_SIZE[0] or self.health < 0
