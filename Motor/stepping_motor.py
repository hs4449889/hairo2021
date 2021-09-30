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

    def move_step(self, steps):
        GPIO.output(self.coil_0, steps[0])
        GPIO.output(self.coil_1, steps[1])
        GPIO.output(self.coil_2, steps[2])
        GPIO.output(self.coil_3, steps[3])
    
    def forward(self, sleep_time, step_time, direction):
        if direction==1:
            for _i in range(step_time):
                for _j in self.default_steps:
                    self.move_step(_j)
                    time.sleep(sleep_time)
        elif direction==0:
            for _i in range(step_time):
                for _j in reversed(self.default_steps):
                    self.move_step(_j)
                    time.sleep(sleep_time)
        self.move_step(self.stop_steps)

# main / 定義
stepping = Stepping_Moter()

while True:
    # mode
    print("time = ")
    sleep = float(input())
    print("dire = ")
    dire  = int(input())
    print("step = ")
    steps = int(input())

    # turning / 回転
    stepping.forward(sleep, steps, dire)