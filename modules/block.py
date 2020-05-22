import pygame as pg


class Block(pg.sprite.Sprite):

    BLOCK_SIZE = 20

    def __init__(self, image, x, y):
        super().__init__()
        self.image = pg.transform.scale(image.convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
        self.rect = pg.Rect(x, y, Block.BLOCK_SIZE, Block.BLOCK_SIZE)
        self.mask = pg.mask.from_surface(self.image)