from tkinter import *
import tkinter as tk
from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Style
from tkinter import Label, Tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import convertImg



# blank window
root = Tk()
# this will be the title of the window
root.title("Hebrew Handwriting Recognition")

root.state('zoomed')
root.resizable(False, False)



C = Canvas(root, bg="blue", height=250, width=300)
filename = Image.open("back_img.jpg")
filename = ImageTk.PhotoImage(filename)

background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()


lbl_output = tk.Label(root, text=": פלט (טקסט מוקלד)", font=("david", 14))
lbl_output.place(x=700, y=68, anchor=NE)

area = Text(root, height=30.1, width=67, font='david',borderwidth=0.5, relief="solid")
area.place(x =400, y =400, anchor="center")

save_btn = Button(root, text="TXT שמור כקובץ ")
save_btn.place(x=430, y=720, anchor=NE)

close_btn = Button(root, text="סגור", command=root.destroy)
close_btn.place(x=100, y=800, anchor=NE)

#init - adding an example image for instructions
img = Image.open("Untitled.png")
im = img.resize((600, 600), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)
myvar = Label(root, image=tkimage,borderwidth=0.5, relief="solid")
myvar.image = tkimage
myvar.place(relx=.5, x=400, y=400, anchor="center")




def convert_to_text(imageToConvert):
    imageToConvert = np.asarray(imageToConvert)
    area.insert(tk.END, convertImg.convert_the_image(imageToConvert))

    cancel_convert_btn = Button(root, text="בטל המרה", state="enable")
    cancel_convert_btn.place(relx=1, x=-350, y=720, anchor=NE)


def add_image_to_convert(img):
    im = img.resize((600, 600), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(im)
    myvar = Label(root, image=tkimage)
    myvar.image = tkimage
    myvar.place(relx=.5, x=400, y=400, anchor="center")


def upload_img():
    path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg'), ("PNG File", '.png'), ("TIF File", '.TIF'), ("JPEG File", '.jpeg')])
    imageToConvert = Image.open(path)
    add_image_to_convert(imageToConvert)
    convert_btn['state'] = "enable"
    convert_btn['command'] = lambda: convert_to_text(imageToConvert)



browse_btn = Button(root, text="בחר תמונה שברצונך להמיר", command=upload_img)
browse_btn.place(relx=1, x=-270, y=60, anchor=NE)

convert_btn = Button(root, text="בצע המרה", state="disable")
convert_btn.place(relx=1, x=-250, y=720, anchor=NE)


root.mainloop()
