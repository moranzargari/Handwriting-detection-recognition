import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import savgol_filter
from statistics import median



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

def detect_Lines(original,thresh):

    hight, width = thresh.shape[:2]
    # creates a vector that containing the sum of pixels per line
    img_row_sum = np.sum(thresh, axis=1)

    # smoothing the data by Savitzky–Golay filter
    w = savgol_filter(img_row_sum,19, 1)

    # find maximum points
    c_w_max = argrelextrema(w, np.greater, order=5)

    # find the median of the differences between two adjacent maximum points
    median_prev = findMedian(c_w_max[0])

    # initialize stop conditions
    delta = 1  # threshold of change between iterations
    i = 2  # index of current iteration

    # in each iteration, do smooth until the difference between iterations < delta
    while 1:
     for x in range(i):
        if x == 0:
            w = savgol_filter(w, 11, 1)
        else:
            w = savgol_filter(w, 9, 1)
     c_w_max = argrelextrema(w, np.greater, order=5)
     median_next = findMedian(c_w_max[0])
     if abs(median_next-median_prev) <= delta:
        break
     median_prev = median_next
     i += 1

    # ####################################################################
    # # show current status
    # plt.scatter(c_w_max[0], w[c_w_max[0]], linewidth=1.5, s=40, c='black')
    # plt.plot(img_row_sum)
    # plt.plot(w, 'pink')
    # plt.show()

    ####################################################################
    # after smoothing the graph, now we will find the minimum upper and lower points of the line- Y's values
    max_points = c_w_max[0]
    lines_upper, lines_lower = list(), list()
    min = img_row_sum[0]
    indexU, indexL = 0, 0 # holds the bounderys of the lower and upper Y's values of the lines
    i, j, k = 0, 0, 0 # indexs of minimum points
    while i < len(img_row_sum) and j < len(max_points):
        while i < max_points[j]:
            if img_row_sum[i] < min:
                min = img_row_sum[i]
                indexL = i
            i += 1
            if img_row_sum[k] <= min:
                min = img_row_sum[k]
                indexU = k
            k += 1
        lines_lower.append(indexL)
        lines_upper.append(indexU)
        min = img_row_sum[max_points[j]]
        j += 1

    ####################################################################
    # finding the last minimum point, so we could find the last lower line.
    last_max_point = max_points[len(max_points)-1]
    last_min_point=  img_row_sum[last_max_point]
    index = 0
    for x in range(last_max_point,len(img_row_sum)):
      if img_row_sum[x] < last_min_point:
          index = x
          last_min_point = img_row_sum[x]
    lines_lower.append(index)

    ####################################################################
    # cut's each line
    class line:
        def __init__(self, img, upper_bound, lower_bound):
            self.img = img
            self.upper_bound = upper_bound
            self.lower_bound =lower_bound


    lines = list()
    min_line_hight = 20
    count_lines_min_hight = 0
    for v in range(len(lines_upper)):
        if lines_upper[v] > lines_lower[v + 1]:
            continue
        roi = original[lines_upper[v]:lines_lower[v + 1], 0:width]
        if roi.shape[0] < min_line_hight:
            count_lines_min_hight += 1
        if roi.shape[0] > 7:
            cur_line = line(roi,lines_upper[v],lines_lower[v + 1])
            lines.append(cur_line)
        # cv2.imshow('malben', roi)
        # cv2.imwrite("alo1/" + str(v) + ".png", roi)
        # cv2.waitKey(0)
    if count_lines_min_hight > len(lines)*0.5:
        return lines, 1
    return lines, 0

####################################################################
