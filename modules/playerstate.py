from enum import Enum


class PlayerState(Enum):
    IDLE = 0
    WALKING = 1
    JUMPING = 2
    DYING = 3


class Direction(Enum):
    LEFT = 0
    RIGHT = 1


class Action(Enum):
    WALK = 0
    STOP = 1
    JUMP = 2
    LAND = 3
