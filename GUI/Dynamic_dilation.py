import cv2
import numpy as np





def dynamicDilation(original):



    # fitting image size
    if original.shape[0] < 40:
        original = cv2.resize(original, (original.shape[1] * 2, original.shape[0] * 2))
    elif original.shape[0] > 75:
        original = cv2.resize(original, (original.shape[1] // 2, original.shape[0] // 2))
    H, W = original.shape[:2]


    ####################################################################
    # proccessing the image first
    # copy image
    new_image = original.copy()
    new_image = new_image[int(H * 0.1):int(H * 0.8), :]

    # grayscale
    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    # binary
    ret, thresh = cv2.threshold(gray, 109, 255, cv2.THRESH_BINARY_INV)


    ####################################################################
    # find the contours before the dilation
    im2, ctrs, hier = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    startnum = len(ctrs)

    # first dilation
    kernel = np.ones((29, 5), np.float32)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    im22, ctrs2, hier2 = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # erosion
    kernel_erode = np.ones((1, 2), np.float32)
    if len(ctrs2) != 0 and len(ctrs) / len(ctrs2) < 6:
        # erosion
        thresh = cv2.erode(thresh, kernel_erode, iterations=1)

    # dilation
    kernel = np.ones((27, 5), np.float32)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    im22, ctrs2, hier2 = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # init before the dynamic dilation
    prev = 0
    ctrs_prev = ctrs
    kernel = np.ones((1, 2), np.float32)
    num_iterations = 4
    i = 0

    # dynamic dilation loop
    while abs(prev - len(ctrs)) > 0 or startnum == len(ctrs):
        prev = len(ctrs)
        ctrs_prev = ctrs
        img_dilation = cv2.dilate(img_dilation, kernel, iterations=num_iterations)
        if i % 2 == 1 and num_iterations != 1:
            img_dilation = cv2.erode(img_dilation, kernel_erode, iterations=1)
        im2, ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if (prev - len(ctrs)) > num_iterations and num_iterations < 4:
            num_iterations += 1
        else:
            while (prev - len(ctrs)) < num_iterations:
                num_iterations -= 1
        if num_iterations < 1:
            num_iterations = 1
        if i == 10:
            break
        i += 1


    ####################################################################
    # sort contours = sort the word
    sorted_ctrs = sorted(ctrs_prev, key=lambda ctr: cv2.boundingRect(ctr)[0], reverse=True)
    line_words = list()
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
        y = 0
        h = H
        # Getting ROI
        roi = original[y:y + h, x:x + w]
        line_words.append(roi)
        # show ROI
        # cv2.imshow('segment no:' + str(i), roi)
        # # cv2.rectangle(image, (x, y), (x + w, y + h), (90, 0, 255), 2)
        # cv2.waitKey(0)
    return line_words





# cv2.imshow('marked areas', image)
# cv2.waitKey(0)
#
# cv2.imwrite("roi/'words.png", image)