import pygame as pg
from enum import Enum


class PlayerState(Enum):
    IDLE = 0
    WALKING = 1
    JUMPING = 2
    DEAD = 3


class Direction(Enum):
    LEFT = 0
    RIGHT = 1


class Action(Enum):
    WALK = 0
    STOP = 1
    JUMP = 2
    LAND = 3


class GameEvent(Enum):
    SWITCH_LEVEL = pg.USEREVENT + 0
    GAME_OVER = pg.USEREVENT + 1
