# PWM Motor class
import RPi.GPIO as GPIO
import time 

class DcMotor:
    """
    DCモーターを使用するためのclass
    pwm制御用のpinやdirction用のpin番号(BCM)を保持する

    Parameters
    ----------
    pwm_pin : int
        モータードライバのpwm制御用pin
    
    dir_pin : int
        モータードライバのdirection制御用のpin
    """
    def __init__(self,pwm_pin = 19,dir_pin = 26):
        
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin

        #pwm set up
        GPIO.setup(self.pwm_pin,GPIO.OUT)
        self.pwm_pin = GPIO.PWM(self.pwm_pin,100)
        self.pwm_pin.start(0)

        #direction set up
        GPIO.setup(self.dir_pin,GPIO.OUT)
        GPIO.output(self.dir_pin,True)
        
    def rotation(self,Direction = True,Rotation_Speed = 100):
        """
        DCモーターを回転させるための関数

        Parameters
        ----------
        direction : int
            方向を保持する変数(True = 正回転、False = 負の回転)

        rotation_speed : int
            ChangeDutyCycleの値を保持する変数(0 ~ 100)
        """
        GPIO.output(self.dir_pin,Direction)
        self.pwm_pin.ChangeDutyCycle(Rotation_Speed)
        
    def finish(self):
        """
        pwm制御を停止するための関数

        Parameters
        ----------
        
        None
        """
        self.pwm_pin.stop()
