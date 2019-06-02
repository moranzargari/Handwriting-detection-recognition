from tkinter import *
import tkinter as tk
from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Style
from tkinter import Label, Tk
from PIL import Image, ImageTk
from tkinter import filedialog





# # position a label on the frame using place(x, y)
# # place(x=0, y=0) would be the upper left frame corner
# label = tk.Label(frame, text="על מנת....")
# label.place(x=800, y=30)
# # put the button below the label, change y coordinate
# button = tk.Button(frame, text="Press me", bg='yellow')
# button.place(x=20, y=60)
# print (root.winfo_width())



class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):


        left_frame = tk.Frame(self.master, bg='lightsteelblue')
        left_frame.grid(row=0, column=0, sticky="nsew")

        lbl = tk.Label(left_frame, text=": פלט (טקסט מוקלד)", bg="lightsteelblue")
        lbl.grid(sticky=E, pady=4, padx=5)

        area = Text(left_frame, height=40)
        # area.insert(tk.END,"alooooooooooooooooooooooo")
        area.grid(row=5, column=0, sticky=S+N, padx=55, pady=35)

        cbtn = Button(left_frame, text="TXT שמור כקובץ ")
        cbtn.grid(row=7, column=0, pady=1)



    ########################################################################

        right_frame = tk.Frame(self.master, bg='gray')
        right_frame.grid(row=0, column=1, sticky="nsew")

        self.master.grid_columnconfigure(0, weight=1, uniform="group1")
        self.master.grid_columnconfigure(1, weight=1, uniform="group1")
        self.master.grid_rowconfigure(0, weight=1)
        browse = Button(right_frame, text="בחר תמונה")
        browse.place(relx=1, x=-7, y=12, anchor=NE)

        cbtn = Button(right_frame, text="בצע המרה")
        cbtn.place(relx=1, x=-87, y=12, anchor=NE)

        cbtn = Button(right_frame, text="ביטול")
        cbtn.place(relx=1, x=-167, y=12, anchor=NE)

        def hello(event):
            path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg')])
            im = Image.open(path)
            im = im.resize((500, 500), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(im)
            myvar = Label(right_frame, image=tkimage)
            myvar.image = tkimage
            myvar.place(relx=.5, rely=.5, anchor="center")

        browse.bind('<Button-1>', hello)

        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(3, pad=7)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=7)
        #
        # lbl = tk.Label(left_frame, text=" :באפשרותך ליצא את הפלט ל", bg="lightsteelblue")
        # lbl.grid(sticky=E, pady=4, padx=5)





        # hbtn = Button(left_frame, text="ביטול")
        # hbtn.grid(row=8, column=0, padx=1)



def main():

    # blank window
    root = Tk()
    # this will be the title of the window
    root.title("Hebrew Handwriting Recognition")

    # # set the root window's height, width and x,y position
    # # x and y are the coordinates of the upper left corner
    # w = 1000
    # h = 700
    x = 150
    y = 50
    # # use width x height + x_offset + y_offset (no spaces!)
    # root.geometry(('{}x{}').format(w, h))


    # frame = tk.Frame(root, bg='lightsteelblue')
    # frame.pack(fill='both', expand=True)

    root.state('zoomed')
    app = Example()
    # this is for kiping the window open until we press exit (X)
    root.mainloop()


if __name__ == '__main__':
    main()
