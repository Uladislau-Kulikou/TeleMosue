from abc import ABC, abstractmethod
from math import sqrt

class Gesture(ABC):
    @abstractmethod
    def __init__(self, is_continuous: bool,
                 action_func: callable,
                 drop_func: callable,
                 allow_mouse_mov: bool,
                 hand: str):
        """
        :param is_continuous: True if the gesture is continuous, False if it is one-shot
        :param action_func: Action callback
        :param drop_func: Drop/reset callback
        :param allow_mouse_mov: Whether this gesture allows mouse movement
        """
        self.is_continuous = is_continuous
        self.action_func = action_func
        self.drop_func = drop_func
        self.allow_mouse_movement = allow_mouse_mov
        self.hand = hand

    # Returns the gesture name when `print()` is called
    def __repr__(self):
        return self.__class__.__name__

    # Must return True when the gesture matches the builtin conditions, else False
    @abstractmethod
    def match(self, *args, **kwargs) -> bool:
        NotImplemented

    # Is used when the gesture needs to calculate the distance between 2 fingers
    @staticmethod
    def distance_3d(point1, point2) -> float:
        return sqrt(
            (point1.x - point2.x) ** 2 +
            (point1.y - point2.y) ** 2 +
            (point1.z - point2.z) ** 2
        )

    # Calles the given action function if it has one
    def action(self, *args, **kwargs) -> None:
        if self.action_func is not None:
            self.action_func()

    # Calles the given drop function if it has one
    def drop(self):
        if self.drop_func:
            self.drop_func()



