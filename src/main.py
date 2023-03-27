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
        self.notifaction = Notification(self)
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
                             cursor="hand2",
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
                             cursor="hand2",
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
                             cursor="hand2",
                             command=self.open_folder
                             )
        open_folder.pack(pady=6)

        self.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def new_file(self):
        self.place_forget()
        RightFrame(self.parent)
        self.parent.config(menu=NavBar(self.parent))
        self.parent.resizable(True, True)
        self.parent.geometry("800x350")
        #self.parent.minsize(350, 800)
        
    def open_file(self):
        pass
        
    def open_folder(self):
        pass

    def remove(self):
        self.place_forget()

class RightFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.output_window_status = "visible"

        self.pane = tk.PanedWindow(self,
                            bd=0,
                            orient=tk.VERTICAL)
        self.pane.pack(fill=tk.BOTH, expand=True)

        # Output area(output toggle button and output window)
        self.output_area = tk.Frame(self,
                               bd=0,
                               relief=tk.FLAT)
        self.output_area.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.output_toggle_button = tk.Button(self.output_area,
                                         text="OUTPUT ⮟",
                                         anchor="w",
                                         bd=0,
                                         relief=tk.FLAT,
                                         cursor="hand2",
                                         command=self.toggle_output)
        self.output_toggle_button.pack(fill=tk.BOTH)

        self.output = tk.Text(self.output_area,
                         highlightthickness=0,
                         bd=0,
                         relief=tk.FLAT,
                         state=tk.DISABLED,
                         font=("JetBrains Mono", 12))
        self.output.pack(fill=tk.BOTH, expand=True)

        # Text area(line numbers and the main text widget)
        self.text_area = tk.Frame(self,
                             bd=0,
                             relief=tk.FLAT)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        
        self.line_numbers = tk.Text(self.text_area,
                               highlightthickness=0,
                               bd=0,
                               relief=tk.FLAT,
                               state=tk.DISABLED,
                               width=5,
                               font=("JetBrains Mono", 13))
        self.line_numbers.tag_configure("right", justify="right")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.BOTH, anchor="n")

        self.editor = tk.Text(self.text_area,
                         highlightthickness=0,
                         bd=0,
                         relief=tk.FLAT,
                         wrap="none",
                         undo=True,
                         autoseparators=True,
                         font=("JetBrains Mono", 13))
        self.editor.pack(expand=True, fill=tk.BOTH, padx=(5,0))

        self.pane.add(self.text_area)
        self.pane.add(self.output_area)
        self.pane.paneconfig(self.output_area, minsize=50)
        self.pane.paneconfig(self.text_area, minsize=50)

        # Bindings
        self.parent.bind("<MouseWheel>", self.on_mousewheel_move)
        self.parent.bind("<Key>", self.generate_line_numbers)

        self.pack(expand=True, fill=tk.BOTH)
    
    # Commands
    def toggle_output(self):
        if self.output_window_status == "visible":
            self.pane.remove(self.output_area)
            self.output.pack_forget()
            self.output_area.pack(side=tk.BOTTOM, fill=tk.BOTH)

            self.output_toggle_button.config(text="OUTPUT ⮝")
            self.output_window_status = "hidden"
        
        elif self.output_window_status == "hidden":
            self.output.pack(fill=tk.BOTH, expand=True)
            self.output_toggle_button.config(text="OUTPUT ⮟")

            self.pane.add(self.output_area)
            self.pane.paneconfig(self.output_area, minsize=50)

            self.output_window_status = "visible"
    
    def generate_line_numbers(self, e):
        numbers = ""
        for i in range(int(self.editor.index("end").split(".")[0])-1):
            numbers += " " + str(i + 1) + " \n"
    
        self.line_numbers.configure(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", numbers[:-1])
        self.line_numbers.tag_add("right", 1.0, "end")
        self.line_numbers.configure(state=tk.DISABLED)
        self.line_numbers.yview_moveto(float(self.editor.yview()[0]))
    
    def on_mousewheel_move(self, e):
        self.line_numbers.yview_moveto(float(self.editor.yview()[0]))

class LeftFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

class Notification(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

if __name__ == "__main__":
    App("ZeText Rewrite")
 