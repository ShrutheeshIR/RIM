"""
This module is the main module in this package. It loads emotion recognition model from a file,
shows a webcam image, recognizes face and it's emotion and draw emotion on the image.
"""
from cv2 import WINDOW_NORMAL

import cv2
from face_detect import find_faces
from image_commons import draw_with_alpha,nparray_as_image
import os
from random import randint

def _load_emoticons1(emotions):
    """
    Loads emotions images from graphics folder.
    :param emotions: Array of emotions names.
    :return: Array of emotions graphics.
    """
    return [nparray_as_image(cv2.imread('graphics/%s.png' % emotion, -1), mode=None) for emotion in emotions]


def show_webcam_and_run1(model, emoticons, window_size=None, window_name='webcam', update_time=10):
    """
    Shows webcam image, detects faces and its emotions in real time and draw emoticons over those faces.
    :param model: Learnt emotion detection model.
    :param emoticons: List of emotions images.
    :param window_size: Size of webcam image window.
    :param window_name: Name of webcam image window.
    :param update_time: Image update time interval.
    """
 
    emptyarray = []
    for x in os.listdir('abcd'):
        webcam_image = cv2.imread('abcd/' + x)
        for normalized_face, (x, y, w, h) in find_faces(webcam_image):

            prediction = model.predict(normalized_face)  # do prediction
            if cv2.__version__ != '3.1.0':
                prediction = prediction[0]
            emptyarray.append(prediction)

            image_to_draw = emoticons[prediction]
            draw_with_alpha(webcam_image, image_to_draw, (x, y, w, h))

    val = max(set(emptyarray), key=emptyarray.count)
    return val




if __name__ == '__main__':
    emotions = ['neutral', 'anger', 'disgust', 'happy', 'sadness', 'surprise']
    emoticons = _load_emoticons1(emotions)

    # load model
    if cv2.__version__ == '3.1.0':
        fisher_face =cv2.face.FisherFaceRecognizer_create()
    else:
        fisher_face = cv2.face.FisherFaceRecognizer_create()
    fisher_face.read('models/emotion_detection_model.xml')

    # use learnt model
    window_name = 'WEBCAM (press ESC to exit)'
    val  = show_webcam_and_run1(fisher_face, emoticons, window_size=(1600, 1200), window_name=window_name, update_time=8)
    print(emotions[val])