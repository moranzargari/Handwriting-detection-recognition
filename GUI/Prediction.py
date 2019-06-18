from keras.models import model_from_json
import os
import cv2
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from keras.preprocessing import image

#to avoid errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



def load_jason(model_name):
    json_file = open(str(model_name)+'.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    classifier = model_from_json(loaded_model_json)
    classifier.load_weights(str(model_name)+'.h5')

    return classifier


# def clasisfy_img(window_img,classifier_img):
#     img = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)
#     img = cv2.resize(img, (28, 28))
#     check_image = img
#     check_image = image.img_to_array(check_image)
#     check_image = np.expand_dims(check_image, axis=0)
#     result = classifier_img.predict(check_image / 255)
#
#     # print(str(float("{0:.2f}".format(result[0][0]))))
#     if result[0][0] < 0.5:
#         return 0
#     else:
#         return 1


def clasify_letter(window_img, classifier_letters):

    img = cv2.resize(window_img, (28, 28))
    check_image = img
    check_image = image.img_to_array(check_image)
    check_image = np.expand_dims(check_image, axis=0)
    result = classifier_letters.predict(check_image / 255)
    # prediction_index = np.argmax(result[0])
    return result


