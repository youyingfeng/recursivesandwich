import pygame as pg
from .animations import Spritesheet, Animation


MAX_HEALTH = 100


# TODO: Rewrite the entire player class to inherit from an unimplemented entity class
# Use PEP526 variable annotations to indicate uninitialised variables?
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.spritesheet = Spritesheet("assets/sprites/Idle (32x32).png", 1, 11)
        self.animation = Animation(self.spritesheet.get_images_at(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

        self.image = self.animation.get_current_frame()

        self.rect = pg.Rect(10, 10, 21, 27)         # Change the dimensions of this rect to match sprite and hitbox
        self.xvelocity = 3
        self.yvelocity = 5
        self.gravity = 1  # keep small as it updates every tick
        self.isJumping = False
        self.health = 100 # maximum 100

    # To be called in the camera.draw() method only
    def draw(self, surface: pg.Surface, camera):
        # updates the current frame of the animation
        frame_changed = self.animation.update_image()
        if frame_changed:
            self.image = self.animation.get_current_frame()

        surface.blit(self.image,
                     (self.rect.x - camera.rect.x, self.rect.y - camera.rect.y),
                     pg.Rect(6, 5, 21, 27))     # change the dimensions of this rect if the sprite changes
        self.draw_healthbar(surface, camera)

    def draw_healthbar(self, surface: pg.Surface, camera):
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
    def move(self, left: bool, right: bool, jump: bool, map):
        if self.isJumping:  # block further jump inputs but allow left and right
            self.yvelocity += self.gravity
            self.rect.y += self.yvelocity
            landed = self.enforce_collision_y(map.terrain_group)

            if landed:
                self.isJumping = False
                self.yvelocity = 5
            if left:
                self.rect.x -= self.xvelocity
            if right:
                self.rect.x += self.xvelocity
            self.enforce_collision_x(map.terrain_group)

        else:
            if jump:
                self.yvelocity = -10
                self.isJumping = True

            self.rect.y += self.yvelocity
            self.enforce_collision_y(map.terrain_group)

            if left:
                self.rect.x -= self.xvelocity
            if right:
                self.rect.x += self.xvelocity
            self.enforce_collision_x(map.terrain_group)

        self.enforce_boundaries(map)

    # TODO: Incorporate enforce_boundaries logic into enforce_collision to make boundaries function irrelevant
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

    def enforce_boundaries(self, map):
        if self.rect.top < 0:
            self.rect.top = 0
        # elif self.rect.bottom > map.rect.bottom:
        #     self.rect.bottom = map.rect.bottom
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > map.rect.right:
            self.rect.right = map.rect.right

    # Checks if player is dead
    def is_dead(self, map):
        # Collects all possibilities in which a player can lose a life
        return self.rect.bottom > map.rect.bottom or self.health < 0
