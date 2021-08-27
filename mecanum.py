from Sensor import sonic
from Motor import DC_motor
from timeout_decorator import timeout, TimeoutError
import RPi.GPIO as GPIO
import time
import struct
import math

# GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# motor
FL = DC_motor.DC_MOTOR(pwm_pin = 27, dir_pin = 17)
FR = DC_motor.DC_MOTOR(pwm_pin = 14, dir_pin = 15)
RL = DC_motor.DC_MOTOR(pwm_pin = 26, dir_pin = 19)
RR = DC_motor.DC_MOTOR(pwm_pin = 20, dir_pin = 21)

# sonic
sensor = sonic.ULTRA_SONIC_SENSOR(16, 18)

# set_num
t, value, code, index = 0, 0, 0, 0
i0, i1, i3, i4 = 0, 0, 0, 0
mecanum = [-1, -1, -1, -1]    # FL, FR, RL, RR
count = 0
lock = 0
unlc = 0

@timeout(0.02)
def reading():
    data = f.read(8)
    t, value, code, index = struct.unpack("<ihbb", data)
    return t, value, code, index

# moving_mecanum
def Mecanum_forward():
    # forward
    if mecanum[0] != -1: FL.Rotation(Direction=mecanum[0], Rotation_Speed=80)
    if mecanum[1] != -1: FR.Rotation(Direction=mecanum[1], Rotation_Speed=80)
    if mecanum[2] != -1: RL.Rotation(Direction=mecanum[2], Rotation_Speed=80)
    if mecanum[3] != -1: RR.Rotation(Direction=mecanum[3], Rotation_Speed=80)
    # stop
    if mecanum[0] == -1: FL.Rotation(Direction=mecanum[0], Rotation_Speed=0)
    if mecanum[1] == -1: FR.Rotation(Direction=mecanum[1], Rotation_Speed=0)
    if mecanum[2] == -1: RL.Rotation(Direction=mecanum[2], Rotation_Speed=0)
    if mecanum[3] == -1: RR.Rotation(Direction=mecanum[3], Rotation_Speed=0)

# Mecanum
def Mecanum():
    global mecanum
    if lock==1 and unlc==0:
        # lock
        print("{:6d}_short_length".format(count))
        mecanum = [-1, -1, -1, -1]

    elif i3 == -32767 and abs(i4)<6000:
        # left
        print("{:6d}_{:3d}".format(count, 180))
        mecanum = [0, 1, 1, 0]
    elif i3 == 32767 and abs(i4)<6000:
        # right
        print("{:6d}_{:3d}".format(count, 0))
        mecanum = [1, 0, 0, 1]
    elif i4 == -32767 and abs(i3)<6000:
        # flont
        print("{:6d}_{:3d}".format(count, 90))
        mecanum = [1, 1, 1, 1]
    elif i4 == 32767 and abs(i3)<6000:
        # back
        print("{:6d}_{:3d}".format(count, 270))
        mecanum = [0, 0, 0, 0]
    
    elif i3<0 and i4<0 and math.sqrt(i3**2+i4**2)>30000:
        # flont_left
        print("{:6d}_{:3d}".format(count, 135))
        mecanum = [-1, 1, 1, -1]
    elif i3>0 and i4>0 and math.sqrt(i3**2+i4**2)>30000:
        # back_right
        print("{:6d}_{:3d}".format(count, 315))
        mecanum = [-1, 0, 0, -1]
    elif i3<0 and i4>0 and math.sqrt(i3**2+i4**2)>30000:
        # back_left
        print("{:6d}_{:3d}".format(count, 225))
        mecanum = [0, -1, -1, 0]
    elif i3>0 and i4<0 and math.sqrt(i3**2+i4**2)>30000:
        # front_right
        print("{:6d}_{:3d}".format(count, 45))
        mecanum = [1, -1, -1, 1]

    elif i0<0 and i1<0 and math.sqrt(i0**2+i1**2)>30000:
        # flont_left
        print("{:6d}_{:3d}".format(count, 135))
        mecanum = [-1, 1, -1, 1]
    elif i0>0 and i1>0 and math.sqrt(i0**2+i1**2)>30000:
        # back_right
        print("{:6d}_{:3d}".format(count, 315))
        mecanum = [1, 0, 1, 0]
    elif i0<0 and i1>0 and math.sqrt(i0**2+i1**2)>30000:
        # back_left
        print("{:6d}_{:3d}".format(count, 225))
        mecanum = [0, 1, 0, 1]
    elif i0>0 and i1<0 and math.sqrt(i0**2+i1**2)>30000:
        # front_right
        print("{:6d}_{:3d}".format(count, 45))
        mecanum = [1, -1, 1, -1]
    
    else:
        # stop
        print("{:6d}_Stp".format(count))
        mecanum = [-1, -1, -1, -1]
    
    Mecanum_forward()

# main
with open("/dev/input/js0", "rb") as f:
    while True:
        try:
            # value_save
            t_, value_, code_, index_ = t, value, code, index
            # reading
            t, value, code, index = reading()
        except TimeoutError:
            pass
        except KeyboardInterrupt:
            # stop_all
            print("===stop===")
            break
        finally:
            # sensing
            length = seosor.Sense_Ultra_Sonic()

            # lock
            if length < 15:                         lock = 1
            elif lock==0 and unlc==1 and length>18: unlc = 0
            else:                                   lock = 0
            
            # unlock
            if (value_==1 and code_==1 and value==1 and code==1) and ((index_==8 and index==9) or (index_==9 and index==8)):
                unlc = 1
                print("unlocked")

            # foward
            if   index==0 and code==2: i0 = value
            elif index==1 and code==2: i1 = value
            elif index==3 and code==2: i3 = value
            elif index==4 and code==2: i4 = value
            count += 1
            Mecanum()