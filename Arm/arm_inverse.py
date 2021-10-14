# import
from math import degrees, radians, sin, cos
import numpy as np

class Arms:
    def __init__(self, links, fst_angle, Div=100):
        # Unit of angles are 'Degree'
        # enter array, not ndarray
        self.links = np.array(links)                                    # each_length [len(3)]
        self.fst_angle = self.degree_to_radian(fst_angle, True, True)   # [th1, th2, th3] ==> ndarray(Rads)
        self.div = Div                                                  # consider_times
        self.prints = "time: {:3d}, th1: {:9.1f}, th2: {:9.1f}, th3: {:9.1f}, x: {:9.2f}, y: {:9.2f}, a: {:9.1f}"

    def degree_to_radian(self, _array, Dir, Type):
        # if Deg ==> Rad  : True   # if Rad ==> Deg  : False
        # if Type==> Angle: True   # if Type==> place: False
        # return angle or place array
        if   Dir==True  and  Type==True:
            _changed = np.empty(3)
            for _w, _rad in enumerate(_array): _changed[_w] = radians(_rad)
        elif Dir==False and  Type==True:
            _changed = np.empty(3)
            for _w, _deg in enumerate(_array): _changed[_w] = degrees(_deg)
        elif Dir==True  and  Type==False:
            _changed = np.array(_array)
            _changed[2] = radians(_array[2])
        elif Dir==False and  Type==False:
            _changed = np.array(_array)
            _changed[2] = degrees(_changed[2])
        return _changed

    def rad_to_sum_rad(self, _Rads):
        _array = np.empty(3)
        for _w in range(3):  _array[_w] = sum(_Rads[:_w+1])
        self.sum_angles = _array
    
    def rad_to_place(self, _Rads):
        self.rad_to_sum_rad(_Rads)
        _x = self.links[0]*cos(self.sum_angles[0]) + self.links[1]*cos(self.sum_angles[1]) + self.links[2]*cos(self.sum_angles[2])
        _y = self.links[0]*sin(self.sum_angles[0]) + self.links[1]*sin(self.sum_angles[1]) + self.links[2]*sin(self.sum_angles[2])
        _a = self.sum_angles[2]
        return np.array([_x, _y, _a])

    def setting(self, end_place):
        # goal
        self.end_place = self.degree_to_radian(end_place, True, False)  # [x, y, a] ========> ndarray(Place)
        # first_place
        self.fst_place = self.rad_to_place(self.fst_angle)
        # now_position
        self.place = self.fst_place
        self.angle = self.fst_angle
        # small_change_amount
        self.det = self.end_place - self.fst_place
        self.sca = self.det / self.div

    def moving(self):
        # angles_transition (to return)
        self.angles_transition = []

        for D in range(1, self.div+1, 1):
            # target_rads
            target = self.fst_place + self.sca*D
            change_amount = target - self.place

            # Yakobi
            J = np.zeros((3, 3))
            J[0][0] = -self.links[0] * sin(self.sum_angles[0]) -self.links[1] * sin(self.sum_angles[1]) -self.links[2] * sin(self.sum_angles[2])
            J[0][1] = -self.links[1] * sin(self.sum_angles[1]) -self.links[2] * sin(self.sum_angles[2])
            J[0][2] = -self.links[2] * sin(self.sum_angles[2])
            J[1][0] =  self.links[0] * cos(self.sum_angles[0]) +self.links[1] * cos(self.sum_angles[1]) +self.links[2] * cos(self.sum_angles[2])
            J[1][1] =  self.links[1] * cos(self.sum_angles[1]) +self.links[2] * cos(self.sum_angles[2])
            J[1][2] =  self.links[2] * cos(self.sum_angles[2])
            J[2][0] =  1
            J[2][1] =  1
            J[2][2] =  1
            
            # inverse_and_make_angle
            inv_J = np.linalg.inv(J)
            det_angle = inv_J @ change_amount
            
            self.angle += det_angle
            self.rad_to_sum_rad(self.angle)

            # now_place
            self.place = self.rad_to_place(self.angle)

            # print(move)
            _degs = self.degree_to_radian(self.angle, False, True)
            _posi = self.degree_to_radian(self.place, False, False)

            # array
            self.angles_transition.append(_degs)

            # print
            print(self.prints.format(D, _degs[0], _degs[1], _degs[2],  _posi[0], _posi[1], _posi[2]))
        
        # first_setting
        self.fst_angle = self.angle

        # make_numpy_array
        self.angles_transition = np.array(self.angles_transition)



"""
############################################################# test #############################################################

# link_setting
# args = [ アームの長さ[leg1, leg2, leg3], 各関節の角度(初期値)[theta1, theta2, theta3], 分割回数]
#   ※アームの長さ、関節の角度は、支点に近い方から列挙する。
#   ※分割回数は細かいほど正確に動く(はず)
arms = Arms([400, 400, 100], [10, 160, -80], 32)

# 動きの流れ
#   (1)初期値設定：アームの形と初めの位置がわかる
#   (2)目的地設定：逆運動学で動く量を計算
#   (3)デバッグ　：次の移動で動くべき角度が出力される(_degs_180がその時点での角度)
#   (4)現在地更新：移動が終わると、現在地が移動後の位置に更新される
#   (5)再度目的地入力：もう一度目的地を入力すると、(4)の位置からの移動量が計算される



while True:
    # 目的地(X方向)
    print('x')
    x = float(input())
    
    # 目的地(Y方向)
    print('y')
    y = float(input())

    # 目的地(手先角度)
    print('a')
    a = float(input())

    # 目的地設定 ( .Setting('args'))
    # args = 目的地情報[x座標, y座標, 手先角度]
    arms.setting([x, y, a])

    # 計算を実行( .Moving()) ※引数はなし
    arms.moving()

    print(arms.angles_transition)
"""