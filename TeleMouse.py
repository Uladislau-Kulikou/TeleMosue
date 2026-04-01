import threading
import time

import cv2
import mediapipe as mp
from attr import dataclass
from globals import FINGER_TIPS

import actions
from Gestures.Fist import FistGesture
from Gestures.GenericGesture import Gesture
from Gestures.Horns import HornsGesture
from Gestures.LPinch import LPinchGesture
from Gestures.Palm import PalmGesture
from Gestures.RPinch import RPinchGesture
from Gestures.Ring import RingGesture
from Gestures.V import VGesture
from Gestures.ThumbInPalm import ThumbInPalm
from math_funcs import is_facing_camera

@dataclass
class Container:
    """Is used to store the previous gestures for each hand"""
    left = None
    right = None

    def set(self, hand: str, data):
        if hand.startswith("R"):
            self.right = data
        else:
            self.left = data

    def get(self, hand):
        if hand.startswith('R'):
            return self.right
        else:
            return self.left


class TeleMouse:
    def __init__(self, cam_scaling: float = 0.8):
        self.scaling = cam_scaling
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.85, min_tracking_confidence=0.95)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.set_camera(self.scaling)

        self._controller_thread = None

        self.react_to_gestures = True
        self.gesture: Gesture = None
        self.prev_gestures = Container()
        self.prev_hand_landmarks = Container()

        # Disables gesture processing except for itself
        self.disable_gesture = HornsGesture(False, self.toggle_processing, None, False, 'Right')
        # Presses `f` (fullscreen on websites)
        self.fullscreen_gesture = VGesture(False, actions.fullscreen, None, True, 'Right')
        # Scrolls imitating touchpad scrolling
        self.scroll_gesture = FistGesture(True, actions.scroll, None, False, 'Right')
        # Presses ctrl + tab, then lets you navigate to desired tab. When released - presses it (browsers)
        self.ctrl_tab_gesture = RingGesture(False, actions.press_ctrl_tab, actions.release_ctrl_tab, True, 'Left')
        # Presses alt + tab, then lets you navigate to desired tab. When released - presses it
        self.alt_tab_gesture = RingGesture(False, actions.press_alt_tab, actions.release_alt_tab, True, 'Right')
        # Default gesture that does not do anything
        self.r_default_gesture = PalmGesture(True, None, None, True,'Right')
        self.l_default_gesture = PalmGesture(True, None, None, False,'Left')
        # Presses mouse left button down
        self.l_pinch_gesture = LPinchGesture(False,
                                             lambda: actions.mouse_down(actions.Button.left),
                                             lambda: actions.mouse_up(actions.Button.left),
                                             True,
                                             'Right')
        # Presses mouse right button down
        self.r_pinch_gesture = RPinchGesture(False,
                                             lambda: actions.mouse_down(actions.Button.right),
                                             lambda: actions.mouse_up(actions.Button.right),
                                             True,
                                             'Right')

        self.volume_gesture = FistGesture(True, actions.set_volume, None, False, 'Left')
        self.go_back_gesture = ThumbInPalm(False, actions.go_back, None, True, 'Right')


    def set_camera(self, scale) -> None:
        max_height = 1080
        max_width = 1920
        height = int(max_height * scale)
        width = int(max_width * scale)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        print(f"Camera is set to resolution {width}x{height}")


    def toggle_processing(self) -> None:
        self.react_to_gestures = not self.react_to_gestures


    def set_camera_state(self, state: bool) -> None:
        """Frees the camera"""
        if not state:
            self.cap.release()
            self.cap = None
        else:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.set_camera(self.scaling)


    def recognize_gesture(self, hand_landmarks, handedness) -> Gesture:
        lm = hand_landmarks
        bent_fingers = set()
        for tip, pip in FINGER_TIPS.items():
            if lm.landmark[tip].y > lm.landmark[pip].y:
                bent_fingers.add(tip)

        # The gestures are matched in priority order
        if self.volume_gesture.match(bent_fingers, handedness):
            return self.volume_gesture

        elif self.scroll_gesture.match(bent_fingers, handedness):
            return self.scroll_gesture

        elif self.disable_gesture.match(bent_fingers, handedness):
            return self.disable_gesture

        elif self.alt_tab_gesture.match(bent_fingers, handedness):
            return self.alt_tab_gesture

        elif self.ctrl_tab_gesture.match(bent_fingers, handedness):
            return self.ctrl_tab_gesture

        elif self.l_pinch_gesture.match(hand_landmarks, handedness):
            return self.l_pinch_gesture

        elif self.r_pinch_gesture.match(hand_landmarks, handedness):
            return self.r_pinch_gesture

        elif self.fullscreen_gesture.match(bent_fingers, handedness):
            return self.fullscreen_gesture

        elif self.go_back_gesture.match(bent_fingers, hand_landmarks, handedness):
            return self.go_back_gesture

        else:
            return self.r_default_gesture if handedness == "Right" else self.l_default_gesture


    # Is needed since we don't flip the image
    @staticmethod
    def flip_handedness(handedness):
        return "Right" if handedness == "Left" else "Left"

    def __start_controller(self) -> None:
        while True:
            if self.cap is None:
                time.sleep(1)
                continue

            ret, frame = self.cap.read()
            if not ret or frame is None:
                time.sleep(0.5)
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    handedness = results.multi_handedness[idx].classification[0].label
                    handedness = self.flip_handedness(handedness)
                    if not is_facing_camera(hand_landmarks, handedness):
                        continue

                    self.gesture = self.recognize_gesture(hand_landmarks, handedness)

                    # getting the previous gesture for the needed hand
                    prev_gesture = self.prev_gestures.get(handedness)
                    prev_hand_landmarks = self.prev_hand_landmarks.get(handedness)

                    # Print the gesture if it was changed
                    if self.gesture != prev_gesture:
                        print(self.gesture, handedness)

                    # Checking if the users shows the `disable gesture`
                    if self.gesture == self.disable_gesture != prev_gesture:
                        self.disable_gesture.action()

                    elif self.react_to_gestures:
                        # Prevents one-shot gestures from acting every frame (letting the continuous ones pass)
                        if self.gesture.is_continuous or (self.gesture != prev_gesture):
                            self.gesture.action(prev_hand_landmarks, hand_landmarks)

                        if prev_gesture: # Prevents an error on the first frame
                            if self.gesture != prev_gesture:
                                # It will be checked wheter the gesture has a drop func or not
                                prev_gesture.drop()

                            if self.gesture.allow_mouse_movement:
                                actions.move_mouse(prev_hand_landmarks, hand_landmarks)

                    self.prev_gestures.set(handedness, self.gesture)
                    self.prev_hand_landmarks.set(handedness, hand_landmarks)



    def launch(self):
        if self._controller_thread and self._controller_thread.is_alive():
            print("Tmouse thread is already running")
            return

        self._controller_thread = threading.Thread(target=self.__start_controller)
        self._controller_thread.start()

