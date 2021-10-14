class Ps4:
    """
    Ps4のボタンが押されてるかどうか？を判定する(現状)

    if(ps4.function):
        #押されてたら実行
    
    ボタンの関数に関してはそのボタンが押されていればTrueを返す
    (もっといい既存のライブラリ無いかな~~)
    
    注意：上記の理由により説明を省略する
    """
    def __init__(self,index,code,value,):
        self.botton_index = index 
        self.botton_code = code
        self.botton_value = value
    

    def batu_button_pushed(self):
        judg = False
        if self.botton_value == 1 and self.botton_code == 1 and self.botton_index == 0 :
            judg = True
        return judg

    def maru_button_pushed(self):
        
        judg = False
        if self.botton_value == 1 and self.botton_code == 1 and self.botton_index == 1 :
            judg = True
        return judg

    def sankaku_button_pushed(self):
        judg = False
        if self.botton_value == 1 and self.botton_code == 1 and self.botton_index == 2 :
            judg = True
        return judg


    def shikaku_button_pushed(self):
        judg = False
        if self.botton_value == 1 and self.botton_code == 1 and self.botton_index == 3:
            judg = True
        return judg



    def right_button_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 6 :
            judg = True
        return judg


    def left_button_pushed(self):
        judg = False
        if self.botton_value == -32767 and self.botton_code == 2 and self.botton_index == 6 :
            judg = True
        return judg

    def down_button_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 7 :
            judg = True
        return judg

    def up_button_pushed(self):
        judg = False
        if self.botton_value == -32767 and self.botton_code == 2 and self.botton_index == 7 :
            judg = True
        return judg



    def R1_button_pushed(self):
        judg = False
        if self.botton_value == 1 and self.botton_code == 1 and self.botton_index == 5 :
            judg = True
        return judg


    def L1_button_pushed(self):
        judg = False
        if self.botton_value == 1 and self.botton_code == 1 and self.botton_index == 4 :
            judg = True
        return judg



    def share_button_pushed(self):
        judg = False
        if self.botton_value == 1 and self.botton_code == 1 and self.botton_index == 8 :
            judg = True
        return judg

    def options_button_pushed(self):
        judg = False
        if self.botton_value == 1 and self.botton_code == 1 and self.botton_index == 9 :
            judg = True
        return judg

    def home_button_pushed(self):
        judg = False
        if self.botton_value == 1 and self.botton_code == 1 and self.botton_index == 10 :
            judg = True
        return judg

    #値が正確にわからないので一旦保留
    """    
    def leverL_button_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 6 :
            judg = True
        return judg

    def leverR_button_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 6 :
            judg = True
        return judg
    """


    def leverL_right_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 1 :
            judg = True
        return judg

    def leverL_left_pushed(self):
        judg = False
        if self.botton_value == -32767 and self.botton_code == 2 and self.botton_index == 0 :
            judg = True
        return judg
  
    def leverL_up_pushed(self):
        judg = False
        if self.botton_value == -32767 and self.botton_code == 2 and self.botton_index == 1 :
            judg = True
        return judg

    #ここ0でいいんだよな?
    def leverL_down_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 0 :
            judg = True
        return judg
  

    def leverR_right_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 4 :
            judg = True
        return judg

    def leverR_left_pushed(self):
        judg = False
        if self.botton_value == -32767 and self.botton_code == 2 and self.botton_index == 3 :
            judg = True
        return judg
  
    def leverR_up_pushed(self):
        judg = False
        if self.botton_value == -32767 and self.botton_code == 2 and self.botton_index == 4 :
            judg = True
        return judg
        
    def leverR_down_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 3:
            judg = True
        return judg
  
    
    
    #R2,L2
    def R2_button_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 2:
            judg = True
        return judg
  

    def L2_button_pushed(self):
        judg = False
        if self.botton_value == 32767 and self.botton_code == 2 and self.botton_index == 5:
            judg = True
        return judg


#test
import struct
def ps4_reading():
    data = f.read(8)
    t , value , code , index = struct.unpack("<ihbb",data)
    return t , value , code , index
    
def ps4_test():
    with open("/dev/input/js0","rb") as f:
        while True:
            t, value , code , index = ps4_reading()
            ps4 = Ps4(t,value,code,index)
            if(ps4.maru_button_pushed):
                print("controller : maru button pushed")

            elif(ps4.batu_button_pushed):
                print("controller : batu button pushed")

            elif(ps4.sankaku_button_pushed):
                print("controller : sankaku button pushed")

            elif(ps4.shikaku_button_pushed):
                print("controller : shikaku button pushed")

            elif(ps4.maru_button_pushed):
                print("controller : maru button pushed")

            #全部作るのくっそだるいなこれ
            elif(ps4.left_button_pushed):
                print("controller : left button pushed")

            elif(ps4.right_button_pushed):
                print("controller : right button pushed")
            
            elif(ps4.up_button_pushed):
                print("controller : up button pushed")

            elif(ps4.down_button_pushed):
                print("controller : down button pushed")


            elif(ps4.R1_button_pushed):
                print("controller : R1 button pushed")

            elif(ps4.L1_button_pushed):
                print("controller : L1 button pushed")


            elif(ps4.share_button_pushed):
                print("controller : share button pushed")

            elif(ps4.options_button_pushed):
                print("controller : options button pushed")

            elif(ps4.home_button_pushed):
                print("controller : home button pushed")


            elif(ps4.leverL_right_pushed):
                print("controller : leverL right pushed")

            elif(ps4.leverL_left_pushed):
                print("controller : leverL left pushed")

            elif(ps4.leverL_up_pushed):
                print("controller : leverL up pushed")

            elif(ps4.leverL_down_pushed):
                print("controller : leverL down pushed")


            elif(ps4.leverR_right_pushed):
                print("controller : LeverR right pushed")

            elif(ps4.leverR_left_pushed):
                print("controller : LeverR left pushed")

            elif(ps4.leverR_up_pushed):
                print("controller : LeverR up pushed")

            elif(ps4.leverR_down_pushed):
                print("controller : LeverR down pushed")


            elif(ps4.L2_button_pushed):
                print("controller : L2 button pushed")

            elif(ps4.R2_button_pushed):
                print("controller : R2 button pushed")
            
            else:
                print("controller : waiting")

            """
            elif(ps4.leverL_button_pushed):
                print("controller : maru button pushed")

            elif(ps4.leverR_button_pushed):
                print("controller : maru button pushed")
            """
            









