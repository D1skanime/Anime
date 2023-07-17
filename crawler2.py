from gettext import find
import os
from pathlib import Path
import glob
from reprlib import recursive_repr
import shutil
from token import ENCODING
import tkinter as tk
from tkinter import messagebox

from delete_images import delete_images
from delete_ordner import delete_ordner
from finde_groupname import finde_groupname
from findname import findname
from Ordnername import Ordnername
from makethemagic import makethemagic
from tag_source import tag_source

                                       
import tkinter as tk
from tkinter import filedialog

def select_path():
    root = tk.Tk()
    root.withdraw()  # Verstecke das Hauptfenster

    path = filedialog.askdirectory(title="Pfad auswählen")  # Öffne den Datei-Dialog zum Auswählen eines Ordners
    root.destroy()  # Schließe das Hauptfenster
    return path

# Beispielaufruf
spath = select_path()
      
#do do : Log file erstellen, speichere jeden Ordnername der erfolgreich # war in den Log file. 
# Verlgeiche bei jeder neu ausführung welche ordner schon gemacht sind anhand des Log files

def SaveLogFile(folder_name):
    Animetexteintragneu = open(PathvonLogDatei, "a")
    Animetexteintragneu.write("\n" + folder_name)
    Animetexteintragneu.close()
    return

def OpenLogFile(PathvonLogDatei):
    Animetexteintrag = []
    with open(PathvonLogDatei, 'r', encoding="cp1252") as f:
        Animetexteintrag = [_.rstrip('\n') for _ in f]
    return(Animetexteintrag)
    

SourceList = [
    ".mp4",
    ".mov",
    ".avi",
    ".wmv",
    ".flv",
    ".mkv",
    ".webm",
    ".3gp",
    ".mpg",
    ".mpeg",
    ".rm",
    ".rmvb",
    ".vob",
    ".m4v",
    ".ts",
    ".m2ts",
    ".f4v",
    ".divx",
    ".ogv",
    ".ogm",
    ".asf",
    ".mxf",
    ".flv",
    ".mpg",
    ".webm"]


path = r"C:\Users\admin\Desktop\Test"
Gruppe = []
  
if os.path.exists(path) == True:
    #Ordnerinhalt aufliste
    PathvonLogDatei = r'C:\Users\admin\Desktop\Animelog.txt'
    path_text = r"C:\Users\admin\Desktop\Gruppen.txt"
    #Lof file öffnen
    Animetexteintragzumvergleich = OpenLogFile(PathvonLogDatei)
    Inhalte = os.listdir(path)
    #Inhalt vergleichen
    Inhalte = list(set(Inhalte) - set(Animetexteintragzumvergleich))
    Inhalte.sort() 
    for inhalt in Inhalte:
        #if inhalt.endswith(EndungOrdner) == True:
           # Ordnerinhalt lesen und Bilder löschen
            delete_images(os.path.join(path, inhalt))
            delete_ordner(os.path.join(path, inhalt))
            folder_name = Ordnername(inhalt)
            AnimeType = tag_source()
            #Baut eine Dic mit ursprüglicher name folge name neuer Name 
            Animename = findname(os.path.join(path, inhalt),folder_name, SourceList)
            Gruppe = finde_groupname(os.path.join(path, inhalt), SourceList,path_text)
              
            folder_name =makethemagic(os.path.join(path, inhalt),folder_name, AnimeType, Animename,Gruppe,inhalt)
            SaveLogFile(folder_name)