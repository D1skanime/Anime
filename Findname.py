import os
import re
import shutil
import tkinter as tk

def Findname(path, Animename, SourceList):
    Files = os.listdir(path)
    Videofiles = {}
    for File in Files:
        VideoSourcetype = Source(File, SourceList)
        if VideoSourcetype:
            Videofiles[File] = [Animename]
            folge_nummer = find_folge_nummer(File)
            Videofiles[File].append(folge_nummer)
            print(File, "-------", folge_nummer)
    
    if VideoSourcetype:
        updated_files = create_gui(Files, Videofiles)
    return updated_files


def create_gui(Files, Videofiles):
    # GUI erstellen
    root = tk.Tk()
    root.title("Folgenliste")

    # Funktion zum Speichern der neuen Folgennummern
    def save_changes():
        for i, file in enumerate(sorted(Videofiles, key=lambda x: int(Videofiles[x][1]))):
            new_folge_nummer = entry_boxes[i].get()
            if new_folge_nummer != Videofiles[file][1]:
                Videofiles[file][1] = new_folge_nummer
        root.destroy()  # GUI schließen  

    # Textlabels und Entry-Boxes erstellen
    entry_boxes = []
    for file in sorted(Videofiles, key=lambda x: int(Videofiles[x][1])):
        folge_name = file
        folge_nummer = Videofiles[file][1]

        label = tk.Label(root, text=folge_name)
        label.pack()

        entry_box = tk.Entry(root)
        entry_box.insert(tk.END, folge_nummer)
        entry_box.pack()

        entry_boxes.append(entry_box)

    # Button zum Speichern der Änderungen
    save_button = tk.Button(root, text="OK", command=save_changes)
    save_button.pack()

    # GUI starten
    root.mainloop()
    return Videofiles


def Source(filename, SourceList):
    for source in SourceList:
        if filename.lower().endswith(source):
            return source
    return None

def find_folge_nummer(filename):
    # Muster SxxExx
    match = re.search(r"S\d{2}E(\d{2})", filename)
    if match:
        folge_nummer = match.group(1)
        return folge_nummer
    # Muster SxxExxx
    match = re.search(r"S\d{2}E(\d{3})", filename)
    if match:
        folge_nummer = match.group(1)
        return folge_nummer
    # Ignoriert []{}()
    match = re.search(r"\b(\d+)\b(?!\.\w+$)(?![\[\(\{]).*?$", filename[::-1])
    if match:
        folge_nummer = match.group(1)[::-1]
        return folge_nummer
    # Muster 00x erkennen
    match = re.search(r"(\d{2,})\D*$", filename[::-1])
    if match:
        folge_nummer = match.group(1)[::-1]
        return folge_nummer
    return 0