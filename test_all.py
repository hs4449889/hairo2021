from Sensor import sonic
from Motor import DC_motor
from timeout_decorator import timeout, TimeoutError
import RPi.GPIO as GPIO
import time
import struct

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# motor
motor1 = DC_motor.DC_MOTOR(pwm_pin = 19,dir_pin = 26)
#motor2 = DC_motor.DC_MOTOR(pwm_pin = 20,dir_pin = 21)  # connect pin

# sensor
sonic1 = sonic.ULTRA_SONIC_SENSOR(17, 27)
#sonic2 = sonic.ULTRA_SONIC_SENSOR(18, 19) # connect

# reading
@timeout(0.02)
def reading():
    data = f.read(8)
    t, value, code, index = struct.unpack("<ihbb", data)
    return t, value, code, index

print("=== start ===")

with open("/dev/input/js0", "rb") as f:
    while True:
        try:
            # reading
            t, value, code, index = reading()

            # Rotation
            if value==1 and code==1 and index==1 and length1 > 20:
                motor1.Rotation(Direction = True, Rotation_Speed = 80)
                print("turning_1")
            else:
                motor1.Rotation(Direction = True, Rotation_Speed = 0)
                
        except TimeoutError:
            # sensing
            length1 = sonic1.Sense_Ultra_Sonic()
            print("length1 = {}".format(length1))
            if length1 < 20:
                motor1.Rotation(Direction = True, Rotation_Speed = 0)
            
        except KeyboardInterrupt:
            motor1.Rotation(0)
            print("===stop===")
            break

GPIO.cleanup()