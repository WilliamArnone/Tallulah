import os
import tkinter as ttk

class View(ttk.Frame):
    controller = None
    root = None

    def __init__(self, root, controller):
        super().__init__(root)
        #not in this view
        #root.protocol("WM_DELETE_WINDOW", self.v_on_closing)
        self.controller = controller
        self.root = root
        self.initUI()

    def initUI(self):
        self.grid()
        ttk.Label(self, text="Hello World!").grid(column=1, row=0, columnspan=5, rowspan=3)
        ttk.Button(self, text="Quit", command=self.root.destroy).grid(column=1, row=1, rowspan=3)
