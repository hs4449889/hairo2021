# 本プログラムの思考回路
#   (1) 2点、点A、点B の座標を得る
#   (2) 最初の点から点Aまでのルートを得る
#   (3) 点Aから点Bの直上の点までのルートを得る
#   (4) (2)を使用し、点Aまで移動する
#   (5) (3)を利用し、点Bの直上まで移動する
#   (6) 縦方向にペンの幅分下げる
#   (7) (3)を逆からFor分で回し、反対の動きで点Aの下に戻る
#   (8) 縦方向にペンの幅分下げる
#   (9) (6)~(8)を繰返す
#  (10) 縦方向が点Bのラインに達したとき、
#       A: 横方向が点Aのラインにいるときは何も行わない
#       B: 横方向が点Bのラインにいるときは高さ変更を行わず、点Aのラインに戻る
#  (11) (2)を逆からFor文で回し、反対の動きで初期位置に戻る

# import_original
import arm_inverse
import realsense
from Motor import stepping_motor

# import_default
import time
import math
import numpy as np
import pigpio

# unit
#   angle  = degree
#   lenght = mm

# auto_moving_arm_class
class AutoArm:
    def __init__(self):
        # setting_arms
        self.link_length = [400, 400, 100]
        self.first_angle = [10, 160, -80]

        # setting_"O"rigin_"R"ealsense_vector
        self.OR_VECTOR   = [0, -600, 0]

        # setting_motor
        self.angle_pins  = [14, 15, 16]
        self.stepping_pin= [10, 11, 12, 13]
        self.stepping    = stepping_motor.Stepping_Moter(
            coil_0=self.stepping_pin[0],
            coil_1=self.stepping_pin[1],
            coil_2=self.stepping_pin[2],
            coil_3=self.stepping_pin[3]
        )

        # setting_servo
        self.MIN_PULTH   = 150
        self.MAX_PULTH   = 500
        
        # setting_pen
        self.PEN_WIDTH   = 20
        self.STEP_PER_MM = 16

        # setting_modules
        self.pi     = pigpio.pi()
        self.arm    = arm_inverse.Arms(self.link_length, self.first_angle)

    def deg_to_pulth(self, x):
        return (x+180)*(self.MAX_PULTH-self.MIN_PULTH)/360 + self.MIN_PULTH + self.MIN_PULTH

    def servo_moving(self, pulths):
        for _x, _pulth in enumerate(pulths):
            self.pi.set_servo_pulsewidth(self.angle_pins[_x], _pulth)

    def get_corner(self):
        # setting_realsense
        self.realsense  = realsense.RealSense([1280, 720], 15)
        self.corner_xyz = np.array([self.OR_VECTOR, self.OR_VECTOR])
        _count = 0

        # if_clicked, return_positions
        while _count < 2:
            # take_picture
            self.realsense.get_frame()
            # return_position
            if self.realsense.depth != 0:
                self.corner_xyz[_count][0] += self.realsense.world_point[0] * 1000
                self.corner_xyz[_count][1] += self.realsense.world_point[1] * 1000
                self.corner_xyz[_count][2] += self.realsense.depth * 1000
                print("RealSense_World >>> X: {:5.1f}mm, Y: {:5.1f}mm, Z: {:5.1f}mm".format(
                    self.corner_xyz[_count][0],
                    self.corner_xyz[_count][1],
                    self.corner_xyz[_count][2]
                ))
                _count += 1
        
        # stop_taking_picture
        self.realsense.pipeline.stop()

    def get_draw_route(self):
        # consider_y_axis
        self.area_height = abs(self.corner_xyz[0][1]-self.corner_xyz[1][1])
        self.separate    = math.floor(self.area_height / self.PEN_WIDTH)

        # consider_x_axis(first_route)
        self.arm.setting([self.corner_xyz[0][0], self.corner_xyz[0][2], 90])
        self.arm.moving()
        self.angles_transition_first = self.deg_to_pulth(self.arm.angles_transition)

        # consider_x_axis(normal_route)
        self.arm.setting([self.corner_xyz[1][0], self.corner_xyz[1][2], 90])
        self.arm.moving()
        self.angles_transition_normal = self.deg_to_pulth(self.arm.angles_transition)

    def moving_x_axis(self, sleep, mode):
        # set_route
        if   mode==0:
            self.route_x = self.angles_transition_first
        elif mode==1:
            self.route_x = self.angles_transition_normal
        elif mode==2:
            self.route_x = np.flipud(self.angles_transition_normal)
        elif mode==3:
            self.route_x = np.flipud(self.angles_transition_first)
        
        # calculate_sleep_time
        _sleep = sleep / self.route_x.shape[0]

        # moving
        for _pulth in self.route_x:
            self.servo_moving(_pulth)
            time.sleep(_sleep)

    def moving_y_axis(self, sleep, steps, direction=1):
        # calculate_sleep_time
        _sleep = sleep / (steps*8)
        # moving_step_motor
        self.stepping.forward(_sleep, steps, direction)

    def auto_moving(self):
        # consider_rute
        self.get_corner()
        self.get_draw_route()

        # get_first_position
        self.steps = abs(self.corner_xyz[0][1]) * self.STEP_PER_MM
        self.moving_y_axis(sleep=4, steps=self.steps, direction=0)
        self.moving_x_axis(sleep=4, mode=0)

        # drawing
        for _i in range(self.separate):
            self.moving_x_axis(sleep=8, mode=_i%2+1)
            if _i!=self.separate-1:
                self.moving_y_axis(sleep=0.5, steps=self.PEN_WIDTH*self.STEP_PER_MM)
        
        # return_position_x
        if self.separate%2 != 0:
            self.moving_x_axis(sleep=8, mode=2)
        
        # return_first_position
        self.moving_x_axis(sleep=4, mode=3)
        self.moving_y_axis(sleep=4, steps=abs(self.corner_xyz[1][1]), direction=0)