from Mecanum import mecanum
from Controller import ps4

import struct
def ps4_reading():
    data = f.read(8)
    t , value , code , index = struct.unpack("<ihbb",data)
    return t , value , code , index
    
#デフォ値運用
mecanum = mecanum.MecanumManager()
if __name__ == '__main__':
    with open("/dev/input/js0","rb") as f:
        while True:
            ps4 = ps4.Ps4
            
            if(ps4.leverL_right_pushed):
                print("controller : leverL right pushed")
                mecanum.right_translation()
                mecanum.mecanum_forward()

            elif(ps4.leverL_left_pushed):
                print("controller : leverL left pushed")
                mecanum.left_translation()
                mecanum.mecanum_forward

            elif(ps4.leverL_up_pushed):
                print("controller : leverL up pushed")
                mecanum.up_translation()
                mecanum.mecanum_forward()

            elif(ps4.leverL_down_pushed):
                print("controller : leverL down pushed")
                mecanum.down_translation()
                mecanum.mecanum_forward()


            elif(ps4.leverR_right_pushed):
                print("controller : LeverR right pushed")
                mecanum.right_turn()
                mecanum.mecanum_forward()

            elif(ps4.leverR_left_pushed):
                print("controller : LeverR left pushed")
                mecanum.left_turn()
                mecanum.mecanum_forward()


