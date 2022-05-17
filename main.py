from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.simpledialog import askstring
from tkinter import ttk
from ttkthemes import themed_tk as tk
import subprocess

root = tk.ThemedTk()
root.get_themes()
root.set_theme("yaru")
root.title("Untitled - ZeText")
root.minsize(350, 770)

default_file_path = ""
run_command = ""
console_content = ""
console_status = "visible"

def maximize_console():
    pass

def minimize_console():
    pass

def show_console():
    global console_status
    if console_status == "visible":
        return

    global console
    console = Text(height=10, bg="#e3e4ea", highlightthickness=0, bd=0, relief=FLAT, state=DISABLED, font=("sans-serif", 15))
    console.pack(expand=True, fill=BOTH)
    console.insert("1.0", console_content)
    console_status="visible"

def hide_console():
    global console_status
    global console
    console_status = "hidden"
    console.destroy()

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
        file_path = asksaveasfilename()

        with open(file_path, "w") as file:
            code = editor.get("1.0", END)
            file.write(code)
        
        default_file_path = file_path
        file_name = default_file_path.split("/")[-1]
        root.title(f"{file_name} - ZeText")

    if run_command == "":
        run_command = askstring(title="Set Run Command", prompt="Eg: python main.py\n(Make sure to type the correct file path.)")

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
file_button.add_command(label="Open File", command=open_file)
file_button.add_command(label="Open Folder")
file_button.add_command(label="Save", command=save)
file_button.add_command(label="Save As...", command=save_as)
file_button.add_command(label="Close Window")
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

root.config(menu=nav_bar)

scrollbar = ttk.Scrollbar(root, orient='vertical')
scrollbar = ttk.Scrollbar()
scrollbar.pack(side=RIGHT, fill='y')

editor = Text(yscrollcommand=scrollbar.set, highlightthickness=0, bd=0, relief=FLAT, font=("sans-serif", 15))
scrollbar.config(command=editor.yview)
editor.pack(expand=True, fill=BOTH)

console_toggle_button = Button(text="CONSOLE", bg="#d0d1d6", anchor="w", bd=0, relief=FLAT, activebackground="#bebfc4", command=console_toggle)
console_toggle_button.pack(fill=BOTH)

console = Text(height=10, bg="#e3e4ea", highlightthickness=0, bd=0, relief=FLAT, state=DISABLED, font=("sans-serif", 15))
console.pack(side=BOTTOM, expand=True, fill=BOTH)

root.mainloop()
