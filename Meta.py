from enum import Enum, unique


@unique
class AXIS(Enum):
    """
    Enum defining the different axes the footpedal has
    """
    PITCH = 1
    YAW = 2
    ROLL = 3

    def __str__(self):
        return f'{self.value}. {self.name}'


@unique
class DIRECTION(Enum):
    """
    Enum defining the directions the footpedal can move in considering the axis

    Mappings
    - PITCH => (Forward, Backward)
    - YAW => (Left, Right)
    - ROLL => (Left, Right)
    """
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4

    def __str__(self):
        return f'{self.value}. {self.name}'


def check(axis: AXIS, direction: DIRECTION) -> bool:
    if axis is AXIS.PITCH:
        if direction is DIRECTION.FORWARD or direction is DIRECTION.BACKWARD:
            return True
        return False
    if direction is DIRECTION.LEFT or direction is DIRECTION.RIGHT:
        return True
    return False
