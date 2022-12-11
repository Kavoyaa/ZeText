from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename, askdirectory
from tkinter.simpledialog import askstring
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import ttk
#from ttkthemes import themed_tk as tk
import subprocess
import time
import os

root = Tk()
#root.get_themes()
#root.set_theme("yaru")
root.title("Untitled - ZeText")
root.minsize(350, 770)

default_file_path = ""
run_command = ""
console_content = ""
console_status = "visible"
theme = "light"
dunno_what_to_name_this = False
mode = ""
current_open_file = ""

primary_colour = "white"
secondary_colour ="#e3e4ea"
tertiary_colour = ""

text_colour="black"

def update_widgets():
    global console
    console.configure(fg=text_colour, bg=secondary_colour)
    global console_toggle_button
    console_toggle_button.configure(fg=text_colour, bg=secondary_colour)
    global editor
    editor.configure(fg=text_colour, bg=primary_colour, insertbackground=text_colour)
    global frame
    frame.configure(bg=primary_colour)
    global tree_toggle
    tree_toggle.configure(fg=text_colour, bg=secondary_colour)
    
    style.configure("Treeview", background=secondary_colour, foreground=text_colour)
    style.map("Treeview", background=[('selected', primary_colour)], foreground=[('selected', text_colour)])

def light_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "white"
    secondary_colour="#e3e4ea"
    text_colour="black"
    
    update_widgets()

def solarised_light_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#fdf6e3"
    secondary_colour="#eee8d5"
    text_colour="#556970"

    update_widgets()

def monokai_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#272822"
    secondary_colour="#1f201b"
    text_colour="#cbcab9"
    
    update_widgets()

def coffee_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#d9ba93"
    secondary_colour = "#bba180"
    text_colour = "white"
    
    update_widgets()

def dark_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#272727"
    secondary_colour = "#1f1f1f"
    text_colour = "white"
    
    update_widgets()
    
def one_dark_theme():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "#282c34"
    secondary_colour = "#23272c"
    text_colour = "#e7eaef"
    
    update_widgets()

def black_n_white():
    global secondary_colour, primary_colour, text_colour, theme

    primary_colour = "white"
    secondary_colour = "#2c2c2c"
    text_colour = "#2c2c2c"
    
    update_widgets()
    global console, console_toggle_button
    console_toggle_button.configure(fg="white")
    console.configure(fg="white")

def set_primary_colour():
    global primary_colour
    primary_colour = colorchooser.askcolor(title ="Colour Chooser")[1]
    print(primary_colour)
    try:
        update_widgets()
    except:
        messagebox.showerror("Error", "Invalid hex code.")

def set_secondary_colour():
    global secondary_colour
    secondary_colour = colorchooser.askcolor(title ="Colour Chooser")[1]
    try:
        update_widgets()
    except:
        messagebox.showerror("Error", "Invalid hex code.")

def set_text_colour():
    global text_colour
    text_colour = colorchooser.askcolor(title ="Colour Chooser")[1]
    try:
        update_widgets()
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
    console = Text(frame, height=9, bg=secondary_colour, highlightthickness=0, bd=0, relief=FLAT, state=DISABLED, font=("JetBrains Mono", 15), fg=text_colour)
    console.pack(expand=True, fill=BOTH)
    console.insert("1.0", console_content)
    console_status="visible"
    console_toggle_button.config(text="CONSOLE ⮟")

def hide_console():
    global console_status
    global console
    console_status = "hidden"
    console.destroy()
    console_toggle_button.config(text="CONSOLE ⮝")

def console_toggle():
    global console_status
    if console_status == "visible":
        hide_console()
    else:
        show_console()

def run():
    global default_file_path
    global run_command
    
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
   
    file_path = asksaveasfilename()

    with open(file_path, "w") as file:
        code = editor.get("1.0", END)
        file.write(code)
        
    global default_file_path
    default_file_path = file_path
    file_name = default_file_path.split("/")[-1]
    root.title(f"{file_name} - ZeText")
    

def save():
    global default_file_path, mode, current_open_file
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
        print(current_open_file)
        with open(current_open_file, "w") as f:
            code = editor.get("1.0", END)
            f.write(code)
            print(current_open_file)

def open_file():
    file_path = askopenfilename()

    with open(file_path, "r") as file:
        code = file.read()

        editor.delete("1.0", END)
        editor.insert("1.0", code)

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

#root.config(menu=nav_bar)


frame = LabelFrame(root, bd=0, relief=FLAT, bg=primary_colour)
#frame.pack(side=RIGHT, expand=True, fill=BOTH)



editor = Text(frame, highlightthickness=0, bd=0, relief=FLAT, font=("JetBrains Mono", 15), bg=primary_colour)




editor.pack(expand=True, fill=BOTH, padx=(5,0))

console_toggle_button = Button(frame, text="CONSOLE ⮟", bg=secondary_colour, anchor="w", bd=0, relief=FLAT, activebackground="#bebfc4", command=console_toggle)
console_toggle_button.pack(fill=BOTH)

console = Text(frame, height=9, bg=secondary_colour, highlightthickness=0, bd=0, relief=FLAT, state=DISABLED, font=("JetBrains Mono", 13))
console.pack(side=BOTTOM, expand=True, fill=BOTH)

