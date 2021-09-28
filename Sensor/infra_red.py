import RPi.GPIO as GPIO
#INFRA RED class 
class InfraRedSensor:
    #GPIO pin setup
    def __init__(self,sense_pin = 14):
        self.sense_pin = sense_pin
        GPIO.setup(self.sense_pin,GPIO.IN)

    #Sensor sense return True/False
    def sense_infra_red(self):
        judg = True
        if(GPIO.input(self.sense_pin) != GPIO.LOW):
            print("Not Sense Infra Red Sensor")
            judg = False
        return judg



