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
    def __init__(self,
            front_left = dc_motor.DcMotor(pwm_pin = 27, dir_pin = 17),
            front_right = dc_motor.DcMotor(pwm_pin = 14, dir_pin = 15),
            rear_left = dc_motor.DcMotor(pwm_pin = 26, dir_pin = 19),
            rear_right = dc_motor.DcMotor(pwm_pin = 20, dir_pin = 21)):
        
        self.front_left  = front_left
        self.front_right = front_right
        self.rear_left   = rear_left
        self.rear_right  = rear_right

        self.specify_motion = [-1,-1,-1,-1]

    #呼び出している間mecanumを回し続ける
    def mecanum_forward(self):
        if self.specify_motion[0] != -1: self.front_left.rotation(Direction=self.specify_motion[0], Rotation_Speed=80)
        if self.specify_motion[1] != -1: self.front_right.rotation(Direction=self.specify_motion[1], Rotation_Speed=80)
        if self.specify_motion[2] != -1: self.rear_left.rotation(Direction=self.specify_motion[2], Rotation_Speed=80)
        if self.specify_motion[3] != -1: self.rear_right.rotation(Direction=self.specify_motion[3], Rotation_Speed=80)


    def left_translation(self):
    def right_translation(self):
    def up_translation(self):
    def down_translation(self):

    def left_turn(self):
    def right_turn(self):

    def stop(self):








