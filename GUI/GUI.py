from tkinter import *
import tkinter as tk
from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Style
from tkinter import Label, Tk
from functools import partial
from PIL import Image, ImageTk
from tkinter import filedialog


class Program(Frame):

    def __init__(self):
        super().__init__()
        self.guiView()


    def guiView(self):

        lbl_output = tk.Label(self.master, text=": פלט (טקסט מוקלד)", bg="white", font=("david", 16))
        lbl_output.place(x=700, y=60, anchor=NE)

        area = Text(self.master, height=30.1, width=67, font='david')
        # area.insert(tk.END,"alooooooooooooooooooooooo")
        area.place(x =400, y =400, anchor="center")

        save_btn = Button(self.master, text="TXT שמור כקובץ ")
        save_btn.place(x=430, y=720, anchor=NE)

        close_btn = Button(self.master, text="סגור", command=self.master.destroy)
        close_btn.place(x=100, y=800, anchor=NE)


    ########################################################################


        #init - adding an example image
        im = Image.open("Untitled.jpg")
        im = im.resize((600, 600), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(im)
        myvar = Label(self.master, image=tkimage)
        myvar.image = tkimage
        myvar.place(relx=.5, x=400, y=400, anchor="center")


        browse_btn = Button(self.master, text="בחר תמונה שברצונך להמיר")
        browse_btn.place(relx=1, x=-300, y=60, anchor=NE)

        convert_btn = Button(self.master, text="בצע המרה", state="disable")
        convert_btn.place(relx=1, x=-250, y=720, anchor=NE)


        # add functionality to the view
        browse_btn.bind('<Button-1>', self.hello)


    def hello(self, event=None):
        path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg'), ("PNG File", '.png'), ("TIF File", '.TIF'), ("JPEG File", '.jpeg')])
        im = Image.open(path)
        im = im.resize((600, 600), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(im)
        myvar = Label(self.master, image=tkimage)
        myvar.image = tkimage
        myvar.place(relx=.5, x=400, y=400, anchor="center")
        self.area.insert(tk.END,"alooooooooooooooooooooooo")






def main():

    # blank window
    root = Tk()
    # this will be the title of the window
    root.title("Hebrew Handwriting Recognition")

    root.state('zoomed')
    root.resizable(False, False)
    program = Program()

    # this is for kiping the window open until we press exit (X)
    root.mainloop()


if __name__ == '__main__':
    main()






# # position a label on the frame using place(x, y)
# # place(x=0, y=0) would be the upper left frame corner
# label = tk.Label(frame, text="על מנת....")
# label.place(x=800, y=30)
# # put the button below the label, change y coordinate
# button = tk.Button(frame, text="Press me", bg='yellow')
# button.place(x=20, y=60)
# print (root.winfo_width())


# self.columnconfigure(1, weight=1)
# self.columnconfigure(3, pad=7)
# self.rowconfigure(3, weight=1)
# self.rowconfigure(5, pad=7)
#
# lbl = tk.Label(left_frame, text=" :באפשרותך ליצא את הפלט ל", bg="lightsteelblue")
# lbl.grid(sticky=E, pady=4, padx=5)


# hbtn = Button(left_frame, text="ביטול")
# hbtn.grid(row=8, column=0, padx=1)



    # # set the root window's height, width and x,y position
    # # x and y are the coordinates of the upper left corner
    # w = 1000
    # h = 700
    # x = 150
    # y = 50
    # # use width x height + x_offset + y_offset (no spaces!)
    # root.geometry(('{}x{}').format(w, h))


    # frame = tk.Frame(root, bg='lightsteelblue')
    # frame.pack(fill='both', expand=True)

    #
    # def hello(self, event, param):
    #     path = filedialog.askopenfilename(
    #         filetypes=[("Image File", '.jpg'), ("PNG File", '.png'), ("TIF File", '.TIF'), ("JPEG File", '.jpeg')])
    #     im = Image.open(path)
    #     im = im.resize((600, 600), Image.ANTIALIAS)
    #     tkimage = ImageTk.PhotoImage(im)
    #     myvar = Label(param, image=tkimage)
    #     myvar.image = tkimage
    #     myvar.place(relx=.5, rely=.5, anchor="center")
    #
    # class Program(Frame):
    #
    #     def __init__(self):
    #         super().__init__()
    #         self.guiView()
    #
    #     def guiView(self):
    #         left_frame = tk.Frame(self.master, bg='DarkSeaGreen4')
    #         left_frame.grid(row=0, column=0, sticky="nsew")
    #
    #         lbl_output = tk.Label(left_frame, text=": פלט (טקסט מוקלד)", bg="DarkSeaGreen4", font=("david", 16))
    #         lbl_output.place(relx=1, x=-87, y=82, anchor=NE)
    #
    #         area = Text(left_frame, height=30.1, width=67, font='david')
    #         # area.insert(tk.END,"alooooooooooooooooooooooo")
    #         area.place(relx=.5, rely=.5, anchor="center")
    #
    #         save_btn = Button(left_frame, text="TXT שמור כקובץ ")
    #         save_btn.place(relx=1, x=-340, y=750, anchor=NE)
    #
    #         close_btn = Button(left_frame, text="סגור", command=self.master.destroy)
    #         close_btn.place(relx=1, x=-680, y=800, anchor=NE)
    #
    #         ########################################################################
    #
    #         right_frame = tk.Frame(self.master, bg='DarkSeaGreen3')
    #         right_frame.grid(row=0, column=1, sticky="nsew")
    #
    #         # init - adding an example image
    #         im = Image.open("Untitled.jpg")
    #         im = im.resize((600, 600), Image.ANTIALIAS)
    #         tkimage = ImageTk.PhotoImage(im)
    #         myvar = Label(right_frame, image=tkimage)
    #         myvar.image = tkimage
    #         myvar.place(relx=.5, rely=.5, anchor="center")
    #
    #         # give each frame half window screen
    #         self.master.grid_columnconfigure(0, weight=1, uniform="group1")
    #         self.master.grid_columnconfigure(1, weight=1, uniform="group1")
    #         self.master.grid_rowconfigure(0, weight=1)
    #
    #         browse_btn = Button(right_frame, text="בחר תמונה שברצונך להמיר")
    #         browse_btn.place(relx=1, x=-300, y=70, anchor=NE)
    #
    #         convert_btn = Button(right_frame, text="בצע המרה", state="disable")
    #         convert_btn.place(relx=1, x=-87, y=12, anchor=NE)
    #
    #         # add functionality to the view
    #         browse_btn.bind('<Button-1>', partial(hello, param=right_frame, event=NONE))
    #
    #         def hello(self, event, param):
    #             path = filedialog.askopenfilename(
    #                 filetypes=[("Image File", '.jpg'), ("PNG File", '.png'), ("TIF File", '.TIF'),
    #                            ("JPEG File", '.jpeg')])
    #             im = Image.open(path)
    #             im = im.resize((600, 600), Image.ANTIALIAS)
    #             tkimage = ImageTk.PhotoImage(im)
    #             myvar = Label(param, image=tkimage)
    #             myvar.image = tkimage
    #             myvar.place(relx=.5, rely=.5, anchor="center")
    #
    #
    # def main():
    #
    #     # blank window
    #     root = Tk()
    #     # this will be the title of the window
    #     root.title("Hebrew Handwriting Recognition")
    #
    #     root.state('zoomed')
    #     root.resizable(False, False)
    #     program = Example()
    #
    #     # this is for kiping the window open until we press exit (X)
    #     root.mainloop()
    #
    #
    # if __name__ == '__main__':
    #     main()
    #
    #
