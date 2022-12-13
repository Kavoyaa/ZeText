from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename, askdirectory
from tkinter.simpledialog import askstring
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import ttk
import subprocess
import time
import os
import imghdr

root = Tk()
root.title("ZeText")
root.minsize(350, 200)

default_file_path = ""
run_command = ""
console_content = ""
console_status = "visible"
theme = "light"
dunno_what_to_name_this = False
mode = ""
current_open_file = ""
tree_status = "visible"
prev = ""
editor_status="visible"

primary_colour = "white"
secondary_colour ="#e3e4ea"
tertiary_colour = ""
text_colour="black"

def theme_widgets():
    global console
    console.configure(fg=text_colour, bg=secondary_colour)
    global console_toggle_button
    console_toggle_button.configure(fg=text_colour, bg=secondary_colour)
    global editor
    editor.configure(fg=text_colour, bg=primary_colour, insertbackground=text_colour)
    global frame
    frame.configure(bg=primary_colour)
    global image_label
    image_label.configure(bg=primary_colour)
    global tree_toggle_button
    tree_toggle_button.configure(fg=text_colour, bg=secondary_colour)
    global file_tree
    file_tree.configure(bg=secondary_colour)
    
    style.configure("Treeview", background=secondary_colour, foreground=text_colour)
    style.map("Treeview", background=[('selected', primary_colour)], foreground=[('selected', text_colour)])

def light_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "white"
    secondary_colour="#e3e4ea"
    text_colour="black"
    
    theme_widgets()

def solarised_light_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#fdf6e3"
    secondary_colour="#eee8d5"
    text_colour="#556970"

    theme_widgets()

def monokai_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#272822"
    secondary_colour="#1f201b"
    text_colour="#cbcab9"
    
    theme_widgets()

def coffee_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#d9ba93"
    secondary_colour = "#bba180"
    text_colour = "white"
    
    theme_widgets()

def dark_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#272727"
    secondary_colour = "#1f1f1f"
    text_colour = "white"
    
    theme_widgets()
    
def one_dark_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#282c34"
    secondary_colour = "#23272c"
    text_colour = "#e7eaef"
    
    theme_widgets()

def black_n_white():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "white"
    secondary_colour = "#2c2c2c"
    text_colour = "#2c2c2c"
    
    theme_widgets()
    global console, console_toggle_button, tree_toggle_button
    console_toggle_button.configure(fg="#e8e8e8")
    console.configure(fg="#e8e8e8")
    tree_toggle_button.configure(fg="#e8e8e8")
    style.configure("Treeview", foreground="#e8e8e8")
    style.map("Treeview", foreground=[('selected', "black")])

def set_primary_colour():
    global primary_colour
    primary_colour = colorchooser.askcolor(title ="Colour Chooser")[1]
    print(primary_colour)
    try:
        theme_widgets()
    except:
        messagebox.showerror("Error", "Invalid hex code.")

def set_secondary_colour():
    global secondary_colour
    secondary_colour = colorchooser.askcolor(title ="Colour Chooser")[1]
    try:
        theme_widgets()
    except:
        messagebox.showerror("Error", "Invalid hex code.")

def set_text_colour():
    global text_colour
    text_colour = colorchooser.askcolor(title ="Colour Chooser")[1]
    try:
        theme_widgets()
    except:
        messagebox.showerror("Error", "Invalid hex code.")

def maximize_console():
    pass

def minimize_console():
    pass

def show_console():
    global console_status
    if console_status == "visible":
        return

    global console
    console.pack(side=BOTTOM, expand=True, fill=BOTH)
    console_toggle_button.config(text="CONSOLE ⮟")
    console_status = "visible"

def hide_console():
    global console_status
    global console
    console_status = "hidden"
    console.pack_forget()
    console_toggle_button.config(text="CONSOLE ⮝")

def console_toggle():
    global console_status
    if console_status == "visible":
        hide_console()
    else:
        show_console()

def show_tree():
    global tv, tree_toggle_button, tree_status
    tree_toggle_button.configure(text="FILE TREE ⮟", width=3, anchor='w', font=('JetBrains Mono', 9))
    tv.pack(expand=TRUE, anchor='n', fill=BOTH)
    tree_status = "visible"

