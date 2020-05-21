import pygame as pg


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

    # Draws the player on the specified surface
    def draw(self, surface: pg.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    """ Collision methods applied after a movement to make sure that the sprite does not clip.
    Methods are a bit inefficient - checks each axis individually """

    def enforce_collision_x(sprite: pg.sprite.Sprite, group: pg.sprite.Group):
        for colliding_sprite in pg.sprite.spritecollide(sprite, group, False):
            if colliding_sprite.rect.left < sprite.rect.left < colliding_sprite.rect.right:
                sprite.rect.left = colliding_sprite.rect.right
            if colliding_sprite.rect.left < sprite.rect.right < colliding_sprite.rect.right:
                sprite.rect.right = colliding_sprite.rect.left

    def enforce_collision_y(sprite: pg.sprite.Sprite, group: pg.sprite.Group):
        all_colliding_sprites = pg.sprite.spritecollide(sprite, group, False)
        for colliding_sprite in all_colliding_sprites:
            if colliding_sprite.rect.top < sprite.rect.top < colliding_sprite.rect.bottom:
                sprite.rect.top = colliding_sprite.rect.bottom
            if colliding_sprite.rect.top < sprite.rect.bottom < colliding_sprite.rect.bottom:
                sprite.rect.bottom = colliding_sprite.rect.top
        return len(all_colliding_sprites) > 0