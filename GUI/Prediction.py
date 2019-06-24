from keras.models import model_from_json
import os
import cv2
import numpy as np
from keras.preprocessing import image

#to avoid errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



def load_jason(model_name):
    """
        this method receives a trained model name and load the model to
        a classifier object and return's the classifier.
        with this classifier we able to predicts the letters from the image.
    """
    json_file = open(str(model_name)+'.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    classifier = model_from_json(loaded_model_json)
    classifier.load_weights(str(model_name)+'.h5')

    return classifier


def clasify_letter(window_img, classifier_letters):
    """
        input: classifier = classifier_letters
               image of the current letter = window_img
        this function job is to use the classifier that it receives
        to predict the letter from the image.
        the function returns a vector scores.
        this vector contain the score of each letter that the image maybe contain
        the letter (cell in the vector) with the highest score is the right prediction.
    """
    img = cv2.resize(window_img, (28, 28))
    check_image = img
    check_image = image.img_to_array(check_image)
    check_image = np.expand_dims(check_image, axis=0)
    result = classifier_letters.predict(check_image / 255)

    return result


