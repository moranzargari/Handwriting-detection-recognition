import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import savgol_filter
from statistics import median
import sys

####################################################################
# this function get an array as input
# and returns the median of the differences between the points
def findMedian(points):
   differences = list()
   if len(points) <= 1:
       return 0
   for i in range(len(points)):
       if i > 0:
           differences.append(points[i] - points[i - 1])
   return median(differences)

####################################################################
# reading the image (gray)
img_name = "alo/59.png"
img = cv2.imread(img_name, 0)
original = cv2.imread(img_name)

# binary
ret, thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)

hight, width = thresh.shape[:2]

#slice margines from the lower part of the image
thresh = thresh[:int(hight*0.88), :]

# kernel = np.ones((9,9), np.uint8)
# img_dilation = cv2.dilate(thresh, kernel, iterations=1)
cv2.imshow('dilated',thresh)
cv2.waitKey(0)


####################################################################
# creates a vector that containing the sum of pixels per line
img_row_sum = np.sum(thresh, axis=0)

# create a list of all the points on the graph that is bigger then zero- not a space between words/letters
points_max_min = list()
for i,v in enumerate(img_row_sum):
    if v!=0:
        points_max_min.append(i)

####################################################################
# show current status
plt.plot(img_row_sum)
plt.show()
plt.scatter(points_max_min, img_row_sum[points_max_min], linewidth=1.5, s=40, c='black')
plt.plot(img_row_sum)
plt.show()
####################################################################

#now we calculate the avarage of the entire spaces on the image sizes
sum = 0
spaces=0
flg=0
space = list()
for i in range(1,len(points_max_min)):
    for j in range(points_max_min[i-1],points_max_min[i]):
        if img_row_sum[j]==0: # in case we meet a space
            flg=1
            break
    if flg==1:
        d = abs(points_max_min[i] - points_max_min[i-1]) # calculate the distance between the points
        if d < width*0.125:
            sum+= d
            spaces+=1
            flg=0

# calculate the avarage
if spaces!=0:
    reminder = sum % spaces
    m = sum // spaces
    if reminder >=0.5:
        m+=1
else:
    m = 0


#####################################################################
# find the right border of a word
idx_min = 0
count_zeros = 0
word_right_bound = list()
word_left_bound = list()
for i in range(1,len(points_max_min)):
    min = points_max_min[i-1] # the min point will be for the border
    for x in range(points_max_min[i-1],points_max_min[i]):
        if img_row_sum[x]==0: # count zeros between points -- so could know how big the space we saw
            count_zeros+=1
        if img_row_sum[x] < min:
            min = img_row_sum[x]
            idx_min = x
    if(m!=0 and count_zeros >= m*1.15): # in case the space is bigger then it is a space between words
        original = cv2.line(original, (idx_min, 0), (idx_min, hight), (0, 255, 0), 2)
        plt.axvline(x=idx_min, color='red')
        word_right_bound.append(idx_min)
    count_zeros=0


#####################################################################
# draw left border in blue
i, j=0, 0
while(i < len(img_row_sum)-1):
    value = img_row_sum[i]
    if value == 0 and img_row_sum[i+1]>0:
        original = cv2.line(original, (i, 0), (i, hight), (255, 0, 0), 2)
        plt.axvline(x=i, color='green')
        word_left_bound.append(i)
        i = word_right_bound[j]
        j += 1
    if j==len(word_right_bound):
        break
    i+=1

#####################################################################
#find the left border of a word in blue
v = len(img_row_sum)-1
if len(word_right_bound)!=0: # in case the image dosent contain one word
    for u in range(word_right_bound[-1],len(img_row_sum)-1):
        if img_row_sum[u]==0 and img_row_sum[u+1]>0:
            original = cv2.line(original, (u, 0), (u, hight), (255, 0, 0), 2)
            plt.axvline(x=u, color='green')
            word_left_bound.append(u)
            break
        u+=1
else: # in case the image contain only one word.
    u=0
    while u < len(img_row_sum)-1:
        if img_row_sum[u+1]>0:
            original = cv2.line(original, (u, 0), (u, hight), (255, 0, 0), 2)
            plt.axvline(x=u, color='green')
            word_left_bound.append(u)
            break
        u+=1

# this will find the last right border in green
while v>0:
    if img_row_sum[v]==0 and img_row_sum[v-1]>0:
        original = cv2.line(original, (v, 0), (v, hight), (0, 255, 0), 2)
        plt.axvline(x=v, color='red')
        word_right_bound.append(v)
        break
    v-=1
# show each word that the algorithm found
# for l,r in zip(word_left_bound,word_right_bound):
#     roi = img[0:hight, l:r]
#     cv2.imshow(str(l)+"-"+str(r), roi)
#     cv2.waitKey(0)

cv2.imwrite("out.png", original)
plt.scatter(points_max_min, img_row_sum[points_max_min], linewidth=1.5, s=40, c='black')
plt.plot(img_row_sum)
plt.show()

#####################################################################

cv2.imshow('with lines', original)
cv2.waitKey(0)
cv2.imwrite("output.png",original)

