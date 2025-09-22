import tkinter as tk
from tkinter import ttk

from chords_notes_tab import ChordNotesTab
from notes_tab import NotesTab
from retentive_notes import RetentiveNotesTab

window = tk.Tk()
window.title("Tab Widget")
window.config(padx=20,pady=20)
tabControl = ttk.Notebook(window)

tab1 = NotesTab(tabControl)
tab2 = ChordNotesTab(tabControl)
tab3 = RetentiveNotesTab(tabControl)

tabControl.add(tab1, text ='Notas')
tabControl.add(tab2, text ='Notas de acordes')
tabControl.add(tab3, text ='Retentiva')

tabControl.grid(column=0,row=0)

window.mainloop()