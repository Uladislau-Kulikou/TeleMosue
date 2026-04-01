from Gestures.GenericGesture import Gesture

class RPinchGesture(Gesture):
    def __init__(self, is_continuous: bool, action_func: callable, drop_func: callable, allow_mouse_mov: bool, hand:str):
        super().__init__(is_continuous, action_func, drop_func, allow_mouse_mov, hand)

    def match(self, hand_landmarks, handedness: str) -> bool:
        thumb_tip = hand_landmarks.landmark[4]
        middle_tip = hand_landmarks.landmark[12]

        distance = self.distance_3d(thumb_tip, middle_tip)
        comparing_line = self.distance_3d(hand_landmarks.landmark[5], hand_landmarks.landmark[9])
        relative_distance = distance / comparing_line
        return relative_distance < 1.7 and handedness == self.hand
