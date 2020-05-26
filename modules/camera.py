import pygame as pg


# TODO: Camera structure
# Since the map can be structured as a rect, and the player is a rect also,
# make the camera class to follow the player around and only draw stuff in the rect.
# possibly using collision. Block detection in a rect is possible.
# IDEA: Initialise the map as a big rect, then make the camera follow the character


class Camera:
    def __init__(self, camera_size, map):
        self.boundaries = map.rect

        # rudimentary clamping only on the x-axis, since y-axis clamping seems unnecessary
        if self.boundaries.right < camera_size[0]:
            temp = camera_size
            camera_size = (self.boundaries.right, int(temp[1] * self.boundaries.right / temp[0]))
        self.camera_size = camera_size
        self.rect = pg.Rect((0, 0), camera_size)

        # TODO: clamp camera to map bounds, this is buggy

    # Moves this camera's position to the target's position
    def follow_target(self, target: pg.sprite.Sprite):
        lerp = 0.1                         # for smooth camera follow
        new_x = target.rect.x - int(self.camera_size[0] / 2)
        new_y = target.rect.y - int(self.camera_size[1] / 2)

        self.rect.x += int((new_x - self.rect.x) * lerp)    # gives the camera some play
        self.rect.y += int((new_y - self.rect.y) * lerp)    # such that it wont follow the player tightly

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.boundaries.bottom:
            self.rect.bottom = self.boundaries.bottom
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.boundaries.right:
            self.rect.right = self.boundaries.right

    def draw(self, surface, all_sprites_group: pg.sprite.Group):
        all_sprites = all_sprites_group.sprites()
        colliding_sprites = []
        for sprite in all_sprites:
            if self.rect.colliderect(sprite.rect):
                colliding_sprites.append(sprite)
        for sprite in colliding_sprites:
            surface.blit(sprite.image, (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y))

        # To clamp the camera to a map smaller than the drawing surface, we have to create a new
        # surface, draw on it, then scale it to the target surface.