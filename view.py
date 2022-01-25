import copy
import tkinter as ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image

from controller import Controller

class View:
    controller = None
    root = None
    widgets = []

    def __init__(self, root, controller):
        #not in this view
        #root.protocol("WM_DELETE_WINDOW", self.v_on_closing)
        self.controller = controller
        self.root = root

        self.StartUI()

    def StartUI(self):
        """Set up of the starting page"""
        self.ClearScreen()
        self.root.geometry("350x250")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        buttonLoad = ttk.Button(self.root, text="Open .DOT file", command=self.OpenFile)
        buttonLoad.grid(row=0, column=0, sticky=S, pady=5)
        buttonExit  = ttk.Button(self.root, text="Quit", command=self.root.destroy)
        buttonExit.grid(row=1, column=0, sticky=N, pady=5)

        self.widgets.append(buttonLoad)
        self.widgets.append(buttonExit)

    def MainUI(self, path):
        """Set up the view with the graph and the properties"""

        self.ClearScreen()

        if self.controller.path == None:
            
            menu_bar = Menu(self.root)
            file_menu = Menu(menu_bar, tearoff=False)
            file_menu.add_command(label="Open",compound=LEFT, command= self.OpenFile)
            menu_bar.add_cascade(label="File",menu=file_menu)
            self.root.config(menu=menu_bar)

            # window settings
            self.root.geometry("1000x800")
            self.root.grid_columnconfigure(0, weight=7)
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_rowconfigure(1, weight=1)

            properties_frame = LabelFrame(self.root, text = "Properties", padx=3, pady=3)
            properties_frame.grid(row=0, column=1, sticky=W+E+S+N)

        
            frame_main = Frame(self.root, bg="gray")
            frame_main.grid(row=1, column=1, sticky='news')

            indipendenceLabel = Label(frame_main, text="INDIPENDENCE:")
            indipendenceLabel.pack(fill="x")

            self.canvas = Canvas(frame_main)
            self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)

            scrollbar = Scrollbar(frame_main, command=self.canvas.yview)
            scrollbar.pack(side=RIGHT, fill='y')

            self.canvas.configure(yscrollcommand = scrollbar.set)

            
            # scrolling hanglers
            self.canvas.bind('<Configure>', lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
            self.root.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(-1*(event.delta//120), "units"))

            self.indipency_frame = Frame(self.canvas)
            self.canvas.create_window((0,0), window=self.indipency_frame, anchor='nw')
            
            # initialize check buttons
            properties = {}

            properties['SP']=BooleanVar()
            sp = Checkbutton(properties_frame, text="SP - Square Property", variable=properties['SP'])
            sp.pack(anchor=W)

            properties['BTI']=BooleanVar()
            bti = Checkbutton(properties_frame, text="BTI - Backward Transitions are Indipendent", variable=properties['BTI'])
            bti.pack(anchor=W)

            properties['WF']=BooleanVar()
            wf = Checkbutton(properties_frame, text="WF - Well-Foundedness", variable=properties['WF'])
            wf.pack(anchor=W)

            properties['CPI']=BooleanVar()
            cpi = Checkbutton(properties_frame, text="CPI - Coinitial Propagation of Indipendence", variable=properties['CPI'])
            cpi.pack(anchor=W)

            properties['IRE']=BooleanVar()
            ire = Checkbutton(properties_frame, text="IRE - Independence Respects Events", variable=properties['IRE'])
            ire.pack(anchor=W)

            btnCheck = Button(properties_frame, text="Check", command=lambda:self.CheckProperties(properties))
            btnCheck.pack()
        
        errors = self.controller.Parse(path)

        if errors:
            messagebox.showerror("Error"," ".join(map(str, errors)))
            return

        # graph image
        imagePath = self.controller.GetGraphImage()
        image = ImageTk.PhotoImage(Image.open(imagePath))
        lblImage = Label(image=image)
        lblImage.image=image
        lblImage.grid(row=0, column=0, rowspan=2, sticky=W+E+S+N)
        self.widgets.append(lblImage)

        txtIndipendence = Label(self.indipency_frame, border=0, justify=LEFT, text=self.controller.graph.GetIndipendenceString())
        txtIndipendence.pack(fill="both")
        self.widgets.append(txtIndipendence)

        #updating indipendence label scrollbar
        self.canvas.update()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        
    def ClearScreen(self):
        """Destroy the start ui, or the image of the main ui"""
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []

    def OpenFile(self):
        """Open dot file and set the ui"""
        path = filedialog.askopenfilename(initialdir=".",
        		                              filetypes=(("DOT graph", "*.gv *.dot"), ("all files", "*.*")),
        		                              title="Choose a file."
        		                              )
        if path == '': return
        self.MainUI(path)

    def CheckProperties(self, properties):
        """Check all properties and prints a log"""
        log, errors = self.controller.CheckProperties(properties)
        self.PopUpWindow(log, errors)

    def PopUpWindow(self, text, errors):
        """Create a new window with the log infos"""
        root = Tk()
        root.title("Log")

        canvas = Canvas(root)
        canvas.pack(side=LEFT, fill='both', expand=True)

        scrollbar = Scrollbar(root, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')

        canvas.configure(yscrollcommand = scrollbar.set)

        # scroll handling
        canvas.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
        root.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))

        frame = Frame(canvas)
        canvas.create_window((0,0), window=frame, anchor='nw')

        l = Label(frame, text=text, justify=LEFT, border=0)
        l.pack(fill='both', expand=True)

        btn = Button(frame, text="Save", command=lambda: self.SaveLog(text))
        btn.pack(pady=5)

        btn = Button(frame, text="Apply", command=lambda: self.ForceProperties(errors))
        btn.pack(pady=5)

        root.mainloop()

    def SaveLog(self, text):
        """Save text as a txt file"""
        dialog = filedialog.asksaveasfile(mode='w', title="Save Log", defaultextension=".txt", filetypes=(("Text FIle", "*.txt"), ("all files", "*.*")))
        if dialog is None: 
            return
        dialog.write(text)
        dialog.close() 

    def ForceProperties(self, errors):
        """Check properties and save a DOT file with the changes"""
        text2save = self.controller.ForceProperties(errors)
        dialog = filedialog.asksaveasfile(mode='w', title="Save Graph", defaultextension=".dot", filetypes=(("DOT graph", "*.gv *.dot"), ("all files", "*.*")))
        if dialog is None: 
            return
        dialog.write(text2save)
        dialog.close() 