def hide_tree():
    global tv, tree_toggle_button, tree_status
    tv.pack_forget()
    tree_toggle_button.pack_forget()
    tree_toggle_button.pack(side=TOP, fill=BOTH)
    tree_toggle_button.configure(text="F\nI\nL\nE\n\nT\nR\nE\nE\n⮞", width=3, anchor='center', font=('JetBrains Mono', 9))
    tree_status = "hidden"
    
def tree_toggle():
    global tree_status
    if tree_status == "visible":
        hide_tree()
    else:
        show_tree()

def run():
    global default_file_path
    global run_command
    if mode == "file":
        if default_file_path == "":
            save_as()

    if run_command == "":
        set_run_command()

    if console_status == "hidden":
        show_console()
    
    process = subprocess.Popen(
        run_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)

    output, error = process.communicate()
    console.configure(state=NORMAL)
    console.delete("1.0", END)
    time.sleep(0.1)
    console.insert(END, output)
    console.insert(END, error)
    console.configure(state=DISABLED)

def set_run_command():
    global run_command
    run_command = askstring(title="Set Run Command", prompt="Eg: python main.py\n(Make sure to type the correct file path.)")

def save_as():
    global mode, current_open_file
    if mode == "file":
        file_path = asksaveasfilename()

        with open(file_path, "w") as file:
            code = editor.get("1.0", END)
            file.write(code)
            
        global default_file_path
        default_file_path = file_path
        file_name = default_file_path.split("/")[-1]
        root.title(f"{file_name} - ZeText")
    
    if mode == "folder":
        file_path = asksaveasfilename()

        with open(file_path, "w") as file:
            code = editor.get("1.0", END)
            file.write(code)

def save():
    global default_file_path, mode, current_open_file, file_contents
    if mode == "file":
        if default_file_path == "":
            file_path = asksaveasfilename()
        else:
            file_path = default_file_path
        
        with open(file_path, "w") as file:
            code = editor.get("1.0", END)
            file.write(code)
        
        default_file_path = file_path
        file_name = default_file_path.split("/")[-1]
        root.title(f"{file_name} - ZeText")
    
    if mode == "folder":
        if file_contents[current_open_file.replace("\\", "/").split('/')[-1]]["readable"] == False: return
        with open(current_open_file, "w") as f:
            code = editor.get("1.0", END)
            f.write(code)

def open_file():
    global editor, image_label

    file_path = askopenfilename()
    if file_path == "":
        return ""

    image_type = imghdr.what(file_path)
    if image_type == None:
        with open(file_path, "r") as file:
            code = file.read()

            editor.delete("1.0", END)
            editor.insert("1.0", code)
    else:
        editor.pack_forget()

        global image
        image = PhotoImage(file=file_path).subsample(4, 4)
        image_label.configure(image=image)
        image_label.pack(expand=True, fill=BOTH, padx=(5,0))       

    global default_file_path
    default_file_path = file_path
    file_name = default_file_path.split("/")[-1]
    root.title(f"{file_name} - ZeText")

# Navigation Bar
nav_bar = Menu(root, background="#e3e4ea", bd=0, relief=FLAT)

# File button
file_button = Menu(nav_bar, tearoff=0, background="#e3e4ea")

file_button.add_command(label="New File")
file_button.add_command(label="New Window")
file_button.add_separator()
file_button.add_command(label="Open File", command=open_file)
file_button.add_command(label="Open Folder")
file_button.add_separator()
file_button.add_command(label="Save", command=save)
file_button.add_command(label="Save As...", command=save_as)
file_button.add_separator()
file_button.add_command(label="Close Window")
file_button.add_separator()
file_button.add_command(label="Exit", command=exit)

nav_bar.add_cascade(label="File", menu=file_button)

# Edit button
edit_button = Menu(nav_bar, tearoff=0, background="#e3e4ea", bd=0, relief=FLAT)

nav_bar.add_cascade(label="Edit", menu=edit_button)

# Run button
run_button = Menu(nav_bar, tearoff=0, background="#e3e4ea", bd=0, relief=FLAT)

run_button.add_command(label="Run", command=run)
run_button.add_command(label="Set Run Command", command=set_run_command)

