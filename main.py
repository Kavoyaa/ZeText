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
root.minsize(550, 355)
root.resizable(False, False)

default_file_path = ""
run_command = ""
output_content = ""
output_window_status = "visible"
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
primary_text_colour = "black"
secondary_text_colour = "grey"

def enable_bindings(mode):
    if mode == "file":
        root.bind("<Control-s>", save_binding)
        root.bind("<MouseWheel>", mousewheel_move)
        root.bind("<Key>", show_lines)
    else:
        tv.bind("<ButtonRelease-1>", on_tv_click)
        root.bind("<Control-s>", save_binding)
        root.bind("<MouseWheel>", mousewheel_move)
        root.bind("<Key>", show_lines)
        root.bind("<Control-Shift-S>", save_as)
        root.bind("<F5>", run)
        root.bind("<Control-F5>", set_run_command)

def theme_widgets():
    global output
    output.configure(fg=primary_text_colour, bg=secondary_colour)
    global output_toggle_button
    output_toggle_button.configure(fg=primary_text_colour, bg=secondary_colour, activebackground=secondary_colour, activeforeground=primary_text_colour)
    global editor
    editor.configure(fg=primary_text_colour, bg=primary_colour, insertbackground=primary_text_colour)
    global right_frame
    right_frame.configure(bg=primary_colour)
    global image_label
    image_label.configure(bg=primary_colour)
    global tree_toggle_button
    tree_toggle_button.configure(fg=primary_text_colour, bg=secondary_colour, activebackground=secondary_colour, activeforeground=primary_text_colour)
    global left_frame
    left_frame.configure(bg=secondary_colour)
    global file_tree
    file_tree.configure(bg=secondary_colour)
    global line_nums
    line_nums.configure(bg=primary_colour, fg=secondary_text_colour)
    global text_frame
    text_frame.configure(bg=primary_colour)
    
    style.configure("Treeview", background=secondary_colour, foreground=primary_text_colour)
    style.map("Treeview", background=[('selected', primary_colour)], foreground=[('selected', primary_text_colour)])

def light_theme():
    global secondary_colour, primary_colour, primary_text_colour, theme, secondary_text_colour

    primary_colour = "white"
    secondary_colour ="#e3e4ea"
    primary_text_colour ="black"
    secondary_text_colour = "#9a9a9a"
    
    theme_widgets()

def solarised_light_theme():
    global secondary_colour, primary_colour, primary_text_colour, theme, secondary_text_colour

    primary_colour = "#fdf6e3"
    secondary_colour ="#eee8d5"
    primary_text_colour ="#556970"
    secondary_text_colour = "#d4cdb9"

    theme_widgets()

def monokai_theme():
    global secondary_colour, primary_colour, primary_text_colour, theme, secondary_text_colour

    primary_colour = "#272822"
    secondary_colour ="#1f201b"
    primary_text_colour ="#cbcab9"
    secondary_text_colour = "#42433f"
    
    theme_widgets()

def dark_theme():
    global secondary_colour, primary_colour, primary_text_colour, theme, secondary_text_colour

    primary_colour = "#272727"
    secondary_colour = "#1f1f1f"
    primary_text_colour = "white"
    secondary_text_colour = "#4d4d4d"
    
    theme_widgets()
    
def one_dark_theme():
    global secondary_colour, primary_colour, primary_text_colour, theme, secondary_text_colour

    primary_colour = "#282c34"
    secondary_colour = "#23272c"
    primary_text_colour = "#e7eaef"
    secondary_text_colour = "grey"
    
    theme_widgets()

def black_n_white():
    global secondary_colour, primary_colour, primary_text_colour, theme, secondary_text_colour

    primary_colour = "white"
    secondary_colour = "#2c2c2c"
    primary_text_colour = "#2c2c2c"
    secondary_text_colour = "grey"
    
    theme_widgets()
    global output, output_toggle_button, tree_toggle_button
    output_toggle_button.configure(fg="#e8e8e8")
    output.configure(fg="#e8e8e8")
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

def set_primary_text_colour():
    global primary_text_colour
    primary_text_colour = colorchooser.askcolor(title ="Colour Chooser")[1]
    try:
        theme_widgets()
    except:
        messagebox.showerror("Error", "Invalid hex code.")

def set_secondary_text_colour():
    global secondary_text_colour
    secondary_text_colour = colorchooser.askcolor(title ="Colour Chooser")[1]
    try:
        theme_widgets()
    except:
        messagebox.showerror("Error", "Invalid hex code.")

