import pygame as pg


# Every Block has an image and a Rect, both of the same square size.
class Block(pg.sprite.Sprite):
	BLOCK_SIZE = 25

	def __init__(self, image, x, y):
		super().__init__()
		self.image = pg.transform.scale(image.convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
		self.rect = pg.Rect(x, y, Block.BLOCK_SIZE, Block.BLOCK_SIZE)
		self.blit_rect = pg.Rect(x, y, Block.BLOCK_SIZE, Block.BLOCK_SIZE)


class HazardousBlock(Block):
	def __init__(self, image, x, y):
		super().__init__(image, x, y)
		self.rect = pg.Rect(x, y + 10, Block.BLOCK_SIZE, Block.BLOCK_SIZE - 10)
		self.blit_rect = pg.Rect(x, y, Block.BLOCK_SIZE, Block.BLOCK_SIZE)

	def update(self, entity):
		if (self.rect.left < entity.rect.left < self.rect.right or self.rect.left < entity.rect.right < self.rect.right)\
				and self.rect.top == entity.rect.bottom:
			entity.take_damage()


# -------------------- Type objects to store hitboxes of different textures -------------------- #
# This level of complication is really just to make life easier
class TerrainTypeSpike:
	def __init__(self):
		# All numbers are relative to the size of a normal block (i.e. must be between 0 and 1, where 1 is the size of
		# an actual block)
		self.block_pos_x = 0		# Left edge of the actual block
		self.block_pos_y = 0.4		# Top edge of the actual block
		self.block_width = 1		# Width of the actual block
		self.block_height = 0.6		# Height of the actual block

