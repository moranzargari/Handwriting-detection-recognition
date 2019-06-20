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
from tkinter import messagebox


# blank window
root = Tk()
# this will be the title of the window
root.title("Hebrew Handwriting Recognition")

root.state('zoomed')
root.resizable(False, False)

s = Style()
s.configure('my.TButton', font=('Helvetica', 12))


C = Canvas(root, bg="blue", height=250, width=300)
filename = Image.open("back_img.jpg")
filename = ImageTk.PhotoImage(filename)

background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()


lbl_output = tk.Label(root, text=": פלט (טקסט מוקלד)", font=("Helvetica", 14))
lbl_output.place(x=700, y=68, anchor=NE)

area = Text(root, height=30.1, width=67, font='david',borderwidth=0.5, relief="solid")
area.place(x =400, y =400, anchor="center")

save_btn = Button(root, text="TXT שמור כקובץ ", state="disable", style='my.TButton')
save_btn.place(x=430, y=720, anchor=NE)

close_btn = Button(root, text="סגור", command=root.destroy, style='my.TButton')
close_btn.place(x=150, y=800, anchor=NE)

#init - adding an example image for instructions
img = Image.open("Untitled.png")
im = img.resize((600, 600), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)
myvar = Label(root, image=tkimage,borderwidth=0.5, relief="solid")
myvar.image = tkimage
myvar.place(relx=.5, x=400, y=400, anchor="center")


def convert_to_text(imageToConvert):
    area.delete('1.0', END)
    imageToConvert = np.asarray(imageToConvert)
    area.insert(tk.END, convertImg.convert_the_image(imageToConvert))
    save_btn['state'] = "enable"
    save_btn['command'] = lambda: save_txt()



def add_image_to_convert(img):
    im = img.resize((600, 600), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(im)
    myvar = Label(root, image=tkimage)
    myvar.image = tkimage
    myvar.place(relx=.5, x=400, y=400, anchor="center")


def upload_img():
    path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg'), ("PNG File", '.png'), ("TIF File", '.TIF'),
                                                 ("JPEG File", '.jpeg')])
    imageToConvert = Image.open(path)
    add_image_to_convert(imageToConvert)
    convert_btn['state'] = "enable"
    convert_btn['command'] = lambda: convert_to_text(imageToConvert)


def save_txt():
    text = area.get("1.0", END)  # get the text from text area
    name = filedialog.asksaveasfilename(
        initialdir="C:",
        title="Choose your file",
        filetypes=(
            ("Text Files", "*.txt"),
            ),
        defaultextension=''
    )
    try:
        f = open(name, "w")
        f.write(text)
        f.close()
        messagebox.showinfo("הודעה", "!התמונה הומרה לקובץ טקסט בהצלחה \n :הקובץ נשמר ב \n " + str(name))
    except:
        pass

browse_btn = Button(root, text="בחר תמונה שברצונך להמיר", command=upload_img, style='my.TButton')
browse_btn.place(relx=1, x=-270, y=60, anchor=NE)


convert_btn = Button(root, text="בצע המרה", state="disable",  style='my.TButton')
convert_btn.place(relx=1, x=-300, y=720, anchor=NE)


root.mainloop()
