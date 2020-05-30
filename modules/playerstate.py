from enum import Enum


class PlayerState(Enum):
    IDLE = 0
    WALKING = 1
    JUMPING = 2


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
