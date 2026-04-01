import math

class OneEuroFilter:
    def __init__(self, min_cutoff=1, beta=0.015, d_cutoff=1.0):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_prev = None
        self.dx_prev = 0.0
        self.t_prev = None

    def alpha(self, cutoff, dt):
        tau = 1.0 / (2 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / dt)

    def filter(self, x, t):
        if self.t_prev is None:
            self.t_prev = t
            self.x_prev = x
            return x

        dt = t - self.t_prev
        if dt <= 0:
            return x

        # derivative
        dx = (x - self.x_prev) / dt
        a_d = self.alpha(self.d_cutoff, dt)
        dx_hat = a_d * dx + (1 - a_d) * self.dx_prev

        # adaptive cutoff
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = self.alpha(cutoff, dt)
        x_hat = a * x + (1 - a) * self.x_prev

        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t

        return x_hat

    def reset(self):
        self.x_prev = None
        self.dx_prev = 0.0
        self.t_prev = None



def is_facing_camera(hand_landmarks, hand: str, max_angle_deg: float = 40) -> bool:
    wrist = (hand_landmarks.landmark[0].x,
             hand_landmarks.landmark[0].y,
             hand_landmarks.landmark[0].z)

    middle_mcp = (hand_landmarks.landmark[9].x,
                  hand_landmarks.landmark[9].y,
                  hand_landmarks.landmark[9].z)

    pinky_mcp = (hand_landmarks.landmark[17].x,
                 hand_landmarks.landmark[17].y,
                 hand_landmarks.landmark[17].z)

    v1 = (middle_mcp[0] - wrist[0],
          middle_mcp[1] - wrist[1],
          middle_mcp[2] - wrist[2])

    v2 = (pinky_mcp[0] - wrist[0],
          pinky_mcp[1] - wrist[1],
          pinky_mcp[2] - wrist[2])

    normal = (v1[1]*v2[2] - v1[2]*v2[1],
              v1[2]*v2[0] - v1[0]*v2[2],
              v1[0]*v2[1] - v1[1]*v2[0])

    dot = normal[2] * -1  # scalar with (0,0,-1)
    norm_n = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)

    if norm_n == 0:
        return False

    cos_angle = dot / norm_n
    cos_angle = max(-1.0, min(1.0, cos_angle))  # clamp

    angle = math.degrees(math.acos(cos_angle))

    # Flip the angle for the left hand
    if hand == "Left":
        angle = 180 - angle
    return angle < max_angle_deg
