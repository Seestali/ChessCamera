from picamery.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

class Camera:



# initialize PiCamera and grab reference
camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

camera.capture(rawCapture, format="rgb")
image = rawCapture.array