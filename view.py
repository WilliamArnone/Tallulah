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
            self.root.grid_columnconfigure(0, weight=20)
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_rowconfigure(1, weight=1)

            properties_frame = LabelFrame(self.root, text = "Properties", padx=3, pady=3)
            properties_frame.grid(row=0, column=1, sticky=W+E+S+N)
        
            indipendence_frame = Frame(self.root, bg="gray")
            indipendence_frame.grid(row=1, column=1, sticky=W+E+S+N)

            indipendence_title = Label(indipendence_frame, text="INDIPENDENCE:")
            indipendence_title.pack(fill="x")

            self.indipendence_text = Text(indipendence_frame, width=40)
            self.indipendence_text.pack(side=LEFT, fill="both", expand=True)

            scrollbar = Scrollbar(indipendence_frame, command=self.indipendence_text.yview)
            scrollbar.pack(side=RIGHT, fill='y')
            
            self.indipendence_text['yscrollcommand'] = scrollbar.set
            
            # initialize checkboxes
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

            check_button = Button(properties_frame, text="Check", command=lambda:self.CheckProperties(properties))
            check_button.pack()
        
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

        #clears the indipendence string
        self.indipendence_text.configure(state='normal')
        self.indipendence_text.delete('1.0', END)
        self.indipendence_text.insert('end', self.controller.graph.GetIndipendenceString())
        self.indipendence_text.configure(state='disabled')

        
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

    def PopUpWindow(self, log, errors):
        """Create a new window with the log infos"""
        root = Tk()
        root.title("Log")

        frame = Frame(root)
        frame.pack(fill="both", expand=True)

        log_text = Text(frame)
        
        char_counter = 0

        #sets all the colors
        log_text.tag_configure("black", foreground="#000000")
        log_text.tag_configure("red", foreground="#B20000")
        log_text.tag_configure("green", foreground="#007500")
        log_text.tag_configure("blue", foreground="#0000A3")

        #the errors are in the form (text, color)
        #color is a string id from the previously defined tags
        for text, color in log:
            log_text.insert('end', text)
            length = len(text)
            log_text.tag_add(color, '1.0+'+str(char_counter)+'c', '1.0+'+str(char_counter+length)+'c')
            char_counter += length


        log_text.pack(side=LEFT, fill='both', expand=True)
        scrollbar = Scrollbar(frame, command=log_text.yview)
        scrollbar.pack(side=RIGHT, fill='y')

        log_text['yscrollcommand'] = scrollbar.set
        log_text.configure(state='disabled')

        btn = Button(root, text="Save", command=lambda: self.SaveLog(log))
        btn.pack(side=LEFT, fill="x", expand=True)

        btn = Button(root, text="Apply", command=lambda: self.ForceProperties(errors))
        btn.pack(side=RIGHT, fill="x", expand=True)

        root.mainloop()

    def SaveLog(self, log):
        """Save text as a txt file"""
        dialog = filedialog.asksaveasfile(mode='w', title="Save Log", defaultextension=".txt", filetypes=(("Text FIle", "*.txt"), ("all files", "*.*")))
        if dialog is None: 
            return
        text2save = ""
        for text, color in log: text2save+=text

        with open(dialog.name, 'w', encoding='utf-8') as f:
            f.write(text2save)
            f.close() 

    def ForceProperties(self, errors):
        """Check properties and save a DOT file with the changes"""
        graph = self.controller.ForceProperties(errors)
        text2save = graph.ToString()
        dialog = filedialog.asksaveasfile(mode='w', title="Save Graph", defaultextension=".dot", filetypes=(("DOT graph", "*.gv *.dot"), ("all files", "*.*")))
        if dialog is None: 
            return
        dialog.write(text2save)
        dialog.close() 