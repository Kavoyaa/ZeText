
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.simpledialog import askstring
from tkinter import ttk
from ttkthemes import themed_tk as tk
import subprocess

root = tk.ThemedTk()
root.get_themes()
root.set_theme("plastik")
root.title("Untitled - ZeText")

default_file_path = ""
run_command = ""

def show_console():
    console.configure(height=10)

def hide_console():
    console.configure(height=0)

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
    
    process = subprocess.Popen(
        run_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)

    output, error = process.communicate()
    console.insert(END, output)
    console.insert(END, error)

def set_run_command():
    global run_command
    run_command = askstring(title="Set Run Command", prompt="Eg: python main.py\n(Make sure to type the correct file path.)")
    print(run_command)

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
    print("e"+ default_file_path)
    
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
nav_bar = Menu(root, background="#e3e4ea")

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
edit_button = Menu(nav_bar, tearoff=0, background="#e3e4ea")

nav_bar.add_cascade(label="Edit", menu=edit_button)

# Run button
run_button = Menu(nav_bar, tearoff=0, background="#e3e4ea")

run_button.add_command(label="Run", command=run)
run_button.add_command(label="Set Run Command", command=set_run_command)

nav_bar.add_cascade(label="Run", menu=run_button)

# Console button
console_button = Menu(nav_bar, tearoff=0, background="#e3e4ea")

console_button.add_command(label="Show Console", command=show_console)
console_button.add_command(label="Hide Console", command=hide_console)

nav_bar.add_cascade(label="Console", menu=console_button)

root.config(menu=nav_bar)


scrollbar = ttk.Scrollbar(root, orient='vertical')
scrollbar.pack(side=RIGHT, fill='y')

editor = Text(yscrollcommand=scrollbar.set, highlightthickness=0, bd=0, relief=tk.FLAT)
scrollbar.config(command=editor.yview)

editor.pack(expand=True, fill=BOTH)

console = Text(height=10, bg="#e3e4ea", highlightthickness=0, bd=0, relief=tk.FLAT)
console.pack(expand=True, fill=BOTH)


root.mainloop()
