# -*- coding: utf-8 -*-

"""
@author: Gallien FRESNAIS
"""

import numpy as np
import cv2
import tensorflow as tf
import tensorflow.keras as keras

# TFLite with Coral, needs to be installed locally on the Raspberry Pi 4
from tflite_runtime.interpreter import load_delegate

# - Local - #
from WebcamVideoStream import WebcamVideoStream

"""
Main program
"""


def main():
    # Load Model and allocate tensors to the Coral USB device
    interpreter = tf.lite.Interpreter(model_path='../../../AI_Token_Recognition.tflite',
                                      experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

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
            img = cv2.resize(frame, (160, 160))

            cv2.imshow("Resized", img)

            # convert the frame to an array
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            # set the input to give it the image
            interpreter.set_tensor(input_details[0]['index'], img_array)
            interpreter.invoke()

            # get a prediction
            predictions = interpreter.get_tensor(output_details[0]['index'])
            score = tf.nn.softmax(predictions[0])

            # RESULT
            print(
                "This image most likely belongs to {} with a {:.2f} percent confidence."
                .format(np.argmax(score), 100 * np.max(score))
            )

    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

    # close the already opened camera
    vc.stop()


if __name__ == '__main__':
    main();
