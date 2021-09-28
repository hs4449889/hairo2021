# PWM Motor class
import RPi.GPIO as GPIO
import time 

class DcMotor:
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
        
    def Rotation(self,Direction = True,Rotation_Speed = 100):
        GPIO.output(self.dir_pin,Direction)
        self.pwm_pin.ChangeDutyCycle(Rotation_Speed)
        
    def finish(self):
        self.pwm_pin.stop()
