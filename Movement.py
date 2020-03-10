from typing import Union
from keyboard import press_and_release
from Meta import DIRECTION, AXIS, check


class Movement:
    def __init__(self, foot: str, axis: AXIS, direction: DIRECTION):
        if not check(axis, direction):
            raise Exception('Your axis is not compatible with your direction')
        self.__hotkey = dict()
        self.__threshold: Union[int, None] = None
        self.axis = axis
        self.direction = direction
        self.foot = foot

    def __str__(self) -> str:
        return f'({self.foot}, {self.axis.name}, {self.direction.name}, {self.__threshold}) -> {self.hotkey}'

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def hotkey(self) -> str:
        return self.__hotkey.get('key', None)

    @hotkey.setter
    def hotkey(self, hotkey: str) -> None:
        def x():
            press_and_release(hotkey)
        self.__hotkey = {
            'key': hotkey,
            'function': x
        }

    @property
    def threshold(self) -> Union[int, None]:
        return self.__threshold

    @threshold.setter
    def threshold(self, value: int) -> None:
        # Check to see if the threshold value is allowed
        if value < 0:
            raise ValueError('Threshold must be a positive number')
        self.__threshold = value

    def trigger(self, value: int) -> bool:
        if self.direction is DIRECTION.FORWARD or DIRECTION.LEFT:
            if value >= self.__threshold:
                return True
        if self.direction is DIRECTION.BACKWARD or DIRECTION.RIGHT:
            # Value in this case is negative
            if value <= -1 * self.__threshold:
                return True
        return False

    def is_left(self) -> bool:
        if self.foot == 'left':
            return True
        return False
