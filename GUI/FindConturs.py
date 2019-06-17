import cv2
import numpy as np



def find_letters(word_image):


   if word_image.shape[0] < 40:
      print(word_image.shape[0])
      word_image = cv2.resize(word_image, (word_image.shape[1] * 2, word_image.shape[0] * 2))

   #grayscale
   gray = cv2.cvtColor(word_image,cv2.COLOR_BGR2GRAY)

   #binary
   ret,thresh = cv2.threshold(gray, 109, 255, cv2.THRESH_BINARY_INV)



   #dilation
   # kernel = np.ones((3,3), np.uint8)
   # img_dilation = cv2.dilate(thresh, kernel, iterations=1)
   # cv2.imshow('dilated',thresh)
   # cv2.waitKey(0)
   im2, ctrs, hier = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


   #sort contours
   sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0], reverse=True)

   letters_images = list()

   class contur:
      def __init__(self, x, y, w, h):
         self.x_start = x
         self.y_start = y
         self.x_end = x + w
         self.y_end = y + h

   new_ctr = list()
   for j, ctr in enumerate(sorted_ctrs):
      x, y, w, h = cv2.boundingRect(ctr)
      c = contur(x, y, w, h)
      new_ctr.append(c)


   for j, new_c in enumerate(new_ctr):
      length = len(new_ctr)
      if j < length-1 and new_c.x_start >= new_ctr[j+1].x_start and new_c.x_end <= new_ctr[j+1].x_end:
         bigger = max(new_c.y_end, new_ctr[j+1].y_end)
         new_ctr[j + 1].y_end = bigger
         new_ctr.remove(new_ctr[j])

   for i, ctr in enumerate(new_ctr):

      if (ctr.y_end - ctr.y_start) > 5:
         # Getting ROI
         roi = word_image[ctr.y_start:ctr.y_end, ctr.x_start:ctr.x_end]
         roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
         img_b = np.pad(roi, pad_width=10, mode='constant', constant_values=255)
         cv2.imshow(str(i), img_b)
         cv2.waitKey(0)
         letters_images.append(img_b)

   return letters_images