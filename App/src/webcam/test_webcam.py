# -*- coding: utf-8 -*-

from WebcamVideoStream import WebcamVideoStream

import cv2
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Adding custom options for tesseract
custom_config = r'-c tessedit_char_whitelist=0123456789 --oem 3 --psm 7'


def draw_boxes(img_to_box):
    img = img_to_box.copy()

    # split the copied image into boxes
    boxes = pytesseract.image_to_boxes(img, config=custom_config, timeout=0.5)

    # draw each box
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (255, 255, 255), 2)
    return img


def print_img_str(img):
    # convert the clean image to string (only numerical characters here)
    img_str = pytesseract.image_to_string(img, config=custom_config, timeout=0.5)

    # removes the useless whitespaces
    img_str = img_str.strip()
    img_str = img_str.replace(" ", "")

    # if no result is found by tesseract, initialize it to 0
    if len(img_str) < 1:
        img_str = "0"

    print('Found: (' + img_str + ')')


vc = WebcamVideoStream(src=0).start()

while True:
    # read the current camera frame
    frame = vc.read()

    # show the current frame
    # DEBUG only, it slows down the program
    # cv2.imshow("My webcam", frame)

    # get the frame dimensions
    h, w, c = frame.shape

    # copy the image so it will be a cleaned image for tesseract
    img = vc.mask_frame()

    # DEBUG
    img_box = img.copy()
    #img_box = draw_boxes(img)

    # draw the chart containing the image with boxes
    cv2.imshow("Tesseract", img_box)

    print_img_str(img)

    # if 'x' key is pressed, exit the loop
    if cv2.waitKey(1) & 0XFF == ord('x'):
        break

# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()

# close the already opened camera
vc.stop()