nav_bar.add_cascade(label="Run", menu=run_button)

# Console button
console_button = Menu(nav_bar, tearoff=0, background="#e3e4ea", bd=0, relief=FLAT)

console_button.add_command(label="Show Console", command=show_console)
console_button.add_command(label="Hide Console", command=hide_console)
console_button.add_command(label="Maximize", command=maximize_console)
console_button.add_command(label="Minimize", command=minimize_console)

nav_bar.add_cascade(label="Console", menu=console_button)

# Theme button
themes_button = Menu(nav_bar, tearoff=0, bd=0, relief=FLAT, background="#e3e4ea")

themes_button.add_command(label="Light Theme", command=light_theme)
themes_button.add_command(label="Solarised Light Theme", command=solarised_light_theme)
themes_button.add_command(label="Dark Theme", command=dark_theme)
themes_button.add_command(label="Coffee Theme", command=coffee_theme)
themes_button.add_command(label="One Dark Theme", command=one_dark_theme)
themes_button.add_command(label="Monokai Theme", command=monokai_theme)
themes_button.add_command(label="Black N White  Theme", command=black_n_white)

themes_button_custom = Menu(themes_button, tearoff=0, bd=0, relief=FLAT)
themes_button_custom.add_command(label="Primary Colour", command=set_primary_colour)
themes_button_custom.add_command(label="Seconday Colour", command=set_secondary_colour)
themes_button_custom.add_command(label="Text Colour", command=set_text_colour)
themes_button.add_separator()
themes_button.add_cascade(label="Custom", menu=themes_button_custom)

nav_bar.add_cascade(label="Themes", menu=themes_button)

frame = LabelFrame(root, bd=0, relief=FLAT, bg=primary_colour)

editor = Text(frame, highlightthickness=0, bd=0, relief=FLAT, font=("JetBrains Mono", 15), bg=primary_colour)
editor.pack(expand=True, fill=BOTH, padx=(5,0))

console_frame = Frame(frame, bd=0, relief=FLAT)
console_frame.pack(side=BOTTOM, fill=BOTH)

console_toggle_button = Button(console_frame, text="CONSOLE ⮟", bg=secondary_colour, anchor="w", bd=0, relief=FLAT, activebackground="#bebfc4", command=console_toggle)
console_toggle_button.pack(fill=BOTH)

console = Text(console_frame, height=9, bg=secondary_colour, highlightthickness=0, bd=0, relief=FLAT, state=DISABLED, font=("JetBrains Mono", 13))
console.pack(side=BOTTOM, expand=True, fill=BOTH)

bottom_bar = Frame(root, bd=0, relief=FLAT)

file_tree = Frame(root, bd=0, relief=FLAT, bg=secondary_colour)

tree_toggle_button = Button(file_tree, text="FILE TREE ⮟", bg=secondary_colour, anchor="w", bd=0, relief=FLAT, activebackground="#bebfc4", command=tree_toggle, fg=text_colour, width=31)
tree_toggle_button.pack(side=TOP, fill=BOTH)

image_label = Label(frame, highlightthickness=0, bd=0, relief=FLAT, font=("JetBrains Mono", 15), bg=primary_colour)

