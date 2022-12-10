from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.simpledialog import askstring
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import themed_tk as tk
import subprocess
import time

root = tk.ThemedTk()
root.get_themes()
root.set_theme("yaru")
root.title("Untitled - ZeText")
root.minsize(350, 770)

default_file_path = ""
run_command = ""
console_content = ""
console_status = "visible"
theme = "light"

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
    primary_colour = askstring(title="Set Primary Colour", prompt="Type hexcode of the colour.")
    try:
        update_widgets()
    except:
        messagebox.showerror("Error", "Invalid hex code.")

def set_secondary_colour():
    global secondary_colour
    secondary_colour = askstring(title="Set Secondary Colour", prompt="Type hexcode of the colour.")
    try:
        update_widgets()
    except:
        messagebox.showerror("Error", "Invalid hex code.")

def set_text_colour():
    global text_colour
    text_colour = askstring(title="Set Text Colour", prompt="Type hexcode of the colour.")
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
    console = Text(height=10, bg=secondary_colour, highlightthickness=0, bd=0, relief=FLAT, state=DISABLED, font=("sans-serif", 15), fg=text_colour)
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
    file_path = asksaveasfilename()

    with open(file_path, "w") as file:
        code = editor.get("1.0", END)
        file.write(code)
    
    global default_file_path
    default_file_path = file_path
    file_name = default_file_path.split("/")[-1]
    root.title(f"{file_name} - ZeText")

def save():
    global default_file_path
    
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

root.config(menu=nav_bar)



editor = Text(highlightthickness=0, bd=0, relief=FLAT, font=("sans-serif", 15), bg=primary_colour)

editor.pack(expand=True, fill=BOTH)

console_toggle_button = Button(text="CONSOLE ⮟", bg=secondary_colour, anchor="w", bd=0, relief=FLAT, activebackground="#bebfc4", command=console_toggle)
console_toggle_button.pack(fill=BOTH)

console = Text(height=10, bg=secondary_colour, highlightthickness=0, bd=0, relief=FLAT, state=DISABLED, font=("sans-serif", 15))
console.pack(side=BOTTOM, expand=True, fill=BOTH)

root.mainloop()
