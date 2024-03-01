import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from PyQt5.QtWidgets import QApplication, QFileDialog

#Skripte
from delete_images import delete_images
from delete_ordner import delete_ordner
from find_gruppe import find_gruppe_in_videofile
from makethemagic import makethemagic
from tag_videofile import tag_videofile
from rename_folder import rename_folder
from all_ordner import all_ordner
from videofiles import isvideofile
from find_nummer import find_folge_nummer
from remove_junke import remove_junke
from update_videofiles import create_gui
from buildnew_name import buildnew_name
from save_gruppe import save_gruppe
from fix_nummer import fix_nummer
from app import app


from style import apply_dark_theme

apply_dark_theme(app)

def select_path(title):
    root = tk.Tk()
    root.withdraw()
    result = all_ordner()
    path = filedialog.askdirectory(title=title)
    root.destroy()
    return path, result


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

def alle_funktionen(path_text, path, PathvonLogDatei, ordnername_orgin, source_list, typ_liste):
    delete_ordner(path)
    delete_images(path)
    daten = os.listdir(path)
    videofiles = isvideofile(daten, ordnername_orgin, source_list)
    videofiles = remove_junke(videofiles)
    videofiles = tag_videofile(videofiles)
    videofiles = find_gruppe_in_videofile(videofiles)
    videofiles = find_folge_nummer(videofiles)
    videofiles = create_gui(videofiles, path_text, typ_liste, path)
    videofiles = fix_nummer(videofiles)
    videofiles = buildnew_name(videofiles)
    makethemagic(path, videofiles)
    rename_folder(path, videofiles[next(iter(videofiles))][0], ordnername_orgin)  
    save_log_file(videofiles[next(iter(videofiles))][0], PathvonLogDatei)
    save_gruppe(path_text, videofiles)

def main():
    # Beispielaufruf
    path, result = select_path("Pfad auswählen")
    PathvonLogDatei = select_file_path("Log-Datei auswählen")
    path_text = select_file_path("Gruppen-Textdatei auswählen")
    # Für Test
    #path = r"A:/Anime/Serie/Anime.TV.Sub.unfertig"
    #PathvonLogDatei = r"C:\Users\admin\Desktop\Animelog.txt"
    #path_text = r"C:\Users\admin\Desktop\Gruppen.txt"

    if not os.path.exists(path):
        print(f"Der angegebene Pfad '{path}' existiert nicht.")
        return
    
    source_list = [
        ".mp4", ".mov", ".avi", ".wmv", ".flv", ".mkv", ".webm", ".3gp", ".mpg", ".mpeg", ".rm", ".rmvb", ".vob",
        ".m4v", ".ts", ".m2ts", ".f4v", ".divx", ".ogv", ".ogm", ".asf", ".mxf", ".flv", ".mpg", ".webm"
    ]

    typ_liste = [
        'OVA','Bonus','Film','AMV','TS','ONA'
    ]

    try:
        print(path)
        log_entries = open_log_file(PathvonLogDatei)
        if result == "one":
            ordnername_orgin = os.path.basename(path)
            alle_funktionen(path_text, path, PathvonLogDatei, ordnername_orgin, source_list, typ_liste)
        else:
            contents = [item for item in os.listdir(path) if item not in log_entries]
            contents.sort()
            for item in contents:
                path_ordnername_orgin = os.path.join(path, item)
                ordnername_orgin = os.path.basename(path_ordnername_orgin)
                alle_funktionen(path_text, path_ordnername_orgin, PathvonLogDatei, ordnername_orgin, source_list, typ_liste)     
    except Exception as e:
        print("Ein Fehler ist aufgetreten:")
        print(str(e))
    
main()
