from Gestures.GenericGesture import Gesture

class PalmGesture(Gesture):
    def __init__(self, is_continuous: bool, action_func: callable, drop_func: callable, allow_mouse_mov: bool, hand:str):
        super().__init__(is_continuous, action_func, drop_func, allow_mouse_mov, hand)

    @staticmethod
    def match() -> bool:
        return True


