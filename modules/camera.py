import pygame as pg


'''Camera structure: Since the Map and Player contains a Rect attribute, we initiialize
the map as a big Rect and make the camera follow the Player, only drawing stuff inside
the Rect.'''


class Camera:
    def __init__(self, camera_size, map):
        self.boundaries = map.rect

        # Rudimentary clamping of camera to map bounds only on the x-axis
        '''To clamp the camera to a map smaller than the drawing surface, we have to 
        create a new surface, draw on it, then scale it to the target surface.'''
        if self.boundaries.right < camera_size[0]:
            temp = camera_size
            camera_size = (self.boundaries.right, int(temp[1] * self.boundaries.right / temp[0]))
        
        self.camera_size = camera_size
        self.rect = pg.Rect((0, 0), camera_size)

    # Moves this camera's position to the target's position
    def follow_target(self, target: pg.sprite.Sprite):
        # Give the camera some lag
        lerp = 0.1
        new_x = target.rect.x - int(self.camera_size[0] / 2)
        new_y = target.rect.y - int(self.camera_size[1] / 2)
        self.rect.x += int((new_x - self.rect.x) * lerp)
        self.rect.y += int((new_y - self.rect.y) * lerp)

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

        # Make list of sprites whose Rects fall within the camera Rect
        captured_sprites = []
        for sprite in all_sprites:
            if self.rect.colliderect(sprite.rect):
                captured_sprites.append(sprite)

        # Blit these Rects on the game_display
        for sprite in captured_sprites:
            surface.blit(sprite.image, (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y))