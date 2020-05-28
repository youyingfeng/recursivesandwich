import pygame as pg
from .playerstate import PlayerState

"""
Components form the base of our entities.
Here, I have abandoned the idea of inheritance in favour of composition, 
as we were getting cancerous classes with a lot of dependencies.
Instead, entities are now defined by the type of components we have.
The bulk of the processing is now done by the components, 
and the entities are basically containers for state.
Some components will also hold state.

This follows the Component design pattern laid out in game programming patterns.

Hopefully this code is reusable for other classes. Physics is defo reusable, as is render.
"""


class Component:
    def __init__(self):
        pass

    def update(self, *args):
        raise NotImplementedError


class PlayerInputComponent(Component):
    def __init__(self):
        super().__init__()

    def update(self, player, *args):
        print(player.state)
        current_keys = pg.key.get_pressed()
        if player.state == PlayerState.IDLE:
            if current_keys[pg.K_LEFT]:
                player.state = PlayerState.WALKING
                player.x_velocity = -3

            if current_keys[pg.K_RIGHT]:
                player.state = PlayerState.WALKING
                player.x_velocity = 3

            if current_keys[pg.K_SPACE]:
                player.state = PlayerState.JUMPING
                player.y_velocity = -10
        elif player.state == PlayerState.WALKING:
            if current_keys[pg.K_LEFT]:
                player.x_velocity = -3

            if current_keys[pg.K_RIGHT]:
                player.x_velocity = 3

            if not (current_keys[pg.K_LEFT] or current_keys[pg.K_RIGHT]):
                player.state = PlayerState.IDLE
                player.x_velocity = 0

            if current_keys[pg.K_SPACE]:
                player.state = PlayerState.JUMPING
                player.y_velocity = 10

        elif player.state == PlayerState.JUMPING:
            if current_keys[pg.K_LEFT]:
                player.x_velocity = -3

            if current_keys[pg.K_RIGHT]:
                player.x_velocity = 3

            if not (current_keys[pg.K_LEFT] or current_keys[pg.K_RIGHT]):
                player.x_velocity = 0


class PhysicsComponent(Component):
    def __init__(self):
        super().__init__()
        self.gravity = 1

    def update(self, entity, map):
        # Enforces gravity
        entity.y_velocity += self.gravity

        # Positions the entity at its future position
        entity.rect.y += entity.y_velocity

        # Handles collisions along the y axis first
        for colliding_sprite in pg.sprite.spritecollide(entity, map.terrain_group, False):
            if colliding_sprite.rect.top < entity.rect.top < colliding_sprite.rect.bottom:
                entity.rect.top = colliding_sprite.rect.bottom
            if colliding_sprite.rect.top < entity.rect.bottom < colliding_sprite.rect.bottom:
                if entity.state == PlayerState.JUMPING:
                    entity.state = PlayerState.IDLE
                entity.rect.bottom = colliding_sprite.rect.top
                entity.y_velocity = 0

        entity.rect.x += entity.x_velocity
        # Then handles collisions along the x axis
        for colliding_sprite in pg.sprite.spritecollide(entity, map.terrain_group, False):
            if colliding_sprite.rect.left < entity.rect.left < colliding_sprite.rect.right:
                entity.rect.left = colliding_sprite.rect.right
            if colliding_sprite.rect.left < entity.rect.right < colliding_sprite.rect.right:
                entity.rect.right = colliding_sprite.rect.left


        ## For some reason, swapping the order will mess up collision. Dont swap it. Always put y first.
        map_width = map.dimensions[0]
        # Then keeps everything within map boundaries
        if entity.rect.top < 0:
            entity.rect.top = 0
        if entity.rect.left < 0:
            entity.rect.left = 0
        elif entity.rect.right > map_width:
            entity.rect.right = map_width


class AnimationComponent(Component):
    def __init__(self, animations_list):
        super().__init__()
        # ok fuck this lets take in a dictionary
        self.animations_list = animations_list
        self.current_animation = self.animations_list[PlayerState.IDLE]
        self.current_state = None
        self.frame_counter = 0
        self.frames_per_update = 3
        self.current_index = 0
        self.animation_length = len(self.current_animation)

    def update(self, entity):
        if not (entity.state == self.current_state):
            self.current_state = entity.state
            self.current_animation = self.animations_list[self.current_state]
            self.frame_counter = 0
            self.current_index = 0
            self.animation_length = len(self.current_animation)
        else:
            self.frame_counter = (self.frame_counter + 1) % self.frames_per_update

        if self.frame_counter == 0:
            # this will probably cause some anim bugs
            self.current_index = (self.current_index + 1) % self.animation_length
            entity.image = self.current_animation[self.current_index]

    def get_current_image(self):
        return self.current_animation[self.current_index]


class RenderComponent(Component):
    def __init__(self):
        super().__init__()

    def update(self, entity, camera, surface):
        surface.blit(entity.image,
                     (entity.rect.x - camera.rect.x, entity.rect.y - camera.rect.y),
                     pg.Rect(6, 5, 21, 27))




