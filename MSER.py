
import cv2

def grouper(iterable, interval=2):
   print(interval)
   prev = None
   group = []
   for item in iterable:
       if not prev or abs(item[1] - prev[1]) <= interval:
           group.append(item)
       else:
           yield group
           group = [item]
       prev = item
   if group:
       yield group


img = cv2.imread('collection/110.jpg')
mser = cv2.MSER_create()


# img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))
cv2.imshow('a', img)
cv2.waitKey(0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('b', gray)
cv2.waitKey(0)
# vis = img.copy()
#
# regions = mser.detectRegions(gray)
# hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions[0]]
# cv2.polylines(vis, hulls, 1, (0,255,0))

coordinates, bboxes = mser.detectRegions(gray)
# coordinates holds the resulting list of points sets , bboxes holds the resulting bounding boxes
# for bbox in bboxes:
#    x, y, w, h = bbox
#    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) # draw the rectangle borders
#
# cv2.imshow('c', img)
# cv2.waitKey(0)
##
###

bboxes_list = list()
heights = list()
for bbox in bboxes:
   x, y, w, h = bbox
   bboxes_list.append([x, y, x + w, y + h])  # Create list of bounding boxes, with each bbox containing the left-top and right-bottom coordinates
   heights.append(h)
heights = sorted(heights)  # Sort heights
median_height = heights[len(heights) // 4] // 4# Find half of the median height

###
###
cv2.imshow('d', img)
cv2.waitKey(0)

bboxes_list = sorted(bboxes_list, key=lambda k: k[1])  # Sort the bounding boxes based on y1 coordinate ( y of the left-top coordinate )
combined_bboxes = grouper(bboxes_list, median_height)  # Group the bounding boxes
for group in combined_bboxes:
   x_min = min(group, key=lambda k: k[0])[0]  # Find min of x1
   x_max = max(group, key=lambda k: k[2])[2]  # Find max of x2
   y_min = min(group, key=lambda k: k[1])[1]  # Find min of y1
   y_max = max(group, key=lambda k: k[3])[3]  # Find max of y2
   cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

   roi = img[y_min:y_max,x_min:x_max]
   # cv2.imwrite("alo/"+str(y_min)+"-"+str(y_max)+".png", roi)
   cv2.imshow("ff",roi)
   cv2.waitKey(0)

cv2.imshow('f', img)
cv2.waitKey(0)

cv2.imwrite("lines.png", img)


# https://stackoverflow.com/questions/48615935/merging-regions-in-mser-for-identifying-text-lines-in-ocr
