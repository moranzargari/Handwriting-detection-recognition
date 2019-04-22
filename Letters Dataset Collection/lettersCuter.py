import cv2
import matplotlib.pyplot as plt
import numpy as np


##################################################ALOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO


image = cv2.imread('kaki/TABLES/2.jpg')    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
table_name = 2

##################################################ALOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO




cv2.imshow('table_orig', image)
cv2.waitKey(0)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray)
cv2.waitKey(0)

ret,thresh = cv2.threshold(gray, 109, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('thresh',thresh)
cv2.waitKey(0)

im2, ctrs, hier = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[1])

folders = list()
counter = 0
name_num = 0
curr_folder = 1
for i, ctr in enumerate(sorted_ctrs):
   # Get bounding box
   x, y, w, h = cv2.boundingRect(ctr)
   if h>=60 and w>=60:

      # Getting ROI
      roi = image[y:y+h, x:x+w]

      # show ROI
      # cv2.imshow('segment no:'+str(i),roi)
      cv2.rectangle(image,(x,y),( x + w, y + h ),(90,255,0),2)
      # cv2.waitKey(0)
      H = int(h*0.15)
      W = int(w*0.13)

      letter = roi[H:h - H , W:w - W]

      if curr_folder!= counter//10 +1:
         name_num = 0
      cv2.imwrite("kaki/"+str(counter//10 +1)+"/"+str(name_num)+"_"+str(table_name)+ ".png", letter)
      curr_folder = counter//10 +1
      name_num+=1
      counter+=1

cv2.imshow('marked areas',image)
cv2.waitKey(0)
