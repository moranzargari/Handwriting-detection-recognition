from tkinter import *
import tkinter as tk
from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Style





# # position a label on the frame using place(x, y)
# # place(x=0, y=0) would be the upper left frame corner
# label = tk.Label(frame, text="על מנת....")
# label.place(x=800, y=30)
# # put the button below the label, change y coordinate
# button = tk.Button(frame, text="Press me", bg='yellow')
# button.place(x=20, y=60)
# print (root.winfo_width())



class Example(Frame):

    kaki = "jhjhjhjhjh"
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):


        left_frame = tk.Frame(self.master, bg='lightsteelblue')
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        lbl = tk.Label(left_frame, text=": פלט (טקסט מוקלד)", bg="lightsteelblue")
        lbl.grid(sticky=E, pady=4, padx=5)

        area = Text(left_frame, height=40)
        # area.insert(tk.END,"alooooooooooooooooooooooo")
        area.grid(row=5, column=0, sticky=W+S+N)

        cbtn = Button(left_frame, text="TXT שמור כקובץ ")
        cbtn.grid(row=7, column=0, pady=4)

    ########################################################################

        right_frame = tk.Frame(self.master, bg='gray')
        right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


        cbtn = Button(right_frame, text="בחר תמונה")
        cbtn.grid(row=1, column=7, pady=0)

        cbtn = Button(right_frame, text="בצע המרה")
        cbtn.grid(row=2, column=5, pady=0)





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
    # x = 150
    # y = 50
    # # use width x height + x_offset + y_offset (no spaces!)
    # root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    # frame = tk.Frame(root, bg='lightsteelblue')
    # frame.pack(fill='both', expand=True)

    root.state('zoomed')
    app = Example()
    # this is for kiping the window open until we press exit (X)
    root.mainloop()


if __name__ == '__main__':
    main()
