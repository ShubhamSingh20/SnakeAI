from global_vars import Screen, Segment

class Env(object):
    observation_space = (
        Screen.SCREEN_HEIGTH * Screen.SCREEN_WIDTH / Segment.SEGMENT_HEIGHT * Segment.SEGMENT_WDITH
    )
    action_space = 4 # up, down, left, right