from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button
from math_funcs import OneEuroFilter
import globals as g
import time

kb = KeyboardController()
mouse = MouseController()

filter_x = OneEuroFilter(min_cutoff=1.0, beta=0.007)
filter_y = OneEuroFilter(min_cutoff=1.0, beta=0.007)

click_lock = False
lock_time = 0


def move_mouse(prev_hand_landmarks, hand_landmarks):
    global click_lock

    if not prev_hand_landmarks:
        return

    if click_lock:
        if time.time() - lock_time > 0.15:
            click_lock = False
        else:
            return

    cursor = hand_landmarks.landmark[9]
    prev_cursor = prev_hand_landmarks.landmark[9]

    delta_x = -(cursor.x - prev_cursor.x) * (g.screen_size[0] + g.offset_x) * g.sensitivity[0]
    delta_y = (cursor.y - prev_cursor.y) * (g.screen_size[1] + g.offset_y) * g.sensitivity[1]

    if abs(delta_x) < g.move_threshold:
        delta_x = 0.0
    if abs(delta_y) < g.move_threshold:
        delta_y = 0.0

    if delta_x == 0.0 and delta_y == 0.0:
        return

    start_x, start_y = mouse.position

    raw_x = start_x + delta_x
    raw_y = start_y + delta_y

    t = time.time()
    smooth_x = filter_x.filter(raw_x, t)
    smooth_y = filter_y.filter(raw_y, t)

    mouse.position = (smooth_x, smooth_y)



def set_volume(prev_hand_landmarks, hand_landmarks):
    if not prev_hand_landmarks:
        return
    cursor = hand_landmarks.landmark[9]
    prev_cursor = prev_hand_landmarks.landmark[9]

    delta_y = (cursor.y - prev_cursor.y) * (g.screen_size[1] + g.offset_y) * g.scroll_sensitivity[1]
    if abs(delta_y) < 5:
        return

    if delta_y < 0:
        __volume_up()
    else:
        __volume_down()

def go_back():
    kb.press(Key.alt)
    kb.press(Key.left)
    kb.release(Key.alt)
    kb.release(Key.left)

def __volume_up():
    kb.press(Key.media_volume_up)
    kb.release(Key.media_volume_up)


def __volume_down():
    kb.press(Key.media_volume_down)
    kb.release(Key.media_volume_down)


def mouse_down(but: Button):
    global click_lock, lock_time
    click_lock = True
    lock_time = time.time()
    mouse.press(but)


def mouse_up(but: Button):
    mouse.release(but)


def press_alt_tab():
    kb.press(Key.alt)
    kb.press(Key.tab)


def release_alt_tab():
    mouse.click(Button.left)
    kb.release(Key.alt)
    kb.release(Key.tab)


def press_ctrl_tab():
    kb.press(Key.ctrl)
    kb.press(Key.tab)
    kb.release(Key.tab)


def release_ctrl_tab():
    mouse.click(Button.left)
    kb.release(Key.ctrl)


def fullscreen():
    kb.press('f')
    kb.release('f')


def scroll(prev_hand_landmarks, hand_landmarks):
    if not prev_hand_landmarks:
        return
    dy = hand_landmarks.landmark[9].y - prev_hand_landmarks.landmark[9].y
    dx = hand_landmarks.landmark[9].x - prev_hand_landmarks.landmark[9].x

    # Filtering noise
    if abs(dy) < 0.009 and abs(dx) < 0.009:
        return

    direction_y = 1 if dy > 0 else -1
    mouse.scroll(0, direction_y * g.scroll_sensitivity[0])

    direction_x = 1 if dx < 0 else -1
    mouse.scroll(direction_x * g.scroll_sensitivity[1], 0)

