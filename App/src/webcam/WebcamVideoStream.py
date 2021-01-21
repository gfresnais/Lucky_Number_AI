# -*- coding: utf-8 -*-

"""
@author: Gallien FRESNAIS
"""

from threading import Thread
import cv2
import numpy as np


"""
Uses OpenCV to capture a camera video stream
"""

class WebcamVideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        # sets the width and height of the stream
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # reads the video stream to get the first frame
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        # variable for image processing methods
        self.kernel = np.ones((5, 5), np.uint8)
        # ranges for color detection
        # detects darker colors
        self.lower_range = np.array([0, 0, 0])
        self.upper_range = np.array([180, 170, 150])

    def start(self):
        # starts a new thread for capturing the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

    # closing - dilation followed by erosion
    def closing(self, image):
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, self.kernel)

    # applies a mask to the captured frame
    def mask_frame(self):
        # removes the noise (closing)
        blurred = self.closing(self.frame)

        # convert to hsv color space
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # apply a mask to the hsv image
        mask = cv2.inRange(hsv, self.lower_range, self.upper_range)

        # apply the mask to the original image
        bitwise = cv2.bitwise_and(self.frame, self.frame, mask=mask)

        # convert the image back to bgr color space
        return cv2.cvtColor(bitwise, cv2.COLOR_HSV2BGR)

