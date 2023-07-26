import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

#Skripte
from delete_images import delete_images
from delete_ordner import delete_ordner
from finde_groupname import finde_groupname
from findname import findname
from Ordnername import Ordnername
from makethemagic import makethemagic
from tag_source import tag_source
from rename_folder import rename_folder
from app import app


from style import apply_dark_theme

apply_dark_theme(app)

def select_path(title):
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title=title)
    root.destroy()
    return path

def select_file_path(title):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title)
    root.destroy()
    return file_path

def save_log_file(folder_name, log_file_path):
    with open(log_file_path, "a") as file:
        file.write("\n" + folder_name)

def open_log_file(file_path):
    with open(file_path, 'r', encoding="cp1252") as file:
        entries = [line.rstrip('\n') for line in file]
    return entries

def main():
    # Beispielaufruf
    #path = select_path("Pfad auswählen")
    #PathvonLogDatei = select_file_path("Log-Datei auswählen")
    #path_text = select_file_path("Gruppen-Textdatei auswählen")
    # Für Test
    path = r"C:\Users\admin\Desktop\Test"
    PathvonLogDatei = r"C:\Users\admin\Desktop\Animelog.txt"
    path_text = r"C:\Users\admin\Desktop\Gruppen.txt"

    if not os.path.exists(path):
        print(f"Der angegebene Pfad '{path}' existiert nicht.")
        return
    
    source_list = [
        ".mp4", ".mov", ".avi", ".wmv", ".flv", ".mkv", ".webm", ".3gp", ".mpg", ".mpeg", ".rm", ".rmvb", ".vob",
        ".m4v", ".ts", ".m2ts", ".f4v", ".divx", ".ogv", ".ogm", ".asf", ".mxf", ".flv", ".mpg", ".webm"
    ]

    try:
        log_entries = open_log_file(PathvonLogDatei)
        contents = [item for item in os.listdir(path) if item not in log_entries]
        contents.sort() 
        for item in contents:
            item_path = os.path.join(path, item)
            delete_ordner(item_path)
            delete_images(item_path)
            folder_name = Ordnername(item)
            animetype = tag_source()
            animename = findname(item_path, folder_name, source_list)
            print("Processing:", item_path)
            print("Animation Name:", animename)
            gruppe = finde_groupname(item_path, source_list, path_text)
            print("Group Name:", gruppe)
            makethemagic(item_path, folder_name, animetype, animename, gruppe, item)
            if item != folder_name:
                rename_folder(path, folder_name, item)
            else:
                 folder_name = item   
            save_log_file(folder_name, PathvonLogDatei)

    except Exception as e:
        print("Ein Fehler ist aufgetreten:")
        print(str(e))
    
main()
