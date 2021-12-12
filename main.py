from view import View
from controller import Controller
from tkinter import Tk
#from PIL import ImageTk, Image


def main():
    #icon = ImageTk.PhotoImage(Image.open("icons/logo-ico.ico"))
    #root.tk.call("wm","iconphoto",root._w,icon)
    c = Controller()
    root = Tk()
    View(root, c)
    root.mainloop()


if __name__ == '__main__':
    main()