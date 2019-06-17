import sumPixels
import cv2
import Dynamic_dilation
import Prediction
import FindConturs
import matplotlib.pyplot as plt
import numpy as np


def convert_the_image(original):

    # first lets load the 2 models we have for efficiency
    # classifier_img will be the classifier that decide if the img contain a letter or not.
    # classifier_letters be the classifier that decide which letter it is
    # those to classifiers will be in use in the letters recognition stage
    # classifier_img, classifier_letters = init_Neural_Network()
    classifier_letters = init_Neural_Network()

    # first stage = find the image lines
    lines_images = sumPixels_stage(original)
    output_text = ""
    for i, line in enumerate(lines_images):
        words = Dynamic_dilation.dynamicDilation(line)
        for j, word in enumerate(words):
            letters = FindConturs.find_letters(word)
            for k, letter in enumerate(letters):
                output_text += classify_letters_images(letter, classifier_letters)
            output_text+=" "
        output_text+= "\n"
    #     break
    # for i, word in enumerate(words):
    #     cv2.imshow(str(i), word)
    #     cv2.waitKey(0)
    print(output_text)
    return output_text



def sumPixels_stage(original):

    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # init - size_flg check if the image need resize
    lines, size_flg = sumPixels.detect_Lines(original, thresh)

    # in case the image need resize the call again to the function with the resize image
    if size_flg == 1:
        original = cv2.resize(original, (original.shape[1] * 2, original.shape[0] * 2))
        thresh = cv2.resize(thresh, (thresh.shape[1] * 2, thresh.shape[0] * 2))
        lines, size_flg = sumPixels.detect_Lines(original, thresh)

    return lines


def init_Neural_Network():

    # classifier_img = Prediction.load_jason("model126")
    # classifier_img.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    classifier_letters = Prediction.load_jason("model99")
    classifier_letters.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    # return classifier_img, classifier_letters
    return classifier_letters

def classify_letters_images(letter_img, classifier_letters):
    # we loaded the 2 models in the beginning
    # the flag decide which model we want to run
    # we have 2 options : (0) model to classify if the image contain letter or not
    # (1) model to classify which letter the image is.
    # so we must first check with stage (0) if the image contain letter at all and then (1) recognize which letter it is

    # letter_or_not = Prediction.clasisfy_img(window_img, classifier_img)
    # if letter_or_not == 0:
    #     return letter_or_not# 0- not letter, 1- yes letter
    # else:
        letters = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י'
                    , 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת',
                   'ך', 'ם', 'ן', 'ף', 'ץ']

        prediction_index = Prediction.clasify_letter(letter_img, classifier_letters)
        return letters[prediction_index] # returns the actual letter in hebrew in string