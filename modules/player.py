import pygame as pg

from .animations import Spritesheet
from .components import *


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
        self.state = PlayerState.IDLE

    def update(self, *args):
        raise NotImplementedError


class Player(Entity):
    def __init__(self):
        super().__init__()

        self.health = 100

        self.rect = pg.Rect(10, 10, 20, 30)
        self.blit_rect = pg.Rect(15, 3.5, 50, 30)


        # Spritesheets
        idle_spritesheet = Spritesheet("assets/sprites/adventurer/adventurer-idle.png", 1, 4)
        run_spritesheet = Spritesheet("assets/sprites/adventurer/adventurer-run.png", 1, 6)
        jump_spritesheet = Spritesheet("assets/sprites/adventurer/adventurer-jump.png", 1, 4)

        # Animations
        animation_library = {
                            PlayerState.IDLE: idle_spritesheet.get_images_at(0, 1, 2, 3),
                            PlayerState.WALKING: run_spritesheet.get_images_at(0, 1, 2, 3, 4, 5),
                            PlayerState.JUMPING: jump_spritesheet.get_images_at(0, 1, 2, 3)
                   	        }

        # Sounds
        jump_sound = pg.mixer.Sound("assets/sound/sfx/jump.ogg")
        sound_library = {
                         "JUMP": jump_sound
                        }

        # Components
        self.input_component = PlayerInputComponent()
        self.animation_component = AnimationComponent(animation_library, self.state)
        self.physics_component = PhysicsComponent()
        self.sound_component = SoundComponent(sound_library)
        self.render_component = RenderComponent()

        # Current Image
        self.image = self.animation_component.get_current_image()

    def message(self, message):
        # Apart from sound, can force animation to receive animations too
        self.sound_component.receive(message)

    def handle_input(self):
        self.input_component.update(self)

    def update(self, map):
        self.physics_component.update(self, map)
        self.animation_component.update(self)

    def render(self, camera, surface):
        self.render_component.update(self, camera, surface, self.blit_rect)


class Enemy(Entity):
    def __init__(self, type_object, ai_component, physics_component, render_component, starting_position):
        super().__init__()

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

        # TESTING
        self.damage_collide_component = DamageCollisionComponent()

        # Animation and sound are taken from a type object
        self.animation_component = AnimationComponent(type_object.animation_library, self.state)
        self.sound_component = SoundComponent(type_object.sound_library)

        # Current Image
        self.image = self.animation_component.get_current_image()

    def message(self, message):
        pass
    
    def update(self, map, player):
        self.input_component.update(self)
        self.physics_component.update(self, map)
        self.damage_collide_component.update(self, player)
        self.animation_component.update(self)

    def render(self, camera, surface):
        self.render_component.update(self, camera, surface, self.blit_rect)


class EnemyType:
    def __init__(self):
        # Spritesheets
        idle_spritesheet = Spritesheet("assets/sprites/player/Idle.png", 1, 11)
        run_spritesheet = Spritesheet("assets/sprites/player/Run.png", 1, 12)
        jump_spritesheet = Spritesheet("assets/sprites/player/Jump.png", 1, 1)

        # Sounds
        jump_sound = pg.mixer.Sound("assets/sound/sfx/jump.ogg")

        self.health = 100
        self.animation_library = {
            PlayerState.IDLE: idle_spritesheet.get_images_at(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
            PlayerState.WALKING: run_spritesheet.get_images_at(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
            PlayerState.JUMPING: jump_spritesheet.get_images_at(0)
        }
        self.sound_library = {
            "JUMP": jump_sound
        }