def maximize_output_window():
    pass

def minimize_output_window():
    pass

def show_output():
    global output_window_status
    if output_window_status == "visible":
        return

    global output
    output.pack(side=BOTTOM, expand=True, fill=BOTH)
    output_toggle_button.config(text="OUTPUT ⮟")
    output_window_status = "visible"

def hide_output():
    global output_window_status
    global output
    output_window_status = "hidden"
    output.pack_forget()
    output_toggle_button.config(text="OUTPUT ⮝")

def output_toggle():
    global output_window_status
    if output_window_status == "visible":
        hide_output()
    else:
        show_output()

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

def run_code():
    process = subprocess.Popen(
        run_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)

    output, error = process.communicate()
    output.configure(state=NORMAL)
    output.delete("1.0", END)
    time.sleep(0.1)
    output.insert(END, output)
    output.insert(END, error)
    output.configure(state=DISABLED)

def run(e=None):
    global default_file_path
    global run_command
    if mode == "file":
        if default_file_path == "":
            save_as()

    if run_command == "":
        set_run_command()

    if output_window_status == "hidden":
        show_output()

    process = subprocess.Popen(
        run_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)

    output, error = process.communicate()
    output.configure(state=NORMAL)
    output.delete("1.0", END)
    time.sleep(0.1)
    output.insert(END, output)
    output.insert(END, error)
    output.configure(state=DISABLED)

def set_run_command(e=None):
    global run_command
    run_command = askstring(title="Set Run Command", prompt="Eg: python main.py\n(Make sure to type the correct file path.)")

def select_text():
    pass

def save_as(e=None):
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

def save(e=None):
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

def new_window():
    pass

def open_file():
    global editor, image_label

    file_path = askopenfilename()
    if file_path == "":
        return ""

    image_type = imghdr.what(file_path)
    if image_type == None:
        with open(file_path, "r", encoding="utf-8") as file:
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
file_button.add_command(label="New Window", command=new_window)
file_button.add_separator()
file_button.add_command(label="Open File", command=open_file)
file_button.add_command(label="Open Folder")
file_button.add_separator()
file_button.add_command(label="Save", command=save, accelerator="Ctrl+S")
file_button.add_command(label="Save As...", command=save_as)
file_button.add_separator()
file_button.add_command(label="Close Window", command=exit)
file_button.add_separator()
file_button.add_command(label="Exit", command=exit)

nav_bar.add_cascade(label="File", menu=file_button)

# Edit button
edit_button = Menu(nav_bar, tearoff=0, background="#e3e4ea", bd=0, relief=FLAT)
edit_button.add_command(label="Select All", command=select_text, accelerator="Ctrl+/")

nav_bar.add_cascade(label="Edit", menu=edit_button)

# Run button
run_button = Menu(nav_bar, tearoff=0, background="#e3e4ea", bd=0, relief=FLAT)

run_button.add_command(label="Run", command=run, accelerator="F5")
run_button.add_command(label="Set Run Command", command=set_run_command, accelerator="Ctrl+F5")

nav_bar.add_cascade(label="Run", menu=run_button)

# Theme button
themes_button = Menu(nav_bar, tearoff=0, bd=0, relief=FLAT, background="#e3e4ea")

themes_button.add_command(label="Light Theme", command=light_theme)
themes_button.add_command(label="Solarised Light Theme", command=solarised_light_theme)
themes_button.add_command(label="Dark Theme", command=dark_theme)
themes_button.add_command(label="One Dark Theme", command=one_dark_theme)
themes_button.add_command(label="Monokai Theme", command=monokai_theme)
themes_button.add_command(label="Black N White  Theme", command=black_n_white)

themes_button_custom = Menu(themes_button, tearoff=0, bd=0, relief=FLAT)
themes_button_custom.add_command(label="Primary Colour", command=set_primary_colour)
themes_button_custom.add_command(label="Seconday Colour", command=set_secondary_colour)
themes_button_custom.add_command(label="Primary Text Colour", command=set_primary_text_colour)
themes_button_custom.add_command(label="Secondary Text Colour", command=set_secondary_text_colour)
themes_button.add_separator()
themes_button.add_cascade(label="Custom", menu=themes_button_custom)

nav_bar.add_cascade(label="Themes", menu=themes_button)

right_frame = Frame(root, bd=0, relief=FLAT, bg=primary_colour)

text_frame = Frame(right_frame, bd=0, relief=FLAT, bg=primary_colour)
text_frame.pack(expand=True, fill=BOTH)

