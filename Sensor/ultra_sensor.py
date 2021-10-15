#URTRA SONIC class
import Jetson.GPIO as GPIO
import time

class UltraSonicSensor:
    """
    超音波センサーのsenseのpin番号とreadのpin番号を保持するクラス

    間違ってるかもしれない...
    Parameters
    ----------
    sense_pin : int
        trig(trigger)用のpin番号を保持する    

    read_pin :
        echo用のpin番号を保持する

    """
    def __init__(self,sense_pin = 17,read_pin = 27):
        self.sense_pin = sense_pin
        self.read_pin = read_pin
        
    def sense_urtra_sonic(self):
        """
        センサーからの値を読み取る関数

        Returns
        -------
        distance : float
            読み取った距離を保持する変数
        """
        GPIO.output(self.sense_pin,GPIO.LOW)

        time.sleep(0.3)
        GPIO.output(self.sense_pin,True)
        time.sleep(0.00001)
        GPIO.output(self.sense_pin,False)

        while GPIO.input(self.read_pin) == 0:
            signal_off = time.time()
        while GPIO.input(self.read_pin) == 1:
            signal_on = time.time()
            time_passed = signal_on - signal_off

        distance = 34000 * time_passed / 2
        return distance 



