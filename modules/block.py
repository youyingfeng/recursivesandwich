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
		self.image = pg.transform.scale(type_object.image.convert_alpha(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
		self.blit_rect = pg.Rect(x + int(type_object.block_pos_x * Block.BLOCK_SIZE),
							y + int(type_object.block_pos_y * Block.BLOCK_SIZE),
							int(type_object.block_width * Block.BLOCK_SIZE),
							int(type_object.block_height * Block.BLOCK_SIZE))
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


# Has potential for many variations
class FallingBlock(Block):
	def __init__(self, type_object, x, y):
		super().__init__(type_object, x, y)
		self.falling = False
		self.vel = 1

	def update(self, player):
		if (self.rect.top == player.rect.bottom)\
			and (self.rect.left < player.rect.left < self.rect.right\
				or self.rect.left < player.rect.right < self.rect.right):
			self.blit_rect.y += self.vel
			self.rect.y = self.blit_rect.y

			# This is necessary - or else, player will fluctuate between the IDLE and JUMPING state
			# causing it to flash
			player.rect.bottom = self.rect.top


class MovingBlock(Block):
	def __init__(self, type_object, x, y):
		super().__init__(type_object, x, y)
		self.vel = 1

	def update(self, player):
		if (self.rect.top == player.rect.bottom)\
			and (self.rect.left < player.rect.left < self.rect.right\
				or self.rect.left < player.rect.right < self.rect.right):
			if (player.direction == Direction.RIGHT):
				self.blit_rect.x += self.vel
				self.rect.x = self.blit_rect.x
				player.rect.x = self.rect.x
			if (player.direction == Direction.LEFT):
				self.blit_rect.x -= self.vel
				self.rect.x = self.blit_rect.x
				player.rect.x = self.rect.x

			if pg.key.get_pressed()[pg.K_UP]:
				self.blit_rect.y -= self.vel
				self.rect.y = self.blit_rect.y
				player.rect.bottom = self.rect.top
			elif pg.key.get_pressed()[pg.K_DOWN]:
				self.blit_rect.y += self.vel
				self.rect.y = self.blit_rect.y
				player.rect.bottom = self.rect.top


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
		and updates the animation of the coin"""
		if pg.sprite.collide_rect(self, entity):
			if entity.health < 100:
				entity.health += 20
			self.coin_sound.play()
			self.kill()

		self.animation_component.update(self)


class Ladder(Block):
	def __init__(self, type_object, x, y):
		super().__init__(type_object, x, y)
		self.mid_rect = pg.Rect(self.rect.centerx - 0.5, self.rect.top, 1, self.rect.height)

	def update(self, entity):
		current_keys = pg.key.get_pressed()
		entity_mid_rect = pg.Rect(entity.rect.centerx - 0.5, entity.rect.top, 1, entity.rect.height)

		# A limitation that needs to be addressed is:
		# You cannot enter the HANGING state from JUMPINNG, because it could trigger endless jumping
		if self.mid_rect.colliderect(entity.rect) and entity.state != EntityState.JUMPING:
			if current_keys[pg.K_UP] or current_keys[pg.K_DOWN]:
				entity.state = EntityState.HANGING



