import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.geometry("550x355")
        self.resizable(False, False)

        # Widgets
        self.navbar = NavBar(self)
        #self.config(menu=self.navbar)
        self.homepage = Homepage(self)

        self.mainloop()

class NavBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        # File menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="New File")
        file_menu.add_command(label="New Window")
        file_menu.add_separator()
        file_menu.add_command(label="Open File")
        file_menu.add_command(label="Open Folder")
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...")
        file_menu.add_separator()
        file_menu.add_command(label="Close Window", command=exit)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=exit)
        self.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(self, tearoff=False)
        edit_menu.add_command(label="Select All")
        self.add_cascade(label="Edit", menu=edit_menu)

class Homepage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        name = tk.Label(self, 
                        text="ZeText", 
                        font=("Helvatica", "40"), 
                        fg="#4f555e")
        name.pack(pady=(0, 9))

        new_file = tk.Button(self, 
                             text="New File", 
                             relief=tk.FLAT,
                             bg="#33b0ed",
                             activebackground="#46b5ec",
                             padx=4,
                             width=22,
                             height=2,
                             command=NotImplemented
                             )
        new_file.pack(pady=6)

        open_file = tk.Button(self, 
                             text="Open File", 
                             relief=tk.FLAT,
                             bg="#33b0ed",
                             activebackground="#46b5ec",
                             padx=4,
                             width=22,
                             height=2,
                             command=NotImplemented
                             )
        open_file.pack(pady=6)

        open_folder = tk.Button(self, 
                             text="Open File", 
                             relief=tk.FLAT,
                             bg="#33b0ed",
                             activebackground="#46b5ec",
                             padx=4,
                             width=22,
                             height=2,
                             command=NotImplemented
                             )
        open_folder.pack(pady=6)

        self.place(relx=.5, rely=.5, anchor=tk.CENTER)


        
    
    def test(self):
        pass
        
    

App("ZeText Rewrite")