import pygame as pg


# Every Block has an image and a Rect, both of the same square size.
class Block(pg.sprite.Sprite):
	BLOCK_SIZE = 25

	def __init__(self, image, x, y):
		super().__init__()
		self.image = pg.transform.scale(image.convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
		self.rect = pg.Rect(x, y, Block.BLOCK_SIZE, Block.BLOCK_SIZE)