line_nums = Text(text_frame, bg=primary_colour, highlightthickness=0, bd=0, relief=FLAT, state=DISABLED, font=("JetBrains Mono", 15), width=5, fg="grey")
line_nums.tag_configure("right", justify='right')
line_nums.pack(side=LEFT, anchor="n", fill=BOTH)

editor = Text(text_frame, highlightthickness=0, bd=0, relief=FLAT, font=("JetBrains Mono", 15), bg=primary_colour, wrap="none", undo=True, autoseparators=True)
editor.pack(expand=True, fill=BOTH, padx=(5,0))

output_frame = Frame(right_frame, bd=0, relief=FLAT)
output_frame.pack(side=BOTTOM, fill=BOTH)

output_toggle_button = Button(output_frame, text="OUTPUT ⮟", bg=secondary_colour, anchor="w", bd=0, relief=FLAT, activebackground=secondary_colour, command=output_toggle)
output_toggle_button.pack(fill=BOTH)

output = Text(output_frame, height=9, bg=secondary_colour, highlightthickness=0, bd=0, relief=FLAT, state=DISABLED, font=("JetBrains Mono", 13))
output.pack(side=BOTTOM, expand=True, fill=BOTH)

bottom_bar = Frame(root, bd=0, relief=FLAT)

left_frame = Frame(root, bd=0, relief=FLAT, bg=secondary_colour)
file_tree = Frame(left_frame, bd=0, relief=FLAT, bg=secondary_colour)
file_tree.pack(side=LEFT, fill=BOTH)

tree_toggle_button = Button(file_tree, text="FILE TREE ⮟", bg=secondary_colour, anchor="w", bd=0, relief=FLAT, activebackground=secondary_colour, command=tree_toggle, fg=primary_text_colour, width=31)
tree_toggle_button.pack(side=TOP, fill=BOTH)

image_label = Label(right_frame, highlightthickness=0, bd=0, relief=FLAT, font=("JetBrains Mono", 15), bg=primary_colour)

