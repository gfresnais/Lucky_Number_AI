# -*- coding: utf-8 -*-

"""
@author: Gallien FRESNAIS
"""

import numpy as np
import cv2
import tensorflow as tf
import tensorflow.keras as keras

# - Local - #
from WebcamVideoStream import WebcamVideoStream

"""
Main program
"""


def main():
    # TODO; Load Model and set it to the Intel NCS2 USB


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
            # convert the frame to an array
            img_array = keras.preprocessing.image.img_to_array(frame)
            img_array = tf.expand_dims(img_array, 0)

            # TODO: get a prediction using the NCS2

            # get a prediction
            #predictions = interpreter.get_tensor(output_details[0]['index'])
            #classes = predictions.argmax(axis=-1)
            #score = tf.nn.softmax(predictions[0])

            # RESULT
            #print(
            #    "This image most likely belongs to {} with a {:.2f} percent confidence."
            #    .format(classes[np.argmax(score)], 100 * np.max(score))
            #)

    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

    # close the already opened camera
    vc.stop()


if __name__ == '__main__':
    main();
