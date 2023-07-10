from gettext import find
import os
from pathlib import Path
import glob
from reprlib import recursive_repr
import shutil
from token import ENCODING


# lösche alle png im Verzechniss
def delete_images(folder_path):
    print("\nAktueller Ordner:", folder_path)
    response = input("Möchten Sie die JPG- und PNG-Dateien löschen? (J/N): ")
    if response.lower() == "j" or not response:
        image_extensions = ["jpg", "png", "gif", "bif", "nfo"]
        image_files = []
        for extension in image_extensions:
            image_files.extend(glob.glob(folder_path + "/*." + extension))

        # Anzeigen der gefundenen Dateien
        print("\nGefundene Dateien:")
        for i, file in enumerate(image_files, start=1):
            print(f"{i}. {file}")

        # Auswahl der zu löschenden Dateien
        delete_choices = input("Geben Sie die Nummern der Dateien ein, die gelöscht werden sollen (durch Leerzeichen getrennt): ")
        delete_choices = delete_choices.split()

        # Löschen der ausgewählten Dateien
        for choice in delete_choices:
            try:
                index = int(choice) - 1
                file = image_files[index]
                os.remove(file)
                print(f"{file} wurde gelöscht.")
            except (ValueError, IndexError):
                print(f"Ungültige Auswahl: {choice}")

    elif response.lower() == "n":
        pass
                            

#Finde den Gruppename für die Folge im Verzechnis
def FindGroupname(Path_des_Aktuellen_Ordner, Animename, AnimeType):
    Videofiles = os.listdir(Path_des_Aktuellen_Ordner)
    #Videofiles.sort()
    Zähler = 0
    print("------------------------------------------")
    print("\n".join(Videofiles)) 
    print("\n""------------------------------------------")
    Gruppename = input("Gruppename eingeben: ")
    for Viedeofile in Videofiles:
        Zähler = Zähler+1
        #if Viedeofile.startswith("["):
         #   EndIndex = find("]")
          #  Gruppe = "-"+(Viedeofile[1:EndIndex-1])
        if Gruppename == "":
            Gruppe = ("-null")
        else:
            Gruppe =  "-"+Gruppename     
        Findname(Viedeofile, Zähler, Gruppe, Animename, AnimeType)    
                  
    
#Ordner im Verezeichnis Ordner löschen
#Ordnerkill = Path des Aktuellen Ordner in dem was gelöscht werden soll
def DeleteOrdner(Ordnerkill):
    Verzeichnisse_kill =  [f.path for f in os.scandir(Ordnerkill) if f.is_dir()]
    for Verzechnis_kill in Verzeichnisse_kill:
        try:
            shutil.rmtree(Verzechnis_kill)
        except OSError as e:
            print(f"Error:{e.strerror}")
            #Ordner umbennen
    print(inhalt)         
    Animename = input("---------------------------------------------\n Geben Sie den Animename des Animes: " )
    #Dodo Funktion die den Ainme auf : ? # überprüft und aus löscht oder ersetzt
    Animename = KillSpezialBuchtaben(Animename)
    AnimeType = TagSource()
    FindGroupname(Ordnerkill, Animename, AnimeType)
    return Animename
      

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


def Findname(Viedeofile, Zähler, Gruppe, Animename, AnimeType):
    VideoSourcetype =   Source(Viedeofile)
    Zähler=str(Zähler).rjust(2, '0')
    if AnimeType != "": 
        NewAnimeName = Animename +"."+AnimeType+"E" + Zähler + Gruppe + VideoSourcetype
    else:
        NewAnimeName = Animename + "."+Zähler + Gruppe + VideoSourcetype    
    os.rename(path+"\\" + inhalt + "\\" + Viedeofile, path+"\\" + inhalt + "\\" + NewAnimeName)        
          

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
    

SourceList = [".avi", ".mkv", ".mp4",".wmv",".ogm","m4v"]
SonderzeichenListe = ["/","?","*","<",">","''","|",":"]
    
#path = "C:\\Users\\D1sk\\Desktop\\xxxxxxx\\sss\\TestOrdner"
#EndungOrdner = input ("\nEndung eintragen: ")
#jpg = input("Sollen die JPG und png gelöscht werden, dann Tippe\n für Ja: J oder Enter\n für Nein: n\n...  ")
path = input("\nPfad des Main Ordner eingeben der durchsucht werden soll: ""\n")
Gruppe = []
  
if os.path.exists(path) == True:
    #Ordnerinhalt auflisten
    PathvonLogDatei = 'A:\Anime\Animelog.txt'
    #Lof file öffnen
    Animetexteintragzumvergleich = OpenLogFile(PathvonLogDatei)
    Inhalte = os.listdir(path)
    #Inhalt vergleichen
    Inhalte = list(set(Inhalte) - set(Animetexteintragzumvergleich))
    Inhalte.sort() 
    for inhalt in Inhalte:
        #if inhalt.endswith(EndungOrdner) == True:
           #Ordnerinhalt lesen
            delete_images(path+"\\" +inhalt)
            Animename = DeleteOrdner(path+"\\" +inhalt)
            Animename = RenameOrdner(Animename)
            SaveLogFile(Animename)