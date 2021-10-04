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
        self.MIN_PULTH   = 500
        self.MAX_PULTH   = 2500
        
        # setting_pen
        self.PEN_WIDTH   = 20
        self.STEP_PER_MM = 16

        # setting_modules
        self.pi     = pigpio.pi()
        self.arm    = arm_inverse.Arms(self.link_length, self.first_angle)

    def deg_to_pulth(self, x):
        _pulths = (x+180)*(MAX-MIN)/360
        return _pulths

    def servo_moving(self, pulth):
        # pulth = [theta1_pulth, theta2_pulth, theta3_pulth]
        self.pi.set_servo_pulthwidth(self.angle_pin1, pulth[0])
        self.pi.set_servo_pulthwidth(self.angle_pin2, pulth[1])
        self.pi.set_servo_pulthwidth(self.angle_pin2, pulth[2])

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

    def moving_y_axis(self, sleep, steps, direction=-1):
        # calcurate_sleep_time
        sleep = sleep / (steps * 8)
        # consider_direction / steps < 0 === up(1) / steps > 0 === down(0)
        if direction == -1:
            if steps > 0:   direction = 0
            else:           direction = 1
        self.stepping.forward(0.001, steps, direction)

    def auto_moving(self):
        # consider_route
        self.get_corner()
        self.get_draw_route()

        # get_first_position
        stepping = (self.corner_xyz[0][1]-self.default_y)*self.STEP_MM
        self.moving_y_axis(sleep=4, steps=stepping)
        self.select_route_x(0)
        self.moving_x_axis(8)
        
        # drawing
        for _i in range(self.steps):
            self.select_route_x(1, _i%2)
            self.moving_x_axis()
            if _i!=self.steps-1:
                self.moving_y_axis(sleep=0.5, steps=self.ONE_PART, direction=1)
        
        # return_position_x
        if self.steps%2!=0:
            self.select_route_x(1, 1)
            self.moving_x_axis()
        
        # return_first_position
        stepping = (self.corner_xyz[0][1] - self.default_y + (self.steps-1)*self.PEN_WIDTH) * self.STEP_MM
        self.select_route_x(2)
        self.moving_x_axis(8)
        self.moving_y_axis(sleep=4, steps=stepping)