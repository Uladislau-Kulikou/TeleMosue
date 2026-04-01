from Gestures.GenericGesture import Gesture

class LPinchGesture(Gesture):
    def __init__(self, is_continuous: bool, action_func: callable, drop_func: callable, allow_mouse_mov: bool, hand:str):
        super().__init__(is_continuous, action_func, drop_func, allow_mouse_mov, hand)

    def match(self, hand_landmarks, handedness: str) -> bool:
        thumb_tip = hand_landmarks.landmark[4]
        point_tip = hand_landmarks.landmark[8]

        distance = self.distance_3d(thumb_tip, point_tip)
        comparing_line = self.distance_3d(hand_landmarks.landmark[5], hand_landmarks.landmark[9])
        relative_distance = distance / comparing_line
        return relative_distance < 1.7 and handedness == self.hand




