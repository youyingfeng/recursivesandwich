import pygame as pg


class HeadsUpDisplay:
    """Manages all elements of the GUI"""
    def __init__(self):
        self.healthbar = Healthbar()

    def update(self, player):
        self.healthbar.update(player)

    def render(self, surface):
        self.healthbar.render(surface)


class Healthbar(pg.sprite.Sprite):
    """Represents the health of the player on the GUI"""
    def __init__(self):
        super().__init__()
        # image is 49*17, while decoration is 64 * 17. Original offset is 14
        self.healthbar = pg.image.load("assets/textures/gui/health_bar.png").convert()
        self.healthbar.set_colorkey((0, 0, 0))

        self.healthbar_frame = pg.image.load("assets/textures/gui/health_bar_decoration.png")
        self.healthbar_frame.set_colorkey((0, 0, 0))

        self.image_offset = 14
        self.scale = 1.0

    def update(self, player):
        self.scale = player.health / 100

    def render(self, surface):
        surface.blit(self.healthbar_frame, (15, 15))
        surface.blit(self.healthbar, (15 + self.image_offset, 15), pg.Rect(0, 0, 49 * self.scale, 17))

