import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.geometry("550x355")
        self.resizable(False, False)

        # Widgets
        #self.navbar = NavBar(self)
        #self.config(menu=self.navbar)
        self.homepage = Homepage(self)
        #self.right = RightFrame(self)
        #self.homepage.place_forget()

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

        parent.config(menu=self)

class Homepage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        name = tk.Label(self, 
                        text="ZeText", 
                        font=("Helvatica", "40"), 
                        fg="#4f555e")
        name.pack(pady=(0, 9))

        new_file = tk.Button(self, 
                             text="New File",
                             bd=0,
                             relief=tk.FLAT,
                             bg="#33b0ed",
                             activebackground="#46b5ec",
                             padx=4,
                             width=22,
                             height=2,
                             command=self.new_file
                             )
        new_file.pack(pady=6)

        open_file = tk.Button(self, 
                             text="Open File",
                             bd=0,
                             relief=tk.FLAT,
                             bg="#33b0ed",
                             activebackground="#46b5ec",
                             padx=4,
                             width=22,
                             height=2,
                             command=self.open_file
                             )
        open_file.pack(pady=6)

        open_folder = tk.Button(self, 
                             text="Open Folder",
                             bd=0, 
                             relief=tk.FLAT,
                             bg="#33b0ed",
                             activebackground="#46b5ec",
                             padx=4,
                             width=22,
                             height=2,
                             command=self.open_folder
                             )
        open_folder.pack(pady=6)

        self.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def new_file(self):
        self.place_forget()
        RightFrame(self.parent)
        self.parent.config(menu=NavBar(self.parent))
        self.parent.resizable(True, True)
        self.parent.minsize(350, 800)
        
    def open_file(self):
        pass
        
    def open_folder(self):
        pass

    def remove(self):
        self.place_forget()

class RightFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.output_window_status = "visible"

        # Text area(line numbers and text widget)
        text_area = tk.Frame(self, bd=0, relief=tk.FLAT).pack(expand=True, fill=tk.BOTH)

        line_nums = tk.Text(text_area,
                            highlightthickness=0,
                            bd=0,
                            width=5,
                            relief=tk.FLAT,
                            state=tk.DISABLED,
                            font=("JetBrains Mono", 15)
                            )
        line_nums.tag_configure("right", justify="right")
        line_nums.pack(side=tk.LEFT, fill=tk.BOTH, anchor="n")

        editor = tk.Text(text_area,
                         highlightthickness=0,
                         bd=0,
                         relief=tk.FLAT,
                         wrap="none",
                         undo=True,
                         autoseparators=True,
                         font=("JetBrains Mono", 15)
                         )
        editor.pack(expand=True, fill=tk.BOTH, padx=(5, 0))

        # Output area(output window and toggle button)
        output_area = tk.Frame(self, bd=0, relief=tk.FLAT).pack(side=tk.BOTTOM, fill=tk.BOTH)

        output_toggle = tk.Button(output_area, 
                                  text="OUTPUT ⮟", 
                                  anchor="w", 
                                  bd=0, 
                                  relief=tk.FLAT, 
                                  command=lambda: self.toggle_output(output_window, output_toggle))
        output_toggle.pack(fill=tk.BOTH)

        output_window = tk.Text(output_area,
                                height=9,
                                highlightthickness=0,
                                bd=0,
                                relief=tk.FLAT,
                                state=tk.DISABLED,
                                font=("JetBrains Mono", 13), bg="red")
        output_window.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    def toggle_output(self, widget_1, widget_2):
        if self.output_window_status == "visible":
           widget_1.pack_forget()
           widget_2.config(text="OUTPUT ⮝")
           self.output_window_status = "hidden"
           
        elif self.output_window_status == "hidden":
            widget_1.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            widget_2.config(text="OUTPUT ⮟")
            self.output_window_status = "visible"

class LeftFrame(tk.Frame):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    App("ZeText Rewrite")
 