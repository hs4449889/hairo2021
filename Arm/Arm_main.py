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

# import
import arm_inverse
import realsense
import struct
import math
import time
import numpy as np
import pigpio
from timeout_decorator import timeout, TimeoutError

# unit
#   angle  = degree
#   lenght = mm

# auto_moving_arm_class
class AutoArm:
    def __init__(self):
        # settings
        self.pi         = pigpio.pi()
        self.arm        = arm_inverse.ARMS([400, 400, 100], [10, 160, -80])
        self.corner_xyz = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

        # arm_pins
        self.angle_pin1 = 14
        self.angle_pin2 = 15
        self.angle_pin3 = 16

        # must_adjust_Servo
        self.PEN_WIDTH  = 20
        self.MAX_PULTH  = 2500
        self.MIN_PULTH  = 500

        # must_adjust_Stepping
        self.STEP_MM    = 16    # N_steps is needed to move 1mm.

    def deg_to_pulth(self, x):
        _pulths = (x+180)*(MAX-MIN)/360
        return _pulths

    def servo_moving(self, pulth):
        # pulth = [theta1_pulth, theta2_pulth, theta3_pulth]
        self.pi.set_servo_pulthwidth(self.angle_pin1, pulth[0])
        self.pi.set_servo_pulthwidth(self.angle_pin2, pulth[1])
        self.pi.set_servo_pulthwidth(self.angle_pin2, pulth[2])

    def stepping_moving(self, pulth):
        # test
        print('a')

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
        self.angles_transition_first = self.deg_to_pulth(self.arm.angles_transition)

        # consider_x_axis(normal_route)
        self.arm.Setting([self.corner_xyz[1][0], self.corner_xyz[1][2]])
        self.arm.Moving()
        self.angles_transition_normal =  self.deg_to_pulth(self.arm.angles_transition)

    def select_route_x(self, mode, direction=-1):
        # mode       : fisrt_move = 0 / normal_mode = 1 / end_mode = 2
        # direction  : left = 1       / right = 0

        # set_route
        if   mode==0:
            self.next_route = self.angles_transition_first
        elif mode==2:
            self.next_route = np.flipud(self.angles_transition_first)
        elif direction==1:
            self.next_route = self.angles_transition_normal
        else:
            self.next_route = np.flipud(self.angles_transition_normal)

    def moving_x_axis(self, sleep=16):
        sleep = sleep / self.next_route.shape[0]
        for _i in self.next_route:
            self.servo_moving(_i)
            time.sleep(sleep)

    def moving_y_axis(self, sleep=0.5):
        self.stepping_moving()

    def auto_moving(self):
        # consider_route
        self.get_corner()
        self.get_draw_route()

        # get_first_position
        self.moving_y_axis(4)
        self.select_route_x(0)
        self.moving_x_axis(8)
        
        # drawing
        for _i in range(self.steps):
            self.select_route_x(1, _i%2)
            self.moving_x_axis()
            if _i!=self.steps-1:
                self.moving_y_axis()
        
        # return_position_x
        if self.steps%2!=0:
            self.select_route_x(1, _i%2)
            self.moving_x_axis()
        
        # return_first_position
        self.select_route_x(2)
        self.moving_x_axis(8)
        self.moving_y_axis(4)