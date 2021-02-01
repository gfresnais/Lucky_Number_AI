# -*- coding: utf-8 -*-

"""
@author: Gallien FRESNAIS
"""

import cv2
import easyocr

# - Local - #
from WebcamVideoStream import WebcamVideoStream

# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Adding custom options for tesseract
custom_config = r'-c tessedit_char_whitelist=0123456789 --oem 3 --psm 9'

"""
Draws boxes near what characters tesseract found
"""


def draw_boxes(img_to_box, reader):
    img = img_to_box.copy()

    # split the copied image into boxes
    boxes = reader.detect(img)

    # draw each box
    for b in boxes:
        if len(b) > 0:
            b = b[0]
            img = cv2.rectangle(img, (int(b[0]), int(b[2])), (int(b[1]), int(b[3])), (255, 255, 255), 2)
    return img


"""
Prints the image as a string
Only numerical characters
"""


def print_img_str(img, reader):
    # convert the clean image to string (only numerical characters here)
    img_str = reader.readtext(img, allowlist="0123456789")

    res = "0"
    # if no result is found by tesseract, initialize it to 0
    if len(img_str) > 0:
        if img_str[0][1].isdigit():
            res = img_str[0][1]

    # removes the useless whitespaces
    res = res.strip()
    res = res.replace(" ", "")

    print('Found: (' + res + ')')


"""
Main program
"""


def main():
    vc = WebcamVideoStream(src=0).start()

    reader = easyocr.Reader(['en'])

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
            img_box = draw_boxes(img, reader)

            # draw the chart containing the image with boxes
            cv2.imshow("Tesseract", img_box)

            print_img_str(img, reader)

    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

    # close the already opened camera
    vc.stop()


if __name__ == '__main__':
    main();
