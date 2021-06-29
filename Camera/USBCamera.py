#USBCamera library
import cv2
class UsbCameraDevice:
    def __init__(self,DeviceId = 0):
        self.DeviceId = DeviceId
    def preview(self):
        capture = cv2.VideoCapture(0)
        if capture.isOpened() is False:
            raise IOError
        ret,frame = capture.read()
        if ret is False:
            raise IOError
        cv2.imshow('frame',frame)
        #can key input 1 seconds
        cv2.waitkey(1)
    

"""
camera1 = USBCameraDevice(0)
camera1.preview()
"""