tv = ttk.Treeview(file_tree,show='tree')

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11), background=secondary_colour, foreground=text_colour, activebackground='red', rowheight=25)
style.configure("Treeview.Heading", font=('Calibri', 15,'bold'), foreground="red") 
style.layout("Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
style.map("Treeview", background=[('selected', primary_colour)], foreground=[('selected', text_colour)])

def make_tv(folder):
    if folder == '':
        return

    global file_contents, tv_items, directory
    directory=folder
    tv_items = {}
    file_contents = {}
    
    tv.heading("#0", anchor="w")
    file_path = os.path.abspath(directory)
    tv_item = tv.insert("", END,text=file_path.replace("\\", "/").split('/')[-1], open=True)

    def traverse_dir(parent, path):
        global file_contents, tv_items, directory
        for d in os.listdir(path):
            full_path=os.path.join(path,d)
            tv_items[d] = full_path
            
            with open(tv_items[d], "r", encoding="utf-8") as f:
                try:
                     file_contents[d] = {"content": f.read(), "readable": True}
                except:
                        file_contents[d] = {"content": "", "readable": False}

            isdir = os.path.isdir(full_path)
            id=tv.insert(parent, END, text=d, open=False, tags=r"{}".format(full_path))
            if isdir:
                traverse_dir(id, full_path)
        
    traverse_dir(tv_item, file_path)

tv.pack(expand=TRUE, anchor="n", fill=BOTH)

# messy code warning, i never ever want to touch this part again
def on_tv_click(e):
    global editor, dunno_what_to_name_this, file_contents, prev, current_open_file, image_label, editor_status
    
    selected_item = tv.focus()
    values = tv.item(selected_item)
    image_type = imghdr.what(tv_items[values["text"]])

    if os.path.isdir(tv_items[values['text']]):
        return
    current_open_file = tv_items[values["text"]]
    if dunno_what_to_name_this == True: 
        if editor_status == "visible":
            file_contents[prev]["content"] = editor.get("1.0", END)

    image_label.pack_forget()
    editor.pack(expand=True, fill=BOTH, padx=(5,0))
    editor_status == "visible"
    editor.configure(state=NORMAL)

    if file_contents[values['text']]["readable"]:
        editor.delete("1.0","end")
        editor.insert("1.0", file_contents[values['text']]["content"])
        prev = values["text"].replace("\\", "/").split('/')[-1]
    else:
        if image_type != None:
            if dunno_what_to_name_this == True:
                file_contents[prev]["content"] = editor.get("1.0", END)
            editor.pack_forget()
            editor_status = "hidden"
            global image
            #image = ImageTk.PhotoImage(Image.open(tv_items[values["text"]]).resize((2, 2), Image.ANTIALIAS))
            image = PhotoImage(file=tv_items[values["text"]]).subsample(4, 4)
            image_label.configure(image=image)
            
            image_label.pack(expand=True, fill=BOTH, padx=(5,0))
            return
            
        messagebox.showerror('Error', "Couldn't display file.")
        prev = values["text"].replace("\\", "/").split('/')[-1]
   
        editor.delete("1.0","end")
        editor.insert("1.0", "There was an error displaying the file.")
        editor.configure(state=DISABLED)
    
    dunno_what_to_name_this = True
    
def save_binding(e):
    save()

def new_file_hp():
    homepage.pack_forget()
    root.minsize(350, 800)
    root.config(menu=nav_bar)
    frame.pack(side=RIGHT, expand=True, fill=BOTH)

    root.bind("<Control-s>", save_binding)

    global mode
    mode = "file"

def file_opener_hp():
    file = open_file()
    if file == "":
        return
    homepage.pack_forget()
    root.minsize(350, 800)
    root.config(menu=nav_bar)
    frame.pack(side=RIGHT, expand=True, fill=BOTH)

    root.bind("<Control-s>", save_binding)  

    global mode
    mode = "file"

def folder_opener_hp():
    folder = askdirectory()
    if folder == "":
        return
    homepage.pack_forget()
    root.minsize(1200, 800)
    root.config(menu=nav_bar)
    frame.pack(side=RIGHT, expand=True, fill=BOTH)
    
    file_tree.pack(side=LEFT, fill=BOTH)

    tv.bind("<ButtonRelease-1>", on_tv_click)
    root.bind("<Control-s>", save_binding)

    make_tv(folder)
    file_tree.pack_forget()
    file_tree.pack(side=LEFT, fill=BOTH)

    global mode
    mode = "folder"
    
homepage = Frame(root)

zetext = Label(homepage, text="ZeText", anchor=CENTER).pack()
new_file_hp = Button(homepage, text="New File", anchor=CENTER, command=new_file_hp, bd=0, relief=FLAT, bg="#2199d4").pack(pady=10)
open_file_hp = Button(homepage, text="Open File", anchor=CENTER, command=file_opener_hp, bd=0, relief=FLAT, bg="#2199d4").pack(pady=10)
open_folder_hp = Button(homepage, text="Open Folder", anchor=CENTER, command=folder_opener_hp, bd=0, relief=FLAT, bg="#2199d4").pack(pady=10)

homepage.pack()

root.mainloop()
