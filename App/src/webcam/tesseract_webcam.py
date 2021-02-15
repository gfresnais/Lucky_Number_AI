# -*- coding: utf-8 -*-

"""
@author: Gallien FRESNAIS
"""

import cv2
import pytesseract

# - Local - #
from WebcamVideoStream import WebcamVideoStream

# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Adding custom options for tesseract
custom_config = r'-c tessedit_char_whitelist=0123456789 --oem 3 --psm 9'

"""
Draws boxes near what characters tesseract found
"""


def draw_boxes(img_to_box):
    img = img_to_box.copy()

    # get the frame dimensions
    h, w, c = img.shape

    # split the copied image into boxes
    boxes = pytesseract.image_to_boxes(img, config=custom_config)

    # draw each box
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (255, 255, 255), 2)
    return img


"""
Prints the image as a string
Only numerical characters
"""


def print_img_str(img):
    # convert the clean image to string (only numerical characters here)
    img_str = pytesseract.image_to_string(img, config=custom_config)

    # removes the useless whitespaces
    img_str = img_str.strip()
    img_str = img_str.replace(" ", "")

    # if no result is found by tesseract, initialize it to 0
    if len(img_str) < 1:
        img_str = "0"
    elif len(img_str) > 2:
        img_str = img_str[0:1]

    print('Found: (' + img_str + ')')


"""
Main program
"""


def main():
    vc = WebcamVideoStream(src=0).start()

    while True:
        # read the current camera frame
        frame = vc.read()

        # show the current frame (untouched)
        cv2.imshow("My webcam", frame)

        # if 'x' key is pressed, exit the loop
        if cv2.waitKey(1) & 0XFF == ord('x'):
            break
        # if 'c' key is pressed, process the frame for OCR
        if cv2.waitKey(1) & 0xFF == ord('c'):
            # copy the image so it will be a cleaned image for tesseract
            img = vc.mask_frame()

            # DEBUG
            img_box = draw_boxes(img)

            # draw the chart containing the image with boxes
            cv2.imshow("Tesseract", img_box)

            print_img_str(img)

    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

    # close the already opened camera
    vc.stop()


if __name__ == '__main__':
    main();
