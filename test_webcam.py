# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# global variable for functions
kernel = np.ones((5, 5), np.uint8)


# closing - dilation followed by erosion
def closing(image):
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


# Adding custom options for tesseract
custom_config = r'-c tessedit_char_whitelist=0123456789 --oem 3 --psm 7'

# ranges for color detection
# detects darker colors
lower_range = np.array([0, 0, 0])
upper_range = np.array([180, 170, 150])

vc = cv2.VideoCapture(0)

cv2.namedWindow('My webcam', cv2.WINDOW_NORMAL)
cv2.resizeWindow('My webcam', 500, 500)

cv2.namedWindow('Tesseract', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Tesseract', 500, 500)

while True:
    is_capturing, frame = vc.read()
    cv2.imshow("My webcam", frame)

    h, w, c = frame.shape

    # removes the noise (closing)
    blurred = closing(frame)

    # convert to hsv color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # apply a mask to the hsv image
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # apply the mask to the original image
    bitwise = cv2.bitwise_and(frame, frame, mask=mask)

    # convert the image back to bgr color space
    img_to_bgr = cv2.cvtColor(bitwise, cv2.COLOR_HSV2BGR)

    # copy the image so it will be a cleaned image for tesseract
    img = img_to_bgr.copy()

    # split the copied image into boxes
    boxes = pytesseract.image_to_boxes(img, config=custom_config, timeout=0.5)

    # draw each box
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (255, 255, 255), 2)

    # draw the chart containing the image with boxes
    cv2.imshow("Tesseract", img)

    # convert the clean image to string (only numerical characters here)
    img_str = pytesseract.image_to_string(img_to_bgr, config=custom_config, timeout=0.5)

    # removes the useless whitespaces
    img_str = img_str.strip()
    img_str = img_str.replace(" ", "")

    # if no result is found by tesseract, initialize it to 0
    if len(img_str) < 1:
        img_str = "0"

    print('Found: (' + img_str + ')')

    if cv2.waitKey(1) & 0XFF == ord('x'):
        break

# close the already opened camera
vc.release()
# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()
