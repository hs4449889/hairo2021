from Sensor import sonic
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sonic_sensor1 = sonic.ULTRA_SONIC_SENSOR(trig_pin=17,echo_pin=27)

print("===start===")

while True:
    try:
        distance = sonic_sensor1.Sense_Ultra_Sonic()
        print("distance == " + str(distance))
        time.sleep(1)
    except KeyboardInterrupt:
        print("===finish===")
        break