tv = ttk.Treeview(file_tree, show='tree')

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11), background=secondary_colour, foreground=primary_text_colour, activebackground='red', rowheight=30)
style.configure("Treeview.Heading", font=('Calibri', 15,'bold'), foreground="red") 
style.layout("Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
style.map("Treeview", background=[('selected', primary_colour)], foreground=[('selected', primary_text_colour)])

folder_img = PhotoImage(file="icons/folder.png").subsample(3, 3)
picture_img = PhotoImage(file="icons/picture.png").subsample(3, 3)
file_img = PhotoImage(file="icons/file.png").subsample(3, 3)

def make_tv(folder):
    if folder == '':
        return

    global file_contents, tv_items, directory
    directory=folder
    tv_items = {}
    file_contents = {}
    
    tv.heading("#0", anchor="w")
    file_path = os.path.abspath(directory)
    tv_item = tv.insert("", END, text=" "+file_path.replace("\\", "/").split('/')[-1], open=True, image=folder_img)

    def traverse_dir(parent, path):
        global file_contents, tv_items, directory
        for file in os.listdir(path):
            
            full_path=os.path.join(path, file)
            tv_items[file] = full_path
            try:
                with open(tv_items[file], "r", encoding="utf-8") as f:
                    try:
                        file_contents[file] = {"content": f.read(), "readable": True}
                    except:
                            file_contents[file] = {"content": "", "readable": False}
            except: pass

            isdir = os.path.isdir(full_path)
            
            if isdir:
                id=tv.insert(parent, END, text=" "+file, open=False, tags=r"{}".format(full_path), image=folder_img)
                traverse_dir(id, full_path)
            elif imghdr.what(full_path) != None:
                id=tv.insert(parent, END, text=" "+file, open=False, tags=r"{}".format(full_path), image=picture_img)
            else:
                id=tv.insert(parent, END, text=" "+file, open=False, tags=r"{}".format(full_path), image=file_img)
        
    traverse_dir(tv_item, file_path)

tv.pack(expand=TRUE, anchor="n", fill=BOTH)


# messy code warning, i never ever want to touch this part again
def on_tv_click(e):
    global editor, dunno_what_to_name_this, file_contents, prev, current_open_file, image_label, editor_status
    
    selected_item = tv.focus()
    values = tv.item(selected_item)
    image_type = imghdr.what(tv_items[values["text"][1:]])

    if os.path.isdir(tv_items[values['text'][1:]]):
        return
    current_open_file = tv_items[values["text"][1:]]
    if dunno_what_to_name_this == True: 
        if editor_status == "visible":
            file_contents[prev]["content"] = editor.get("1.0", END)

    image_label.pack_forget()
    text_frame.pack(expand=True, fill=BOTH, padx=(5,0))
    editor_status == "visible"
    editor.configure(state=NORMAL)
    line_nums.pack()

    if file_contents[values['text'][1:]]["readable"]:
        editor.delete("1.0","end")
        editor.insert("1.0", file_contents[values['text'][1:]]["content"])
        prev = values["text"][1:].replace("\\", "/").split('/')[-1]
        show_lines(e=None)
    else:
        if image_type != None:
            if dunno_what_to_name_this == True:
                file_contents[prev]["content"] = editor.get("1.0", END)
            text_frame.pack_forget()
            editor_status = "hidden"

            global image
            #image = ImageTk.PhotoImage(Image.open(tv_items[values["text"]]).resize((2, 2), Image.ANTIALIAS))
            image = PhotoImage(file=tv_items[values["text"][1:]]).subsample(4, 4)
            image_label.configure(image=image)
            
            image_label.pack(expand=True, fill=BOTH, padx=(5,0))
            return
            
        messagebox.showerror('Error', "Couldn't display file.")
        prev = values["text"][1:].replace("\\", "/").split('/')[-1]
   
        editor.delete("1.0","end")
        editor.insert("1.0", "There was an error displaying the file.")
        editor.configure(state=DISABLED)
    
    dunno_what_to_name_this = True

    
def save_binding(e):
    save()

def show_lines(e):
    nums = ""
    for i in range(int(editor.index('end').split('.')[0])-1):
        nums += " " + str(i+1) + " \n"
    
    line_nums.configure(state=NORMAL)
    line_nums.delete("1.0", END)
    line_nums.insert("1.0", nums[:-1])
    line_nums.tag_add("right", 1.0, "end")
    line_nums.configure(state=DISABLED)
    line_nums.yview_moveto(float(editor.yview()[0]))

def mousewheel_move(e):
    line_nums.yview_moveto(float(editor.yview()[0]))

def new_file_opener_hp():
    homepage.place_forget()
    root.minsize(350, 800)
    root.resizable(True, True)
    root.config(menu=nav_bar)
    right_frame.pack(side=RIGHT, expand=True, fill=BOTH)

    root.bind("<Control-s>", save_binding)
    root.bind("<MouseWheel>", mousewheel_move)
    root.bind("<Key>", show_lines)

    show_lines(e=None)

    global mode
    mode = "file"

def file_opener_hp():
    file = open_file()
    if file == "":
        return
    homepage.place_forget()
    root.minsize(350, 800)
    root.resizable(True, True)
    root.config(menu=nav_bar)
    right_frame.pack(side=RIGHT, expand=True, fill=BOTH)

    enable_bindings("file")
    show_lines(e=None)

    global mode
    mode = "file"

def folder_opener_hp():
    folder = askdirectory()
    if folder == "":
        return

    homepage.place_forget()
    root.minsize(1200, 800)
    root.resizable(True, True)
    root.config(menu=nav_bar)
    right_frame.pack(side=RIGHT, expand=True, fill=BOTH)
    
    left_frame.pack(side=LEFT, fill=BOTH)

    enable_bindings("folder")
    make_tv(folder)

    left_frame.pack_forget()
    left_frame.pack(side=LEFT, fill=BOTH)

    editor.configure(state=DISABLED)

    global mode
    mode = "folder"   
    
homepage = Frame(root, bd=0, relief=FLAT)
zetext = Label(homepage, text="ZeText", font=("Helvatica", "40"), fg="#4f555e").pack(pady=(0, 9))

new_file_hp = Button(homepage, text="New File", command=new_file_opener_hp, bd=0, relief=FLAT, bg="#33b0ed", activebackground="#46b5ec", padx=4, width=22, height=2).pack(pady=6)
open_file_hp = Button(homepage, text="Open File",  command=file_opener_hp, bd=0, relief=FLAT, bg="#33b0ed", activebackground="#46b5ec", padx=4, width=22, height=2).pack(pady=6)
open_folder_hp = Button(homepage, text="Open Folder", command=folder_opener_hp, bd=0, relief=FLAT, bg="#33b0ed", activebackground="#46b5ec", padx=4, width=22, height=2).pack(pady=6)

homepage.place(relx=.5, rely=.5, anchor= CENTER)

root.mainloop()
