
import cv2
import numpy as np
#import image
image = cv2.imread('alo/2.png')
cv2.imshow('orig', image)
cv2.waitKey(0)

if image.shape[0] < 40:
   print(image.shape[0])
   image = cv2.resize(image, (image.shape[1] * 2, image.shape[0] * 2))

#grayscale
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray)
cv2.waitKey(0)

#binary
ret,thresh = cv2.threshold(gray, 109, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('second',thresh)
cv2.waitKey(0)



#dilation
kernel = np.ones((9,9), np.uint8)
img_dilation = cv2.dilate(thresh, kernel, iterations=1)
cv2.imshow('dilated',img_dilation)
cv2.waitKey(0)
im2, ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
prev = 0

kernel = np.ones((5,2), np.uint8)
i=1
while prev != len(ctrs):
   prev = len(ctrs)
   img_dilation = cv2.dilate(img_dilation, kernel, iterations=-1)
   im2, ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   print (prev, len(ctrs))
   cv2.imshow('dilated', img_dilation)
   cv2.waitKey(0)
   if i==1:
      i=2
   else:
      i=1

#sort contours)
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0], reverse=True)

for i, ctr in enumerate(sorted_ctrs):
   # Get bounding box
   x, y, w, h = cv2.boundingRect(ctr)

   # Getting ROI
   roi = image[y:y+h, x:x+w]

   # show ROI
   cv2.imshow('segment no:'+str(i),roi)
   cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
   cv2.waitKey(0)
   cv2.imwrite("roi/" + str(y) + "-" + str(y+h) + ".png", roi)

cv2.imshow('marked areas',image)
cv2.waitKey(0)

cv2.imwrite("alo.png", image)
