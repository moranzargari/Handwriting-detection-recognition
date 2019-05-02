import cv2
import matplotlib.pyplot as plt
import numpy as np


################################################## read an image

## 100,104,107,109,112...........101,102,108,110,113.........103,105,106,111......115,118,121,124.....116,119,122,125....114,117,120,123,126...127,130....128,131...129,132
##133,136,139,142,145,148,151,154...............134,137,140,143,146,149,152,155.......135,150,147,144,141,138,153,156
## 157,181,178,175,172,169,166,163,160......182,179,176,173,170,167,164,161.................159,183,180,177,174,171,168,165,162
##197,194,190,187,184...............,185,188,192,195,198..................186,189,193,196,199
image = cv2.imread('k/TABLES/198.jpg')    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
table_name = 198 ## this variable is used for changing the img letter name.

##################################################


kernel = np.ones((5, 5),  np.uint8)

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
      roi = gray[y:y+h, x:x+w]

      # show ROI
      # cv2.imshow('segment no:'+str(i),roi)
      # creating a rectangle for each letter
      cv2.rectangle(gray,(x,y),( x + w, y + h ),(90,255,0),2)
      # cv2.waitKey(0)
      H = int(h*0.15)
      W = int(w*0.13)

      # remove each frame
      letter = roi[H:h - H , W:w - W]

      letter = cv2.erode(letter, kernel, iterations=1)
      #we want each image to be 28x28 size so we use resize
      letter = cv2.resize(letter, (28,28))
      num_of_squars = 6
      if curr_folder!= counter//10 +1:
         name_num = 0
      #write each image to the right folder
      cv2.imwrite("k/"+str(counter//num_of_squars +1)+"/"+str(name_num)+"_"+str(table_name)+ ".png", letter)
      curr_folder = counter//10 +1
      name_num+=1
      counter+=1

cv2.imshow('marked areas',image)
cv2.waitKey(0)

# cv2.imwrite("k/alo.png", image)
