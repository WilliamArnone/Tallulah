import tkinter as ttk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

class View:
    controller = None
    root = None
    widgets = []

    def __init__(self, root, controller):
        #not in this view
        #root.protocol("WM_DELETE_WINDOW", self.v_on_closing)
        self.controller = controller
        self.root = root

        menu_bar = Menu(root)
        file_menu = Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Open File",compound=LEFT, command= self.open_file)
        menu_bar.add_cascade(label="Open",menu=file_menu)
        root.config(menu=menu_bar)

        self.startUI()

    def startUI(self):
        self.clearScreen()
        self.root.geometry("350x250")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        buttonLoad = ttk.Button(self.root, text="Open .DOT file", command=self.open_file)
        buttonLoad.grid(row=0, column=0, sticky=S, pady=5)
        buttonExit  = ttk.Button(self.root, text="Quit", command=self.root.destroy)
        buttonExit.grid(row=1, column=0, sticky=N, pady=5)

        self.widgets.append(buttonLoad)
        self.widgets.append(buttonExit)

    def mainUI(self, path):
        self.clearScreen()
        self.root.geometry("1000x800")
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.controller.setPath(path)

        imagePath = self.controller.getGraphImage()
        image = ImageTk.PhotoImage(Image.open(imagePath))
        lblImage = Label(image=image)
        lblImage.image=image
        lblImage.grid(row=0, column=0, sticky=W)
        self.widgets.append(lblImage)

        frame = LabelFrame(self.root, text = "Properties", padx=10, pady=10)
        frame.grid(row=0, column=1, sticky=W+E+S+N)
        self.widgets.append(frame)

        properties = {}

        properties['SP']=BooleanVar()
        sp = Checkbutton(frame, text="SP - Square Property", variable=properties['SP'])
        sp.pack(anchor=W)
        self.widgets.append(sp)

        properties['BTI']=BooleanVar()
        bti = Checkbutton(frame, text="BTI - Backward Transitions are Indipendent", variable=properties['BTI'])
        bti.pack(anchor=W)
        self.widgets.append(bti)

        properties['WF']=BooleanVar()
        wf = Checkbutton(frame, text="WF - Well-Foundedness", variable=properties['WF'])
        wf.pack(anchor=W)
        self.widgets.append(wf)

        btnCheck = Button(frame, text="Check", command=lambda:self.checkProperties(properties))
        btnCheck.pack()
        self.widgets.append(btnCheck)

        btnBuild = Button(frame, text="Build", command=lambda:self.generateProperties(properties))
        btnBuild.pack()
        self.widgets.append(btnBuild)


    def clearScreen(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []

    def open_file(self):
        path = filedialog.askopenfilename(initialdir=".",
        		                              filetypes=(("DOT graph", "*.gv *.dot"), ("all files", "*.*")),
        		                              title="Choose a file."
        		                              )
        if path == '': return
        self.mainUI(path)

    def checkProperties(self, properties):
        log = self.controller.checkProperties(properties)
        logString = ''

        for msg in log: logString = logString + msg + '\n'

        self.top = Toplevel()
        self.top.title("Log")
        label = Label(self.top,text=logString,justify=LEFT,padx=15,pady=15)
        label.pack()

    def generateProperties(self, properties):
        text2save = self.controller.generateProperties(properties)
        dialog = filedialog.asksaveasfile(mode='w', title="Save Graph", defaultextension=".dot", filetypes=(("DOT graph", "*.gv *.dot"), ("all files", "*.*")))
        if dialog is None: 
            return
        dialog.write(text2save)
        dialog.close() 