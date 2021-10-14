import tkinter as tk
from PIL import ImageTk, Image
from resource_path import resource_path

root = tk.Tk()

on_image = ImageTk.PhotoImage(Image.open(resource_path("unchecked.png")).resize((25, 25)))
off_image = ImageTk.PhotoImage(Image.open(resource_path("checked.png")).resize((25, 25)))

var1 = tk.IntVar(value=1)
var2 = tk.IntVar(value=0)
cb1 = tk.Checkbutton(root, image=off_image, selectimage=on_image, indicatoron=False,
                     onvalue=1, offvalue=0, variable=var1, borderwidth=0)

cb1.pack(padx=20, pady=10)

root.mainloop()