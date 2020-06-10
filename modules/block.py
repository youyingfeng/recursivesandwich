import pygame as pg


# -------------------- Type objects to store hitboxes of different textures -------------------- #
# This level of complication is really just to make life easier
class TerrainType:
	def __init__(self, image: pg.Surface, block_pos_x=0, block_pos_y=0, block_width=1, block_height=1):
		# All numbers are relative to the size of a normal block (i.e. must be between 0 and 1, where 1 is the size of
		# an actual block)
		self.image = image
		self.block_pos_x = block_pos_x
		self.block_pos_y = block_pos_y
		self.block_width = block_width
		self.block_height = block_height


class Block(pg.sprite.Sprite):
	BLOCK_SIZE = 25

	def __init__(self, type_object: TerrainType, x, y):
		super().__init__()
		self.image = pg.transform.scale(type_object.image.convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
		self.blit_rect = pg.Rect(x, y, Block.BLOCK_SIZE, Block.BLOCK_SIZE)
		self.rect = pg.Rect(x + int(type_object.block_pos_x * Block.BLOCK_SIZE),
							y + int(type_object.block_pos_y * Block.BLOCK_SIZE),
							int(type_object.block_width * Block.BLOCK_SIZE),
							int(type_object.block_height * Block.BLOCK_SIZE))


class HazardousBlock(Block):
	def __init__(self, type_object, x, y):
		super().__init__(type_object, x, y)

	def update(self, entity):
		if (self.rect.left < entity.rect.left < self.rect.right or self.rect.left < entity.rect.right < self.rect.right)\
				and self.rect.top == entity.rect.bottom:
			entity.take_damage(20)




