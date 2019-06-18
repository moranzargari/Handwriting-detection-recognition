import cv2
import numpy as np

def draw_white_cells(roiriginal, roi):
   for k in range(roiriginal.shape[0]):
      for j in range(roiriginal.shape[1]):
         if roi[k][j] == 255:
            try:
               roiriginal[k][j] = 255
            except Exception:
               pass
   return roiriginal

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
   new_ctr = list()

   class contur:
      def __init__(self, x, y, w, h):
         self.x_start = x
         self.y_start = y
         self.x_end = x + w
         self.y_end = y + h

   for j, ctr in enumerate(sorted_ctrs):
      x, y, w, h = cv2.boundingRect(ctr)
      c = contur(x, y, w, h)
      new_ctr.append(c)


   length = len(new_ctr)

   i = 0
   kernel = np.ones((3, 3), np.uint8)
   while i < length:
      x, y, w, h = cv2.boundingRect(sorted_ctrs[i])

      if h > 3:
         canvas = np.ones_like(word_image)
         canvas.fill(255)
         cv2.drawContours(canvas, sorted_ctrs, i, (0, 0, 0), 3)

         if i < length - 1 and new_ctr[i].x_start >= new_ctr[i + 1].x_start and new_ctr[i].x_end <= new_ctr[
            i + 1].x_end:
            Y_end_bigger = max(new_ctr[i].y_end, new_ctr[i + 1].y_end)
            cv2.drawContours(canvas, sorted_ctrs, i + 1, (0, 0, 0), 3)
            # canvas = cv2.erode(canvas, kernel, iterations=1)
            roi = canvas[new_ctr[i + 1].y_start:Y_end_bigger, new_ctr[i + 1].x_start:new_ctr[i + 1].x_end]
            roiriginal = word_image[new_ctr[i + 1].y_start:Y_end_bigger, new_ctr[i + 1].x_start:new_ctr[i + 1].x_end]
            i += 1
         else:
            # canvas = cv2.erode(canvas, kernel, iterations=1)
            roi = canvas[y:y + h, x:x + w]
            roiriginal = word_image[y:y + h, x:x + w]
         roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
         # cv2.imshow(str(i)+"roi1", roi)
         # cv2.imshow(str(i)+"roi2", roiriginal)
         # cv2.waitKey(0)
         roi = draw_white_cells(roiriginal, roi)
         roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
         img_b = np.pad(roi, pad_width=10, mode='constant', constant_values=255)
         # cv2.imshow(str(i), img_b)
         # cv2.waitKey(0)
         # cv2.destroyAllWindows()
         letters_images.append(img_b)
      i+=1
   return letters_images