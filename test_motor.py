from Motor import DC_motor
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor1 = DC_motor.DC_MOTOR(pwm_pin = 19,dir_pin = 26)
print("===start===")
while True:
        try:
            motor1.Rotation(Direction = True,Rotation_Speed = 100)
        except KeyboardInterrupt:
            motor1.Rotation(Rotation_Speed=0)
            #motor1.finish()
            print("===stop ===")
            break

GPIO.cleanup()