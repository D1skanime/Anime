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
                            




def Findname(path, Gruppe, Animename, AnimeType):
    Videofiles = os.listdir(path)
    Zähler = 0
    for Viedeofile in Videofiles:
        Zähler = Zähler + 1 
        VideoSourcetype = Source(Viedeofile)
        Zähler = str(Zähler).rjust(2, '0')
        if AnimeType != "":
            NewAnimeName = Animename + "." + AnimeType + "E" + Zähler + Gruppe + VideoSourcetype
        else:
            NewAnimeName = Animename + "." + Zähler + Gruppe + VideoSourcetype
    
        src = os.path.join(path, Viedeofile)
        dst = os.path.join(path, NewAnimeName)
    
        if os.path.exists(src):
            shutil.move(src, dst)
        else:
            print(f"Die Datei {src} wurde nicht gefunden.")            
                  
    
#Ordner im Verezeichnis Ordner löschen
#Ordnerkill = Path des Aktuellen Ordner in dem was gelöscht werden soll

      

def TagSource():
    SourceAnimeType = input("Serie: S0x\nBonus : B0x\n OVA : OVA0x\n TV-Spezial : TS0x\n AMV : AMV0x\n WEB: WEB0x\n Film: Enter \n:  ")
    return SourceAnimeType

def KillSpezialBuchtaben(Animename):
    for SonderZeichen in SonderzeichenListe:
        if(Animename.find(SonderZeichen)) !=-1:
            if SonderZeichen =="?":
                Animename = Animename.replace(SonderZeichen, "!")
            else:    
                Animename = Animename.replace(SonderZeichen, "")
        return Animename




   
          

#funktion du erkennt welchen Datei Type es ist und diese dann zurück schriebt

def Source(type):
    for source in SourceList:
        if source in type:
            return source   
#funktion unbennen des Ordnername wie Anime oder neuer Name
def RenameOrdner(Animename):
    print("----Inhalt =-------------"+ inhalt + "-------------------------")
    newOrdnerAnimename = input("Ordnername wie AktuellerOrdnername?: ")
    if newOrdnerAnimename == "j" or newOrdnerAnimename == "" or newOrdnerAnimename == "J":
        Animename = inhalt
        os.rename(path+"\\" + inhalt, path+"\\" + inhalt)
    elif newOrdnerAnimename == "n" or newOrdnerAnimename == "N":
        newOrdnerAnimename = input("Ordnername wie AnimeName?: ")
        if newOrdnerAnimename == "j" or newOrdnerAnimename == "" or newOrdnerAnimename == "J":
            os.rename(path+"\\" + inhalt, path+"\\" + Animename)
        elif newOrdnerAnimename == "n" or newOrdnerAnimename == "N":
            Animename = input("\nNeuer Ordnername: ""\n")
            os.rename(path+"\\" + inhalt, path+"\\" + Animename)
    return(Animename)
#do do : Log file erstellen, speichere jeden Ordnername der erfolgreich # war in den Log file. 
# Verlgeiche bei jeder neu ausführung welche ordner schon gemacht sind anhand des Log files

def SaveLogFile(Animename):
    Animetexteintragneu = open(PathvonLogDatei, "a")
    Animetexteintragneu.write("\n" + Animename)
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

SonderzeichenListe = ["/","?","*","<",">","''","|",":"]
    
#path = "C:\\Users\\D1sk\\Desktop\\xxxxxxx\\sss\\TestOrdner"
#EndungOrdner = input ("\nEndung eintragen: ")
#jpg = input("Sollen die JPG und png gelöscht werden, dann Tippe\n für Ja: J oder Enter\n für Nein: n\n...  ")
#path = input("\nPfad des Main Ordner eingeben der durchsucht werden soll: ""\n")
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
            Animename = input("---------------------------------------------\n Geben Sie den Animename des Animes: " )
            #Dodo Funktion die den Ainme auf : ? # überprüft und aus löscht oder ersetzt
            Animename = KillSpezialBuchtaben(Animename)
            AnimeType = TagSource()
            Gruppe = finde_groupname(os.path.join(path, inhalt), SourceList,path_text)
            Findname(os.path.join(path, inhalt),Gruppe, Animename, AnimeType)
            Animename = RenameOrdner(Animename)
            SaveLogFile(Animename)