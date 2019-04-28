import cv2
import matplotlib.pyplot as plt
import numpy as np


################################################## read an image 


image = cv2.imread('k/TABLES/50.jpg')    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
table_name = 50 ## this variable is used for changing the img letter name.

##################################################




# cv2.imshow('table_orig', image)
# cv2.waitKey(0)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # setting the image to gray
# cv2.imshow('gray',gray)
# cv2.waitKey(0)

ret,thresh = cv2.threshold(gray, 109, 255, cv2.THRESH_BINARY_INV) # choosing the best threshold that we wish
# cv2.imshow('thresh',thresh)
# cv2.waitKey(0)

# we are using "findContours" function to locate all the squares that contain the letters
im2, ctrs, hier = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# sort the contours to get the first line of the letter "א" and so on
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[1])

folders = list() # creating a list of folders names 
counter = 0
name_num = 0
curr_folder = 1
for i, ctr in enumerate(sorted_ctrs):
   # Get bounding box
   x, y, w, h = cv2.boundingRect(ctr)
   if h>=60 and w>=60:

      # Getting ROI--each letter image
      roi = image[y:y+h, x:x+w]

      # show ROI
      # cv2.imshow('segment no:'+str(i),roi)
      # creating a rectangle for each letter
      cv2.rectangle(image,(x,y),( x + w, y + h ),(90,255,0),2)
      # cv2.waitKey(0)
      H = int(h*0.15)
      W = int(w*0.13)

      # remove each frame
      letter = roi[H:h - H , W:w - W]
      #we want each image to be 28x28 size so we use resize
      letter = cv2.resize(letter, (28,28))
      if curr_folder!= counter//10 +1:
         name_num = 0
      #write each image to the right folder
      cv2.imwrite("k/"+str(counter//10 +1)+"/"+str(name_num)+"_"+str(table_name)+ ".png", letter)
      curr_folder = counter//10 +1
      name_num+=1
      counter+=1

cv2.imshow('marked areas',image)
cv2.waitKey(0)

# cv2.imwrite("k/alo.png", image)

