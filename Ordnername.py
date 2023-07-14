import os
import re
import shutil
import tkinter as tk


def load_gui_and_get_folder_name(inhalt):
    root = tk.Tk()
    root.title("Ordnerbenennung")
    
    label = tk.Label(root, text="Ordnername eingeben:")
    label.pack()
    
    entry = tk.Entry(root)
    entry.insert(tk.END, inhalt)
    entry.pack()
    
    def handle_button_click():
        global new_folder_name
        new_folder_name = entry.get()
        root.destroy()
    
    button = tk.Button(root, text="OK", command=handle_button_click)
    button.pack()
    
    root.mainloop()
    
    return new_folder_name

SonderzeichenListe = ["/","?","*","<",">","''","|",":"]

#funktion unbennen des Ordnername wie Anime oder neuer Name
def Ordnername(inhalt):
    newOrdnerAnimename = load_gui_and_get_folder_name(inhalt)
    newOrdnerAnimename= KillSpezialBuchtaben(newOrdnerAnimename)
    return(newOrdnerAnimename)

def KillSpezialBuchtaben(Animename):
    for SonderZeichen in SonderzeichenListe:
        if(Animename.find(SonderZeichen)) !=-1:
            if SonderZeichen =="?":
                Animename = Animename.replace(SonderZeichen, "!")
            else:    
                Animename = Animename.replace(SonderZeichen, "")
        return Animename