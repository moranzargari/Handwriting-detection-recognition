import cv2
import numpy as np

img = cv2.imread("r.jpg",0)
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((5,5),np.uint8)

dialation = cv2.dilate(thresh,kernel,iterations=1)
erosion = cv2.erode(dialation,kernel,iterations=1)
frame = (dialation - erosion) - thresh

frame1  = 255 - frame


kernel = np.ones((3, 3), np.uint8)  # kernel
prev = np.zeros((img.shape[0], img.shape[1]), np.uint8)  # previous iteration result
cur = np.zeros((img.shape[0], img.shape[1]), np.uint8)  # current iteration result

cur[0, 0] = frame1[0, 0]

while (np.bitwise_xor(prev, cur).any()):
    prev = cur
    cur = cv2.morphologyEx(cur, cv2.MORPH_DILATE, kernel)
    cur = cv2.bitwise_and(cur, frame1)

cur = 255 - cur
cv2.imshow('final result', cur)
cv2.waitKey(0)
