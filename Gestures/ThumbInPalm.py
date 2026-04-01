from Gestures.GenericGesture import Gesture

class ThumbInPalm(Gesture):
    def __init__(self, is_continuous: bool, action_func: callable, drop_func: callable, allow_mouse_mov: bool, hand:str):
        super().__init__(is_continuous, action_func, drop_func, allow_mouse_mov, hand)

    def match(self, bent_fingers, hand_landmarks, handedness: str) -> bool:
        thumb_tip = hand_landmarks.landmark[4]
        checkpoint = hand_landmarks.landmark[9]
        return (not bent_fingers) and thumb_tip.x < checkpoint.x and handedness == self.hand
