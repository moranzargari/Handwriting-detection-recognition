#!/usr/bin/python3
# 2018.01.16 01:11:49 CST
# 2018.01.16 01:55:01 CST
import cv2
import numpy as np

## (1) read
img = cv2.imread("collection/110.jpg")
cv2.imshow('img-color', img)
cv2.waitKey(0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)
cv2.waitKey(0)

## (2) threshold
th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('threshed', threshed)
cv2.waitKey(0)

# ## (3) minAreaRect on the nozeros
# pts = cv2.findNonZero(threshed) #Returns the list of locations of non-zero pixels
# ret = cv2.minAreaRect(pts)

# (cx,cy), (w,h), ang = ret
# if w>h:
#     w,h = h,w
#     ang += 90

## (4) Find rotated matrix, do rotation
# M = cv2.getRotationMatrix2D((cx,cy), ang, 1.0)
# rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

## (5) find and draw the upper and lower boundary of each lines
hist = cv2.reduce(threshed,1, cv2.REDUCE_AVG).reshape(-1)

th = 3
H,W = img.shape[:2]
uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]

print (uppers)
threshed = cv2.cvtColor(threshed, cv2.COLOR_GRAY2BGR)
for y in uppers:
    cv2.line(threshed, (0,y), (W, y), (255,0,0), 1)
    cv2.imshow('marked areas', threshed)
    cv2.waitKey(0)

for y in lowers:
    cv2.line(threshed, (0,y), (W, y), (0,255,0), 1)
    cv2.imshow('marked areas', threshed)
    cv2.waitKey(0)
cv2.imwrite("result.png", threshed)