import tkinter as tk
from tkinter import ttk
from notes_tab import NotesTab


window = tk.Tk()
window.title("Tab Widget")
window.config(padx=20,pady=20)
tabControl = ttk.Notebook(window)

tab1 = NotesTab(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Tab 1')
tabControl.add(tab2, text ='Tab 2')
tabControl.grid(column=0,row=0)

ttk.Label(tab2,text ="Lets dive into the world of computers").grid(column = 0,row = 0,padx = 30,pady = 30)



window.mainloop()