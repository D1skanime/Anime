import os
import re
import shutil
import tkinter as tk


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