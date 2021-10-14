# import_original
from Arm import arm_inverse
from Arm import realsense
from Motor import stepping_motor

# import_default
import time
import Adafruit_PCA9685

# setup
servo = Adafruit_PCA9685.PCA9685()

for i in range(150, 650, 1):
    servo.set_pwm(0, 0, i)