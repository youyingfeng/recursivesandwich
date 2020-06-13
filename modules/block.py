import pygame as pg
from .components import *
from .entitystate import GameEvent
from .spritesheet import *

"""
* =============================================================== *
* This module contains Blocks, which are representations of the   *
* individual tiles of the game map.								  *
* =============================================================== *

"""


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
	"""Represents a block that damages the player if the player comes into contact with it"""
	def __init__(self, type_object, x, y):
		super().__init__(type_object, x, y)

	def update(self, entity):
		"""Checks for collison between the player and the Hazardous Block, and damages the player upon colliding"""
		if (self.rect.left < entity.rect.left < self.rect.right or self.rect.left < entity.rect.right < self.rect.right)\
				and self.rect.top == entity.rect.bottom:
			entity.take_damage(20)


class GatewayBlock(Block):
	"""Represents the endpoint of the level"""
	def __init__(self, type_object, x, y):
		super().__init__(type_object, x, y)

	def update(self, player):
		"""Checks if the player has collided with itself, and initiates a level transition if there is a collision"""
		if player.rect.collidepoint(self.rect.centerx, self.rect.centery):
			pg.event.post(
				pg.event.Event(
					GameEvent.SWITCH_LEVEL.value
				)
			)


# All blocks can really just be surbordinated to this block
class InteractiveBlock(Block):
	pass


class Coin(Block):
	"""Represents a coin which heals the player when picked up"""
	def __init__(self, type_object, x, y):
		super().__init__(type_object, x, y)
		dungeon = Spritesheet("assets/textures/Dungeon/dungeon_spritesheet.png", 14, 23)
		coin_animation = dungeon.get_images_at(15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18)
		self.animation_component = AnimationComponent(coin_animation)
		self.coin_sound = pg.mixer.Sound("assets/sound/sfx/coin.ogg")

	def update(self, entity):
		"""Checks if the player has collided with the coin, healing the player if there is a collision,
		then updates the animation of the coin"""
		if pg.sprite.collide_rect(self, entity):
			if entity.health < 100:
				entity.health += 20
			self.coin_sound.play()
			self.kill()

		self.animation_component.update(self)
