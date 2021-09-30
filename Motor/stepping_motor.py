# import
import RPi.GPIO as GPIO
import time

# setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# stepping_class
class Stepping_Moter:
    def __init__(self, coil_0=6, coil_1=13, coil_2=19, coil_3=26):
        # set_pin_num
        self.coil_0 = coil_0
        self.coil_1 = coil_1
        self.coil_2 = coil_2
        self.coil_3 = coil_3
        
        # set_pin
        GPIO.setup(coil_0, GPIO.OUT)
        GPIO.setup(coil_1, GPIO.OUT)
        GPIO.setup(coil_2, GPIO.OUT)
        GPIO.setup(coil_3, GPIO.OUT)

        # set_steps
        self.default_steps = [
            [1,0,0,1],
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1]
        ]
        self.stop_steps = [0, 0, 0, 0]