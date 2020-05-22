import pygame as pg


# TODO: Camera structure
# Since the map can be structured as a rect, and the player is a rect also,
# make the camera class to follow the player around and only draw stuff in the rect.
# possibly using collision. Block detection in a rect is possible.
# IDEA: Initialise the map as a big rect, then make the camera follow the character


class Camera:

    SURFACE_SIZE = (400, 300)

    def __init__(self):
        self.camera_size = Camera.SURFACE_SIZE
        self.rect = pg.Rect((0, 0), Camera.SURFACE_SIZE)

    # Moves this camera's position to the target's position
    def update(self, target: pg.sprite.Sprite):
        self.rect.x = target.rect.x - int(self.camera_size[0] / 2)
        self.rect.y = target.rect.y - int(self.camera_size[1] / 2)

    # Draws all the sprites from all_sprites_group onto the surface
    def draw(self, surface, all_sprites_group: pg.sprite.Group):
        all_sprites = all_sprites_group.sprites()
        colliding_sprites = []
        for sprite in all_sprites:
            if self.rect.colliderect(sprite.rect):
                colliding_sprites.append(sprite)
        for sprite in colliding_sprites:
            surface.blit(sprite.image, (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y))