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






