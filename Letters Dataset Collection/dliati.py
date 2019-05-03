import numpy as np
import cv2
import os


# load folder
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


# for each image do dilation
for number in range(1, 28):
    images = load_images_from_folder(str(number))
    i = 0
    for img in images:
        kernel = np.ones((1, 2), np.float32)
        img_erosion = cv2.erode(img, kernel, iterations=1)  # erosion
        cv2.imwrite('dataset/' + str(number) + '/' + str(i) + '.png', img_erosion)  # write new image
        i += 1
