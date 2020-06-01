import pygame as pg

from .animations import Spritesheet
from .components import *


MAX_HEALTH = 100


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.rect = pg.Rect(10, 10, 21, 27)

        # Physics attributes
        self.x_velocity = 0
        self.y_velocity = 0

        # Direction:
        self.direction = Direction.RIGHT

        self.state = PlayerState.IDLE

        # Spritesheets
        idle_spritesheet = Spritesheet("assets/sprites/player/Idle.png", 1, 11)
        run_spritesheet = Spritesheet("assets/sprites/player/Run.png", 1, 12)
        jump_spritesheet = Spritesheet("assets/sprites/player/Jump.png", 1, 1)

        # Dictionary of animation sequences (key: PlayerState; value: list of frames)
        animation_sequences = {
                               PlayerState.IDLE: idle_spritesheet.get_images_at(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                               PlayerState.WALKING: run_spritesheet.get_images_at(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
                               PlayerState.JUMPING: jump_spritesheet.get_images_at(0)
                              }

        jump_sound = pg.mixer.Sound("assets/sound/sfx/jump.ogg")

        sound_library = {
                         "JUMP": jump_sound
                        }

        # Components
        self.input_component = PlayerInputComponent()
        self.animation_component = AnimationComponent(animation_sequences, self.state)
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
        self.render_component.update(self, camera, surface)
