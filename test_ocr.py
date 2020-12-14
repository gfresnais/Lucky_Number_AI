# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pytesseract

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 


# main
image = cv2.imread('./images/1/jaune.PNG')
#cv2.imshow('image', image)
#cv2.waitKey(0)

gray = get_grayscale(image)
#cv2.imshow('gray', gray)
#cv2.waitKey(0)

thresh = thresholding(gray)
#cv2.imshow('thresh', thresh)
#cv2.waitKey(0)

opening = opening(gray)
#cv2.imshow('opening', opening)
#cv2.waitKey(0)

canny = canny(gray)
#cv2.imshow('canny', canny)
#cv2.waitKey(0)


# Adding custom options for tesseract
custom_config = r'--oem 3 --psm 13'

# split the characters with boxes
h, w, c = image.shape
boxes = pytesseract.image_to_boxes(image, config=custom_config)
img = image
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

cv2.imshow('test', img)
cv2.waitKey(0)

# destroy all opened windows created by opencv
cv2.destroyAllWindows()

img_str = pytesseract.image_to_string(image, config=custom_config)
print(img_str)