import cv2
import numpy as np



def union_left_ctr(cur_ctr, next_ctr,canvas):
   """
      the method main job is to combine 2 conturs to 1.
      some letters in hebrew are consists of two parts, those 2 parts must be together
      so that the network will classify the right word .
      example : "ש"  "ז"
   :param cur_ctr: first part of the word as contur
   :param next_ctr: second part of the word as contur
   :param canvas: the letters locations
   :return: the right action to preform
   """

   xtemp = cur_ctr.x_start - 3
   ytemp = cur_ctr.y_end - 1

   temp_canvas = canvas.copy()
   ret, temp_canvas = cv2.threshold(temp_canvas, 109, 255, cv2.THRESH_BINARY_INV)
   while temp_canvas[ytemp][xtemp] != 255 and xtemp >= next_ctr.x_start and xtemp > 0:
      xtemp -= 1

   if temp_canvas[ytemp][xtemp] == 255:
         return 0
   else:
         return 1


def draw_white_cells(roiriginal, roi):
   """
      the function main job is to erase noise around the letter, the noise could be a part of the
      next letter in the word. we want to delete the noise to help the classifier decide.
   :param roiriginal: getting an image with a handwritten letter
   :param roi: getting an image with a handwritten letter
   :return: the image without the noise
   """
   roi_temp= roiriginal.copy()
   for k in range(roi_temp.shape[0]):
      for j in range(roi_temp.shape[1]):
         if roi[k][j] == 255:
            roi_temp[k][j] = 255
   return roi_temp



def find_letters(word_image):
   """
      this function is the main function in this algorithm,
      the function cut each letter from the word image by using findconturs function
      each contur is part of the word image that contain a letter.
      also the function is handling few cases to get each letter without a noise around.
   :param word_image: the word image
   :return: a list of objects , each object contain the letter image and info about the image
   """

   if word_image.shape[0] < 40:
      word_image = cv2.resize(word_image, (word_image.shape[1] * 2, word_image.shape[0] * 2))

   #binary
   ret,thresh = cv2.threshold(word_image, 109, 255, cv2.THRESH_BINARY_INV)

   im2, ctrs, hier = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   #sort contours
   sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0], reverse=True)



#creating objects - so we coult hold a few arguments that connected together in the same variable

   class contur:
      def __init__(self, x, y, w, h):
         self.x_start = x
         self.y_start = y
         self.x_end = x + w
         self.y_end = y + h

   class charInfo:
      def __init__(self,img_b, conturHight):
         self.image_letter = img_b
         self.conturH = conturHight

   letters_images = list()
   new_ctr = list()

   for j, ctr in enumerate(sorted_ctrs):
      x, y, w, h = cv2.boundingRect(ctr)
      c = contur(x, y, w, h)
      new_ctr.append(c)


   length = len(new_ctr)

   i = 0
   while i < length:
      x, y, w, h = cv2.boundingRect(sorted_ctrs[i])

      if h > 3:
         canvas = np.ones_like(word_image)
         canvas.fill(255)
         cv2.drawContours(canvas, sorted_ctrs, i, (0, 0, 0), 3)

         if i < length - 1 and new_ctr[i].x_start >= new_ctr[i + 1].x_start and new_ctr[i].x_end <= new_ctr[i + 1].x_end:
            Y_end_bigger = max(new_ctr[i].y_end, new_ctr[i + 1].y_end)
            cv2.drawContours(canvas, sorted_ctrs, i + 1, (0, 0, 0), 3)

            if union_left_ctr(new_ctr[i], new_ctr[i+1], canvas) == 0:
               roi = canvas[y:y + h, x:x + w]
               roiriginal = word_image[y:y + h, x:x + w]
            else:
               roi = canvas[new_ctr[i + 1].y_start:Y_end_bigger, new_ctr[i + 1].x_start:new_ctr[i + 1].x_end]
               roiriginal = word_image[new_ctr[i + 1].y_start:Y_end_bigger, new_ctr[i + 1].x_start:new_ctr[i + 1].x_end]
               i += 1
         else:
            roi = canvas[y:y + h, x:x + w]
            roiriginal = word_image[y:y + h, x:x + w]
         roi = draw_white_cells(roiriginal, roi)

         img_b = np.pad(roi, pad_width=10, mode='constant', constant_values=255)
         letterInfo = charInfo(img_b, roi.shape[0])

         # cv2.imshow(str(i), img_b)
         # cv2.waitKey(0)
         # cv2.destroyAllWindows()
         letters_images.append(letterInfo)
      i+=1
   return letters_images
