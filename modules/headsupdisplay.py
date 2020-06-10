import pygame as pg
import pygame.freetype as ft


class HeadsUpDisplay:
    """Manages all elements of the GUI"""
    def __init__(self):
        self.healthbar = Healthbar()
        self.fps_counter = FPSCounter()

    def update(self, player):
        self.healthbar.update(player)
        self.fps_counter.update()

    def render(self, surface):
        self.healthbar.render(surface)
        self.fps_counter.render(surface)


class Healthbar:
    """Represents the health of the player on the GUI"""
    def __init__(self):
        # image is 49*17, while decoration is 64 * 17. Original offset is 14
        self.healthbar = pg.image.load("assets/textures/hud/health_bar.png").convert()
        self.healthbar.set_colorkey((0, 0, 0))

        self.healthbar_frame = pg.image.load("assets/textures/hud/health_bar_decoration.png")
        self.healthbar_frame.set_colorkey((0, 0, 0))

        self.image_offset = 14
        self.scale = 1.0

    def update(self, player):
        self.scale = player.health / 100

    def render(self, surface):
        surface.blit(self.healthbar_frame, (15, 15))
        surface.blit(self.healthbar, (15 + self.image_offset, 15), pg.Rect(0, 0, 49 * self.scale, 17))


class FPSCounter:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.freetype = ft.Font("assets/fonts/pixChicago.ttf", 8)   # size must be set to 8, otherwise AA kicks in
        self.freetype.antialiased = False
        self.fps = self.freetype.render("0", (150, 100, 100), None, 0, 0, 8)

    def update(self):
        self.clock.tick()
        self.fps = self.freetype.render(str('%.1f' % self.clock.get_fps()), (150, 100, 100), None, 0, 0, 8)

    def render(self, surface):
        surface.blit(self.fps[0], (355, 20))