f = Frame(root, bd=0, relief=FLAT, bg='#23272c')
#f.pack(side=LEFT, fill=BOTH)


tree_toggle = Button(f, text="FILE TREE ⮟", bg=secondary_colour, anchor="w", bd=0, relief=FLAT, activebackground="#bebfc4", command=console_toggle, fg=text_colour, width=31)
tree_toggle.pack(side=TOP, fill=BOTH)

tv = ttk.Treeview(f,show='tree')

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11), background=secondary_colour, foreground=text_colour, activebackground='red', rowheight=25) # Modify the font of the body
style.configure("Treeview.Heading", font=('Calibri', 15,'bold'), foreground="red") # Modify the font of the headings
style.layout("Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
style.map("Treeview", background=[('selected', primary_colour)], foreground=[('selected', text_colour)])

def make_tv(folder):
    if folder == '':
        return

    global file_contents, tv_items, directory
    directory=folder
    tv_items = {}
    file_contents = {}
    
    tv.heading('#0', anchor='w')
    path=os.path.abspath(directory)
    node=tv.insert('','end',text=path,open=True)
    def traverse_dir(parent,path):
        global file_contents, tv_items, directory
        for d in os.listdir(path):
            full_path=os.path.join(path,d)
            tv_items[d] = full_path
            try:
                with open(tv_items[d], 'r') as f:
                    try:
                        file_contents[d] = {"content": f.read(), "readable": True}
                    except:
                        file_contents[d] = {"content": "", "readable": False}
            except Exception as e:
                print(e.__str__())
            isdir = os.path.isdir(full_path)
            id=tv.insert(parent,'end',text=d,open=False, tags=r"{}".format(full_path))
            if isdir:
                traverse_dir(id,full_path)
        
    traverse_dir(node,path)
    print(tv_items)
    print(file_contents)

    '''
    for item in list(tv_items.keys()):
        try:
            with open(tv_items[item], 'r') as f:
                try:
                    file_contents[item] = f.read()
                except:
                    print(item)
        except Exception as e:
            print(e.__str__())
    print(file_contents)
    '''
tv.pack(expand=TRUE, anchor='n', fill=BOTH)
prev = ""

def on_tv_click(e):
    global editor, dunno_what_to_name_this, file_contents, prev, current_open_file
    
    selected_item = tv.focus()
    values = tv.item(selected_item)

    
    
    
    if os.path.isdir(tv_items[values['text']]):
        return
    current_open_file = tv_items[values["text"]]
    if dunno_what_to_name_this == True: file_contents[prev]["content"] = editor.get("1.0", END)
    
    editor.delete("1.0","end")
    if file_contents[values['text']]["readable"]:
        editor.insert("1.0", file_contents[values['text']]["content"])
    else:
        messagebox.showerror('Error', "cant read")
    
    dunno_what_to_name_this = True
    prev = values["text"].replace("\\", "/").split('/')[-1]
    
def save_binding(e):
    save()

#tv.bind("<ButtonRelease-1>", on_tv_click)
#root.bind("<Control-s>", save_binding)

def file_opener_hp():
    homepage.pack_forget()
    root.config(menu=nav_bar)
    frame.pack(side=RIGHT, expand=True, fill=BOTH)

    #f.pack(side=LEFT, fill=BOTH)

    #tv.bind("<ButtonRelease-1>", on_tv_click)
    root.bind("<Control-s>", save_binding)
    open_file()

    global mode
    mode = "file"

def folder_opener_hp():
    
    homepage.pack_forget()
    root.config(menu=nav_bar)
    frame.pack(side=RIGHT, expand=True, fill=BOTH)
    folder = askdirectory()
    
    f.pack(side=LEFT, fill=BOTH)

    tv.bind("<ButtonRelease-1>", on_tv_click)
    root.bind("<Control-s>", save_binding)

    make_tv(folder)
    f.pack_forget()
    f.pack(side=LEFT, fill=BOTH)
    

    global mode
    mode = "folder"
    


homepage = Frame(root)

zetext = Label(homepage, text="ZeText", anchor=CENTER).pack()
open_file_hp = Button(homepage, text="Open File", anchor=CENTER, command=file_opener_hp).pack()
open_folder_hp = Button(homepage, text="Open Folder", anchor=CENTER, command=folder_opener_hp).pack()

homepage.pack()



root.mainloop()
#file_contents[values["text"].replace("\\", "/").split('/')[-1]]["content"] = editor.get("1.0", END)
'''
root.config(menu=nav_bar)
frame.pack(side=RIGHT, expand=True, fill=BOTH)
editor.pack(expand=True, fill=BOTH, padx=(5,0))
console_toggle_button.pack(fill=BOTH)
console.pack(side=BOTTOM, expand=True, fill=BOTH)
f.pack(side=LEFT, fill=BOTH)
tree_toggle.pack(side=TOP, fill=BOTH)
tv.pack(expand=TRUE, anchor='n', fill=BOTH)
tv.bind("<ButtonRelease-1>", on_tv_click)
root.bind("<Control-s>", save_binding)
'''
