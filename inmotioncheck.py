__author__ = 'matt'

class inMotionCheck(*args, **kwargs):
    # args and kwargs should contain the rooms and lookback or lookforward time to check for motion
    # lookforward won't be supported yet

    def __init__(self):
        # init stuff
        self.inmotion_flag = False
        self.inmotiontimerrunning_flag = false

    def