import ctypes # to get the screen resolution

def get_screen_size():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

FINGER_TIPS = {
        8: 6,    # index
        12: 10,  # middle
        16: 14,  # ring
        20: 18   # pinky
    }

screen_size = get_screen_size()
offset_y = screen_size[1] // 3 # to move the mouse lower, so you don't have to raise ur hand too high
offset_x = 0 #screen_size[0] // 3
sensitivity = [2, 2]
scroll_sensitivity = [2, 1]
move_threshold = 1