# import
import arm_inverse
import realsense
import struct
import math
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

        # must_adjust
        self.PEN_WIDTH  = 20

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

    def get_draw_route(self):
        # consider_y_axis
        area_height = abs(self.corner_xyz[0][1] - self.corner_xyz[1][1])
        self.steps  = math.floor(area_height / self.PEN_WIDTH)

        # consider_x_axis(first_route)
        self.arm.Setting([self.corner_xyz[0][0], self.corner_xyz[0][2]])
        self.arm.Moving()
        self.angles_transition_first = self.arm.angles_transition.T

        # consider_x_axis(normal_route)
        self.arm.Setting([self.corner_xyz[1][0], self.corner_xyz[1][2]])
        self.arm.Moving()
        self.angles_transition_normal =  self.arm.angles_transition.T