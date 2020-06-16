import pygame as pg
import pygame.freetype as ft

"""
* =============================================================== *
* This module contains the various classes required to make a     *
* Heads-Up Display (HUD) in the game.                             *
* =============================================================== *
"""


class HeadsUpDisplay:
    """Manages all elements of the HUD"""
    def __init__(self):
        # self.vignette = Vignette()
        self.healthbar = Healthbar()
        self.fps_counter = FPSCounter()

    def update(self, player, camera):
        """Updates all the elements of the HUD"""
        # self.vignette.update(player, camera)
        self.healthbar.update(player)
        self.fps_counter.update()

    def render(self, surface):
        """Renders the elements of the HUD onto the specified surface"""
        # self.vignette.render(surface)
        self.healthbar.render(surface)
        self.fps_counter.render(surface)


class Healthbar:
    """Tracks the current health of the player"""
    def __init__(self):
        # image is 49*17, while decoration is 64 * 17. Original offset is 14
        self.healthbar = pg.image.load("assets/textures/hud/health_bar.png").convert()
        self.healthbar.set_colorkey((0, 0, 0))

        self.healthbar_frame = pg.image.load("assets/textures/hud/health_bar_decoration.png")
        self.healthbar_frame.set_colorkey((0, 0, 0))

        self.image_offset = 14
        self.scale = 1.0

    def update(self, player):
        """Updates the scaling factor of the health bar in proportion to the current health of the player"""
        self.scale = player.health / 100

    def render(self, surface):
        """Renders the health bar at the top-left corner of the specified surface"""
        surface.blit(self.healthbar_frame, (15, 15))
        surface.blit(self.healthbar, (15 + self.image_offset, 15), pg.Rect(0, 0, 49 * self.scale, 17))


class FPSCounter:
    """Tracks the FPS of the game"""
    def __init__(self):
        self.clock = pg.time.Clock()
        self.freetype = ft.Font("assets/fonts/pixChicago.ttf", 8)   # size must be set to 8, otherwise AA kicks in
        self.freetype.antialiased = False
        self.fps = self.freetype.render("0", (150, 100, 100), None, 0, 0, 8)

    def update(self):
        """Updates the current FPS of the game"""
        self.clock.tick()
        self.fps = self.freetype.render(str('%.1f' % self.clock.get_fps()), (150, 100, 100), None, 0, 0, 8)

    def render(self, surface):
        """Renders the FPS counter at the top-right corner of the specified surface"""
        surface.blit(self.fps[0], (355, 20))


class Vignette:
    """Limits the vision of the player"""
    # Since this is a post-process
    def __init__(self):
        self.image = pg.Surface((400, 300))

    def update(self, player, camera):
        """Marks a circular area around the player's position on the surface as transparent"""
        self.image = pg.Surface((400, 300))
        self.image.fill((20, 20, 20))
        pg.draw.circle(self.image,
                       (255, 255, 255),
                       (player.rect.centerx - camera.rect.x,
                        player.rect.centery - camera.rect.y),
                       100)
        self.image.set_colorkey((255, 255, 255))

    def render(self, surface: pg.Surface):
        """Renders the vignette onto the screen"""
        surface.blit(self.image, (0, 0))
