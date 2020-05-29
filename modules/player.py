import pygame as pg

from .animations import Spritesheet, Animation
from .components import *


MAX_HEALTH = 100


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Player state
        self.x_velocity = 0
        self.y_velocity = 0
        self.rect = pg.Rect(10, 10, 21, 27)
        self.state = PlayerState.IDLE
        self.direction = None

        spritesheet1 = Spritesheet("assets/sprites/Idle (32x32).png", 1, 11)
        spritesheet2 = Spritesheet("assets/sprites/Run (32x32).png", 1, 12)
        spritesheet3 = Spritesheet("assets/sprites/Jump (32x32).png", 1, 1)

        animation_sequence = {
                              PlayerState.IDLE: spritesheet1.get_images_at(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                              PlayerState.WALKING: spritesheet2.get_images_at(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
                              PlayerState.JUMPING: spritesheet3.get_images_at(0)
                             }

        # Player components
        self.input_component = PlayerInputComponent()
        self.animation_component = AnimationComponent(animation_sequence)
        self.physics_component = PhysicsComponent()
        self.render_component = RenderComponent()

        self.image = self.animation_component.get_current_image()

    def handle_input(self):
        self.input_component.update(self)

    def update(self, map):
        self.physics_component.update(self, map)
        self.animation_component.update(self)

        #pygame has a listener already with its inbuilt events
        #so what we need to do is just send a gameover event
        #then let the scene handle the event

    def render(self, camera, surface):
        self.render_component.update(self, camera, surface)
