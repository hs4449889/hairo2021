# import
import arm_inverse
import realsense
import struct
from timeout_decorator import timeout, TimeoutError

# unit
#   angle  = degree
#   lenght = mm

# auto_moving_arm_class
class AutoArm:
    def __init__(self):
        # settings
        self.arm        = arm_inverse.ARMS([400, 400, 100], [10, 160, -80])
        self.corner_xyz = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    
    def get_corner(self):
        self.realsense  = realsense.REALSENSE([1280, 720], 15)
        _count = 0
        while _count<2:
            # take_pictures
            self.realsense.Get_Frame()
            # if_clicked, return_positions
            if realsense.depth != 0:
                self.corner_xyz[_count][0] = realsense.world_point[0] * 1000
                self.corner_xyz[_count][1] = realsense.world_point[1] * 1000
                self.corner_xyz[_count][2] = realsense.depth * 1000
                count += 1
        self.realsense.pipeline.stop()