import tkinter as ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image

from controller import Controller
from properties.BTI import BTI
from properties.CPI import CPI
from properties.IRE import IRE
from properties.SP import SP
from properties.WF import WF

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

        buttonLoad = ttk.Button(self.root, text="Open DOT file", command=self.OpenFile)
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
            sp = Checkbutton(properties_frame, text=SP.name, variable=properties['SP'])
            sp.pack(anchor=W)

            properties['BTI']=BooleanVar()
            bti = Checkbutton(properties_frame, text=BTI.name, variable=properties['BTI'])
            bti.pack(anchor=W)

            properties['WF']=BooleanVar()
            wf = Checkbutton(properties_frame, text=WF.name, variable=properties['WF'])
            wf.pack(anchor=W)

            properties['CPI']=BooleanVar()
            cpi = Checkbutton(properties_frame, text=CPI.name, variable=properties['CPI'])
            cpi.pack(anchor=W)

            properties['IRE']=BooleanVar()
            ire = Checkbutton(properties_frame, text=IRE.name, variable=properties['IRE'])
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
        errors = self.controller.CheckProperties(properties)
        popUp = Toplevel(self.root)
        popUp.geometry("800x500")
        popUp.title("Log")

        main = Frame(popUp)
        main.pack(fill="both", expand=True)

        canvas = Canvas(main)
        canvas.pack(side=LEFT, fill="both", expand=True)

        scrollbar = Scrollbar(main, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')

        canvas.configure(yscrollcommand = scrollbar.set)

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))

        # --- put frame in canvas ---

        frame = Frame(canvas)
        canvas.create_window((0,0), window=frame, anchor='nw')
        canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        color = {}
        color["black"] = "#000000"
        color["red"] = "#B20000"
        color["green"] = "#007500"
        color["blue"] = "#0000A3"

        errors_frame = Frame(frame)
        errors_frame.pack(side=LEFT, anchor=N+W)
        check_values = {}
        for property_id in errors:

            check_values[property_id]=[]

            #prints property name
            error_frame = Frame(errors_frame)
            error_frame.pack(fill='x', expand=True)
            name = self.controller.GetPropertyName(property_id)
            Label(error_frame, text=name, foreground=color["blue"]).grid(row=0, column=0)

            #label if there's no error
            if len(errors[property_id])==0:
                error_frame = Frame(errors_frame)
                error_frame.pack(fill='x', expand=True)
                Label(error_frame, text=property_id+" holds", foreground=color["green"]).grid(row=0, column=0)

            #warning label: there are some error that cannot be removed
            if not all(self.controller.IsErrorApplyable(property_id, error) for error in errors[property_id]):
                error_frame = Frame(errors_frame)
                error_frame.pack(fill='x', expand=True)
                Label(error_frame, text=property_id+" CANNOT BE PERFORMED!", foreground=color["red"]).grid(row=0, column=0)

            #label for each error
            for error in errors[property_id]:
                check_var = BooleanVar()
                applyable = self.controller.IsErrorApplyable(property_id, error)
                check_values[property_id].append(check_var)

                error_frame = Frame(errors_frame)
                error_frame.pack(anchor=W, fill='x', expand=True)

                Checkbutton(error_frame, variable=check_var, 
                    state="normal" if applyable else "disabled").grid(row=0, column=0, sticky=W)
                
                check_var.set(applyable)

                logs = self.controller.GetLog(property_id, error)
                for index in range(len(logs)):
                    text, col = logs[index]
                    lbl = Label(error_frame, text=text, foreground=color[col])
                    lbl.grid(row=0, column=index+1, sticky=W)

                    
        btn = Button(popUp, text="Save", command=lambda: self.SaveLog(errors))
        btn.pack(side=LEFT, fill="x", expand=True)

        btn = Button(popUp, text="Apply Selected", command=lambda: self.ForceProperties(errors, check_values))
        btn.pack(side=RIGHT, fill="x", expand=True)
        
    def SaveLog(self, errors):
        """Save log as a txt file"""
        dialog = filedialog.asksaveasfile(mode='w', title="Save Log", defaultextension=".txt", filetypes=(("Text FIle", "*.txt"), ("all files", "*.*")))
        if dialog is None: 
            return
        text2save = ""
        for property_id in errors:

            text2save+=self.controller.GetPropertyName(property_id)

            if len(errors[property_id])==0: text2save+=property_id+' holds'
            for error in errors[property_id]:
                for text, color in self.controller.GetLog(property_id, error): 
                    text2save+=text+' '
                text2save+='\n'

        with open(dialog.name, 'w', encoding='utf-8') as f:
            f.write(text2save)
            f.close() 

    def ForceProperties(self, errors, check):
        """Check properties and save a DOT file with the changes"""
        graph = self.controller.ForceProperties(errors, check)
        text2save = graph.ToString()
        dialog = filedialog.asksaveasfile(mode='w', title="Save Graph", defaultextension=".dot", filetypes=(("DOT graph", "*.gv *.dot"), ("all files", "*.*")))
        if dialog is None: 
            return
        dialog.write(text2save)
        dialog.close() 