from Gestures.GenericGesture import Gesture

class HornsGesture(Gesture):
    def __init__(self, is_continuous: bool, action_func: callable, drop_func: callable, allow_mouse_mov: bool, hand:str):
        super().__init__(is_continuous, action_func, drop_func, allow_mouse_mov, hand)

    def match(self, bent_fingers, handedness: str) -> bool:
        return (8 not in bent_fingers
                and 12 in bent_fingers
                and 16 in bent_fingers
                and 20 not in bent_fingers) and handedness == self.hand


