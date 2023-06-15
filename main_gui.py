import tkinter as tk

root = tk.Tk() #creates root window
root.geometry("300x400") #set width=300 and height 200 px

sss


def start_program_button():
    print('Timer has started')


hello_label = tk.Label(root, text="Hello, welcome to study tracker")
hello_label.pack()

start_button = tk.Button(root, text="Click here to start counter", command=start_program_button, width=10, height=1)
start_button.pack()

entry = tk.Entry(root)
entry.pack()



root.mainloop() #main loop which waits for user input

