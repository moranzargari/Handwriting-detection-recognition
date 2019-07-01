import sumPixels
import cv2
import Dynamic_dilation
import Prediction
import FindLetters
import numpy as np


def convert_the_image(original, result_img):
    """
        this function is the main engine of the program, the function main job is
        to combine all algorithms inside 3 loops.
        first we call the neural network to create a classifier to classify between letters.
        then the first algorithm is starting for finding the lines , for each line we go to the
        second loop to find the words inside the lines and the third loop is for the letters inside
        each word.
    :param original: the original image with grayscale
    :param result_img: the original image with RGB for showing only
    :return: the output string that holds the convert result
    """
    classifier_letters = init_Neural_Network()

    # first stage = find the image lines
    lines_images = sumPixels_stage(original)
    output_text = ""
    flag = 0  # flag for כ
    for i, line in enumerate(lines_images): # for each line find the words
        words = Dynamic_dilation.dynamicDilation(line.img)
        for j, word in enumerate(words):
            result_img = cv2.rectangle(result_img, (word.left_bound, line.upper_bound), (word.right_bound, line.lower_bound), (255, 0, 0), 2) # draw the rectangle borders
            letters = FindLetters.find_letters(word.roi)
            end_of_list = 0
            for k, letter in enumerate(letters): # for each word find the letters
                if k == len(letters) - 1: # flag to know if we see the last letter
                    end_of_list = 1
                char = classify_letters_images(letter, classifier_letters, end_of_list) # classify the letters
                if char == 'ג' or char == 'ז':
                    char = z_Or_g(char, letter)
                if char == 'ו' or char == 'י':
                    char = vav_OR_yud(char, letter, word.hight, end_of_list)
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
                        output_text += char # concat the output letters
            output_text += " "
        output_text += "\n"
    return output_text, result_img


def sumPixels_stage(original):
    """
        this function is for detectin the lines from the image.
    :param original: gets the image in grayscale
    :return: array of images with all the image lines
    """
    copy_img = original.copy()
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
    """
        this function run our model and create's a classifier to decide which letter is what
    :return: classifier
    """
    classifier_letters = Prediction.load_jason("model99")
    classifier_letters.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return classifier_letters


def classify_letters_images(letter_img, classifier_letters, end_of_list):
    """
        this function is deciding which letter the "letter_img" contain from all the
        27 classes that the classifier know.
        we take the result with the high score of all.
        also this function is handling special situations when the classifier is having hart time
        for example : Final letters in hebrew must show at rhe end of the word and not in the middle
    :param letter_img: an image that contain the letter that the algorithms detected
    :param classifier_letters: our model classifier
    :param end_of_list: flag for the end of a word
    :return: a string that is the predicted letter
    """

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
    """
        this function is for handel the letter "ג" that that contain 2 parts together
        the function is taking care of the first part of the letter which look like the letter "c" in english
        in different directions.
    :param letter: gets the first part of the letter "ג"
    :return: if it's in the right direction the the result is 1 then the answer is correct otherwise 0
    """
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
    """
        this function is for distinguish between the letters "כ" and "ח" that look similar in
        some handwriting , to help the network decide between them
    :param char: the network classification
    :param letterObject: the letter image and height
    :param wordH: the word height
    :param end_of_list: flag for the end of a word
    :return: a char with the letter
    """
    if end_of_list == 1 and letterObject.conturH > wordH * 0.85:
        return 'ן'

    if letterObject.conturH < wordH * 0.35:
        return 'י'
    elif letterObject.conturH > wordH * 0.55:
        return 'ו'
    else:
        return char


def z_Or_g(char, letterObject):
    """
        this function is for distinguish between the letters "ט" and "ה" that look similar in
        some handwriting , to help the network decide between them
    :param char: the network classification
    :param letterObject: the letter image and height
    :return: a char with the letter
    """
    letter = cv2.resize(letterObject.image_letter, (28, 28))
    ret, letter = cv2.threshold(letter, 109, 255, cv2.THRESH_BINARY_INV)
    letter = 255 - letter
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
