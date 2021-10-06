from Motor import dc_motor
class MecanumManager(object):
    """
    メカナムホイールを制御するためのclass
    ・メカナムに割り振られているタイヤを呼び出されているときに回す関数
    ・メカナムの動作を変更する関数
    ・メカナム用clen up関数

    mecna

    Parameters
    ------------------


    """
    #// to do //配列にまとめるかどうか相談
    #最終的に辞書を採用(配列は可読性が低い)
    def __init__(self,
            front_left  = {"pwm_pin":1,"dir_pin":1},
            front_right = {"pwm_pin":1,"dir_pin":1},
            rear_left   = {"pwm_pin":1,"dir_pin":1},
            rear_right  = {"pwm_pin":1,"dir_pin":1} ):
        
        self.front_left  = dc_motor.DcMotor(pwm_pin = front_left["pwm_pin"],dir_pin= front_left["dir_pin"])
        self.front_right = dc_motor.DcMotor(pwm_pin = front_right["pwm_pin"],dir_pin= front_right["dir_pin"])
        self.rear_left   = dc_motor.DcMotor(pwm_pin = rear_left["pwm_pin"],dir_pin= rear_left["dir_pin"])
        self.rear_right  = dc_motor.DcMotor(pwm_pin = rear_right["pwm_pin"],dir_pin= rear_right["dir_pin"])

        self.specify_motion = [-1,-1,-1,-1]

    #呼び出している間mecanumを回し続ける
    def mecanum_forward(self):
        if self.specify_motion[0] != -1: self.front_left.rotation(Direction=self.specify_motion[0], Rotation_Speed=80)
        if self.specify_motion[1] != -1: self.front_right.rotation(Direction=self.specify_motion[1], Rotation_Speed=80)
        if self.specify_motion[2] != -1: self.rear_left.rotation(Direction=self.specify_motion[2], Rotation_Speed=80)
        if self.specify_motion[3] != -1: self.rear_right.rotation(Direction=self.specify_motion[3], Rotation_Speed=80)

    def mecanum_stop(self):
        if self.specify_motion[0] == -1: self.front_left.rotation(Direction=self.specify_motion[0], Rotation_Speed=0)
        if self.specify_motion[1] == -1: self.front_right.rotation(Direction=self.specify_motion[1], Rotation_Speed=0)
        if self.specify_motion[2] == -1: self.rear_left.rotation(Direction=self.specify_motion[2], Rotation_Speed=0)
        if self.specify_motion[3] == -1: self.rear_right.rotation(Direction=self.specify_motion[3], Rotation_Speed=0)


    #値設定は後回しで
    def left_translation(self):
        self.specify_motion[,,,]

    def right_translation(self):
        self.specify_motion[,,,]

    def up_translation(self):
        self.specify_motion[,,,]

    def down_translation(self):
        self.specify_motion[,,,]


    def left_turn(self):
        self.specify_motion[,,,]

    def right_turn(self):
        self.specify_motion[,,,]

    def stop(self):
        self.specify_motion[-1,-1,-1,-1]








