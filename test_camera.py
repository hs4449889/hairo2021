from Camera import USBCamera as USB
import cv2

camera1 = USB.USB_CAMERA_DEVICE(DeviceId=-1,window_name='test')

while True:
    try:
        camera1.preview()
    except KeyboardInterrupt:
        print("===stop===")
        break
