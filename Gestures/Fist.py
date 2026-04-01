from Gestures.GenericGesture import Gesture

class FistGesture(Gesture):
    def __init__(self, is_continuous: bool, action_func: callable, drop_func: callable, allow_mouse_mov: bool, hand:str):
        super().__init__(is_continuous, action_func, drop_func, allow_mouse_mov, hand)

    def match(self, bent_fingers, handedness) -> bool:
        return len(bent_fingers) == 4 and handedness == self.hand

    def action(self, prev_hand_landmarks, hand_landmarks) -> None:
        self.action_func(prev_hand_landmarks, hand_landmarks)