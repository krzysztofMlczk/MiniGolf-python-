from enum import Enum


class BallState(Enum):
    CLICKED = 1
    MOVING = 2
    NOT_MOVING = 3
    IN_CUP = 4
