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
    flag = 0  # flag for כ
    for i, line in enumerate(lines_images):
        words = Dynamic_dilation.dynamicDilation(line)
        for j, word in enumerate(words):
            letters = FindConturs.find_letters(word)
            end_of_list = 0
            for k, letter in enumerate(letters):
                if k == len(letters) - 1:
                    end_of_list = 1
                char = classify_letters_images(letter, classifier_letters, end_of_list)
                if char == 'ג' or char == 'ז':
                    char = z_Or_g(char, letter)
                if char == 'ו' or char == 'י':
                    char = vav_OR_yud(char, letter, word.shape[0], end_of_list)
                if char == 'כ':
                    result = check_c(letter)
                    if result == 1:
                        flag = 1
                    else:
                        output_text += char
                else:
                    if flag == 1 and char == 'ו':
                        output_text += 'א'
                        flag = 0
                    elif flag == 1:
                        output_text += 'טו'
                        flag = 0
                    else:
                        output_text += char
            output_text += " "
        output_text += "\n"
    #     break
    # for i, word in enumerate(words):
    #     cv2.imshow(str(i), word)
    #     cv2.waitKey(0)
    print(output_text)
    return output_text


def sumPixels_stage(original):
    copy_img = original.copy()
    try:
        copy_img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    except:
        pass
    ret, thresh = cv2.threshold(copy_img, 127, 255, cv2.THRESH_BINARY_INV)

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


def classify_letters_images(letter_img, classifier_letters, end_of_list):
    # we loaded the 2 models in the beginning
    # the flag decide which model we want to run
    # we have 2 options : (0) model to classify if the image contain letter or not
    # (1) model to classify which letter the image is.
    # so we must first check with stage (0) if the image contain letter at all and then (1) recognize which letter it is

    letters = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י'
        , 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת',
               'ך', 'ם', 'ן', 'ף', 'ץ']

    predictions_vector = Prediction.clasify_letter(letter_img.image_letter, classifier_letters)
    prediction_index = np.argmax(predictions_vector[0])
    str_letter = letters[prediction_index]
    str_letter_temp = str_letter

    if end_of_list == 0:
        problem_letters = ['ך', 'ם', 'ן', 'ף', 'ץ']
    else:
        problem_letters = ['כ', 'מ', 'נ', 'פ', 'צ']

    while str_letter_temp in problem_letters:
        predictions_vector[0][prediction_index] = 0
        prediction_index = np.argmax(predictions_vector[0])
        str_letter_temp = letters[prediction_index]

    if predictions_vector[0][prediction_index] == 0:
        if str_letter == 'ף':
            prediction_index = 11
        elif str_letter == 'ם':
            prediction_index = 14
        elif str_letter == 'ץ':
            prediction_index = 11
        elif str_letter == 'ן':
            prediction_index = 5
        elif str_letter == 'ך':
            prediction_index = 18
        elif str_letter == 'פ':
            prediction_index = 11
        elif str_letter == 'מ':
            prediction_index = 14
        elif str_letter == 'צ':
            prediction_index = 11
        elif str_letter == 'נ':
            prediction_index = 5
        elif str_letter == 'כ':
            prediction_index = 18

    return letters[prediction_index]  # returns the actual letter in hebrew in string


def check_c(letter):
    ret, thresh = cv2.threshold(letter.image_letter, 109, 255, cv2.THRESH_BINARY_INV)
    H, W = letter.image_letter.shape[:2]
    height = H // 2
    i = 0
    j = W - 1
    while thresh[height][i] != 255 and thresh[height][j] != 255:
        i += 1
        j -= 1
    if thresh[height][i] == 255:
        return 1
    else:
        return 0


def vav_OR_yud(char, letterObject, wordH, end_of_list):
    if end_of_list == 1 and letterObject.conturH > wordH * 0.7:
        return 'ן'

    if letterObject.conturH < wordH * 0.3:
        return 'י'
    elif letterObject.conturH > wordH * 0.55:
        return 'ו'
    else:
        return char


def z_Or_g(char, letterObject):
    letter = cv2.resize(letterObject.image_letter, (28, 28))
    ret, letter = cv2.threshold(letter, 109, 255, cv2.THRESH_BINARY_INV)
    letter = 255- letter
    i = 27
    j = 14
    lower_range = 0
    upper_range = 0
    while i > 0:
        if letter[i][j] == 0 and lower_range == 0:
            while i > 0 and letter[i][j] == 0:
                i -= 1
            lower_range = i
        if letter[i][j] == 0 and lower_range != 0:
            upper_range = i + 1
            break
        i -= 1
    if upper_range == 0:
        return char
    for k in range(upper_range,lower_range):
        r = 1
        while letter[k][j + r] == 255 and letter[k][j - r] == 255:
            if r == 13:
                return char
            r += 1
        if letter[k][j + r] == 0 and letter[k][j - r] == 0:
            continue
        if letter[k][j + r] == 0:
            while letter[k][j - r] == 255:
                if r == 13:
                    return 'ז'
                r += 1
        elif letter[k][j - r] == 0:
            while letter[k][j + r] == 255:
                if r == 13:
                    return 'ג'
                r += 1
    return char
