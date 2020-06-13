import pygame as pg

from .entitystate import GameEvent
from .spritesheet import Spritesheet
from .components import *


"""
* =============================================================== *
* This module contains all relevant classes required for the      *
* instantiation of the Player and Enemies.                        *
* =============================================================== *

HOW TO MAKE A NEW ENEMY VARIANT
-------------------------
1.  Make a new EnemyType object with the following public attributes:
        health: int                 ->      Maximum health of the Enemy
        animation_library: dict     ->      Dictionary containing the different 
                                            animation sequences to be played 
                                            for each state
        sound_library: dict         ->      Dictionary containing the different
                                            sounds to be played for each state
2.  Pass this EnemyType object to the Enemy constructor to instantiate a new variant 
    of Enemy
"""


class Entity(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Defines the hitbox of the Entity. Must be redefined in the subclass.
        self.rect = None                   

        # Velocities
        self.x_velocity = 0              
        self.y_velocity = 0

        # Direction which the Entity is facing
        self.direction = Direction.RIGHT

        # State of the entity  
        self.state = EntityState.IDLE

    def update(self, *args):
        raise NotImplementedError


class Player(Entity):
    """Represents the player character"""
    def __init__(self):
        super().__init__()
        self.health = 100

        self.rect = pg.Rect(10, 10, 20, 30)
        self.blit_rect = pg.Rect(15, 3.5, 50, 30)

        self.last_collide_time = 0

        # Spritesheets
        idle_spritesheet = Spritesheet("assets/sprites/adventurer/adventurer-idle.png", 1, 4)
        run_spritesheet = Spritesheet("assets/sprites/adventurer/adventurer-run.png", 1, 6)
        jump_spritesheet = Spritesheet("assets/sprites/adventurer/adventurer-jump.png", 1, 1)

        # Animations
        animation_library = {
                            EntityState.IDLE: idle_spritesheet.get_images_at(0, 1, 2, 3),
                            EntityState.WALKING: run_spritesheet.get_images_at(0, 1, 2, 3, 4, 5),
                            EntityState.JUMPING: jump_spritesheet.get_images_at(0)
                            }

        # Sounds
        jump_sound = pg.mixer.Sound("assets/sound/sfx/jump.ogg")
        hit_sound = pg.mixer.Sound("assets/sound/sfx/hitdamage.ogg")

        sound_library = {
                         "JUMP": jump_sound,
                         "HIT": hit_sound
                        }

        # Components
        self.input_component = PlayerInputComponent()
        self.animation_component = PlayerAnimationComponent(animation_library, self.state)
        self.physics_component = PhysicsComponent()
        self.sound_component = SoundComponent(sound_library)
        self.render_component = RenderComponent()

        # Current Image
        self.image = self.animation_component.get_current_image()

    # ---------- DIRTY METHODS ---------- #
    # These will be placed here until I can find a way to wrap them in a component nicely
    def take_damage(self, damage):
        """Decreases the health of the player by the specified amount"""
        if self.is_immune():
            return
        else:
            self.health -= damage
            self.last_collide_time = pg.time.get_ticks()
            self.message("HIT")
            self.y_velocity = -2

        if self.health <= 0:
            self.state = EntityState.DEAD
            pg.event.post(
                pg.event.Event(
                    GameEvent.GAME_OVER.value
                )
            )

    def is_immune(self):
        return self.last_collide_time > pg.time.get_ticks() - 500

    def message(self, message):
        # Apart from sound, can force animation to receive animations too
        # But it is too much work to do animation, so we will not do that
        self.sound_component.receive(message)

    def handle_input(self):
        self.input_component.update(self)

    def update(self, map):
        self.physics_component.update(self, map)
        self.animation_component.update(self)

    def render(self, camera, surface):
        self.render_component.update(self, camera, surface)


class Enemy(Entity):
    """Base class for all enemies"""
    def __init__(self, type_object, ai_component, physics_component, render_component, starting_position):
        super().__init__()

        self.health = 100

        # Define starting position
        # index 0 is x position, index 1 is y position, index 2 is patrol range
        self.rect = pg.Rect(starting_position[0], starting_position[1], 20, 27)

        self.blit_rect = pg.Rect(5, 3.5, 50, 30)

        # Boundaries for patrol
        self.left_bound = starting_position[0] - starting_position[2]
        self.right_bound = starting_position[0] + starting_position[2]

        # Components
        self.input_component = ai_component
        self.physics_component = physics_component
        self.render_component = render_component

        # Taking damage
        self.damage_collide_component = EnemyDamageCollisionComponent()

        # Animation and sound are taken from a type object
        self.animation_component = PlayerAnimationComponent(type_object.animation_library, self.state)
        self.sound_component = SoundComponent(type_object.sound_library)

        # Current Image
        self.image = self.animation_component.get_current_image()

    def take_damage(self, damage):
        """Instantly kills the enemy"""
        # TODO: Properly handle animations for dying
        self.state = EntityState.DEAD

    def message(self, message):
        pass
    
    def update(self, map, player):
        self.input_component.update(self)
        self.physics_component.update(self, map)
        self.damage_collide_component.update(self, player)
        self.animation_component.update(self)

    def render(self, camera, surface):
        self.render_component.update(self, camera, surface)


class EnemyType:
    """Template object representing the type of enemy, which is passed into the Enemy constructor to
        instantiate an Enemy with the corresponding visuals, health and sounds"""
    def __init__(self):
        # Spritesheets
        idle_spritesheet = Spritesheet("assets/sprites/player/Idle.png", 1, 11)
        run_spritesheet = Spritesheet("assets/sprites/player/Run.png", 1, 12)
        jump_spritesheet = Spritesheet("assets/sprites/player/Jump.png", 1, 1)

        # Sounds
        jump_sound = pg.mixer.Sound("assets/sound/sfx/jump.ogg")

        self.health = 100
        self.animation_library = {
            EntityState.IDLE: idle_spritesheet.get_images_at(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
            EntityState.WALKING: run_spritesheet.get_images_at(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
            EntityState.JUMPING: jump_spritesheet.get_images_at(0),
            EntityState.DEAD: idle_spritesheet.get_images_at(0)
        }
        self.sound_library = {
            "JUMP": jump_sound
        }
