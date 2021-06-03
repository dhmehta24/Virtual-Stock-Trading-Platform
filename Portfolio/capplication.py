import tkinter
from tkinter import Tk
from tkinter import messagebox as mb

app = Tk()

app.title("Please Select An Option")
app.geometry("300x100")

def c_function():

    sts = mb.askyesno("Verify","Are You Sure ?")

    if sts:
        mb.showerror("Error","Exit has not implemented yet !!")

    else:
        mb.showinfo("Info", "Exit has been cancelled")


ent = tkinter.Button(app, text = "Enter", command = lambda:mb.showerror("Error","Sorry, Nowhere to enter")).pack()
ext = tkinter.Button(app, text = "Exit", command = c_function).pack()

app.mainloop()

