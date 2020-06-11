import pygame as pg
from .components import *
from .spritesheet import *


# Dungeon spritesheet
dungeon = Spritesheet("assets/textures/Dungeon/dungeon_spritesheet.png", 14, 23)


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

class GatewayBlock(Block):
	def __init__(self, type_object, x, y):
		super().__init__(type_object, x, y)

	def update(self, player, level):
		if player.rect.collidepoint(self.rect.centerx, self.rect.centery):
			pass
			# supposed to initiate a level change


# All blocks can really just be surbordinated to this block
class InteractiveBlock(Block):
	pass


class Coin(Block):
	def __init__(self, type_object, x, y):
		super().__init__(type_object, x, y)

		coin_animation = dungeon.get_images_at(15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18)
		self.animation_component = AnimationComponent(coin_animation)

		self.coin_sound = pg.mixer.Sound("assets/sound/sfx/coin.ogg")

	def update(self, entity):
		self.animation_component.update(self)

		# Handling collision with player
		x_collision = (self.rect.left <= entity.rect.left <= self.rect.right or self.rect.left <= entity.rect.right <= self.rect.right)\
				and (self.rect.top == entity.rect.bottom or self.rect.bottom == entity.rect.top)
		y_collision = (self.rect.top <= entity.rect.top <= self.rect.bottom or self.rect.top <= entity.rect.bottom <= self.rect.bottom)\
				and (self.rect.left == entity.rect.right or self.rect.right == entity.rect.left)
		if y_collision or x_collision:
			if entity.health < 100:
				entity.health += 20
			self.coin_sound.play()
			self.kill()