import pygame as pg
from .playerstate import PlayerState, Direction


"""Components form the base of our entities. Here, I have abandoned the idea 
of inheritance in favour of composition, as we were getting cancerous classes 
with a lot of dependencies. Instead, entities are now defined by the type of 
components we have. The bulk of the processing is now done by the components, 
and the entities are basically containers for state. Some components will also 
hold state. This follows the Component design pattern laid out in game programming 
patterns. Hopefully this code is reusable for other classes. Physics is defo 
reusable, as is render."""


class Component:
    def __init__(self):
        pass

    def update(self, *args):
        raise NotImplementedError


# -------------------- PLAYER COMPONENTS -------------------- #
class PlayerInputComponent(Component):
    def __init__(self):
        super().__init__()

    def update(self, player, *args):
        current_keys = pg.key.get_pressed()
        if player.state == PlayerState.IDLE:
            if current_keys[pg.K_LEFT]:
                player.state = PlayerState.WALKING
                player.direction = Direction.LEFT
                player.x_velocity = -3

            if current_keys[pg.K_RIGHT]:
                player.state = PlayerState.WALKING
                player.direction = Direction.RIGHT
                player.x_velocity = 3

            if current_keys[pg.K_SPACE]:
                player.state = PlayerState.JUMPING
                player.y_velocity = -13
                player.message("JUMP")

        elif player.state == PlayerState.WALKING:
            if current_keys[pg.K_LEFT]:
                player.x_velocity = -3
                player.direction = Direction.LEFT

            if current_keys[pg.K_RIGHT]:
                player.x_velocity = 3
                player.direction = Direction.RIGHT

            if not (current_keys[pg.K_LEFT] or current_keys[pg.K_RIGHT]):
                player.state = PlayerState.IDLE
                player.x_velocity = 0

            if current_keys[pg.K_SPACE]:
                player.state = PlayerState.JUMPING
                player.y_velocity = -13
                player.message("JUMP")

        elif player.state == PlayerState.JUMPING:
            if current_keys[pg.K_LEFT]:
                player.x_velocity = -3
                player.direction = Direction.LEFT

            if current_keys[pg.K_RIGHT]:
                player.x_velocity = 3
                player.direction = Direction.RIGHT

            if not (current_keys[pg.K_LEFT] or current_keys[pg.K_RIGHT]):
                player.x_velocity = 0


class PhysicsComponent(Component):
    def __init__(self):
        super().__init__()
        self.gravity = 1

    def update(self, entity, map):
        # Enforces gravity
        entity.y_velocity += self.gravity

        # Handles collisions along the y axis first
        # Positions the entity at its future position
        entity.rect.y += entity.y_velocity
        # Hacky fix
        isJumping = True
        for colliding_sprite in pg.sprite.spritecollide(entity, map.terrain_group, False):
            if colliding_sprite.rect.top < entity.rect.top < colliding_sprite.rect.bottom:
                entity.rect.top = colliding_sprite.rect.bottom
            if colliding_sprite.rect.top < entity.rect.bottom < colliding_sprite.rect.bottom:
                isJumping = False
                if entity.state == PlayerState.JUMPING:
                    entity.state = PlayerState.IDLE
                entity.rect.bottom = colliding_sprite.rect.top
                entity.y_velocity = 0

        # This is a hack to ensure that people fall properly
        if isJumping:
            entity.state = PlayerState.JUMPING

        entity.rect.x += entity.x_velocity
        # Then handles collisions along the x axis
        for colliding_sprite in pg.sprite.spritecollide(entity, map.terrain_group, False):
            if colliding_sprite.rect.left < entity.rect.left < colliding_sprite.rect.right:
                entity.rect.left = colliding_sprite.rect.right
            if colliding_sprite.rect.left < entity.rect.right < colliding_sprite.rect.right:
                entity.rect.right = colliding_sprite.rect.left

        map_width = map.dimensions[0]
        # Then keeps everything within map boundaries
        if entity.rect.top < 0:
            entity.rect.top = 0
        if entity.rect.left < 0:
            entity.rect.left = 0
        elif entity.rect.right > map_width:
            entity.rect.right = map_width


class AnimationComponent(Component):
    def __init__(self, animation_sequences, state: PlayerState):
        super().__init__()
        
        # Save a dictionary of animations
        self.animation_sequences = animation_sequences

        # Current animation of entity will depend on its current_state
        self.current_state = state
        self.current_animation = self.animation_sequences[self.current_state]

        self.frame_counter = 0
        self.frames_per_update = 5
        self.current_index = 0
        self.animation_length = len(self.current_animation)

    def update(self, entity):
        # If entity has changed its state
        if entity.state != self.current_state:
            # Update current state of animation
            self.current_state = entity.state
            self.current_animation = self.animation_sequences[self.current_state]
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
        # Flip image if Player is moving backward
        if entity.direction == Direction.LEFT:
            rendered_image = pg.transform.flip(entity.image, True, False)
        else:
            rendered_image = entity.image

        surface.blit(rendered_image,
                     (entity.rect.x - camera.rect.x, entity.rect.y - camera.rect.y),
                     entity.blit_rect)


class SoundComponent(Component):
    def __init__(self, sounds):
        super().__init__()
        self.state = None
        self.sounds = sounds

    def update(self, *args):
        pass

    def receive(self, message):
        if message == "WALK":
            pass
            # play walking sound in infinite loop
        elif message == "STOP":
            pass
            # stop walking sound playback
        elif message == "JUMP":
            # also stop walking sound playback
            self.sounds["JUMP"].play()
        elif message == "LAND":
            pass
            # play landing sound
        elif message == "HIT":
            self.sounds["HIT"].play()


# -------------------- ENEMY COMPONENTS -------------------- #
class EnemyAIInputComponent(Component):
    # This is a simple AI component that walks back and forth between two points
    def __init__(self):
        super().__init__()

    def update(self, entity, *args):
        entity.state = PlayerState.WALKING
        if entity.direction == Direction.LEFT:
            if entity.rect.x > entity.left_bound:
                entity.x_velocity = -1
            else:
                entity.direction = Direction.RIGHT
                entity.x_velocity = 1
        else:
            if entity.rect.x < entity.right_bound:
                entity.x_velocity = 1
            else:
                entity.direction = Direction.LEFT
                entity.x_velocity = -1


class DamageCollisionComponent(Component):
    def __init__(self):
        super().__init__()

    def update(self, entity, player):
        # sprite can technically be any mob, but here it is the player since mobs will not damage other mobs.
        if pg.sprite.collide_rect(entity, player):
            player.take_damage()      # something like this


