import pygame as pg


# =============================================================== #
# The Camera class keeps track of the viewport of the game using  #
# a Rect. The object is always passed to the renderer when        #
# rendering sprites onto the screen.                              #
# =============================================================== #


class Camera:
    def __init__(self, camera_size, map):
        self.boundaries = map.rect

        # Rudimentary clamping of camera to map bounds only on the x-axis
        # If the map is smaller than the camera, then rescale the camera size (pretty sure this code is buggy though)
        # Solution: Either delegate all drawing to the Camera, or don't make maps smaller than the camera
        if self.boundaries.right < camera_size[0]:
            temp = camera_size
            camera_size = (self.boundaries.right, int(temp[1] * self.boundaries.right / temp[0]))
        
        self.camera_size = camera_size
        self.rect = pg.Rect((0, 0), camera_size)

    # Moves this camera's position to the target's position
    def follow_target(self, target):
        # Give the camera some lag
        lerp = 0.1
        new_x = target.rect.x - int(self.camera_size[0] / 2)
        new_y = target.rect.y - int(self.camera_size[1] / 2)
        self.rect.x += int((new_x - self.rect.x) * lerp)
        self.rect.y += int((new_y - self.rect.y) * lerp * 0.5)

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.boundaries.bottom:
            self.rect.bottom = self.boundaries.bottom
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.boundaries.right:
            self.rect.right = self.boundaries.right