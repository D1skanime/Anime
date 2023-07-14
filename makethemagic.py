import os
import shutil
import tkinter as tk
from tkinter import simpledialog

def makethemagic(path, folder_name, AnimeType, Animename, Gruppe, inhalt):
    root = tk.Tk()
    root.withdraw()

    for folge in os.listdir(path):
        folge_pfad = os.path.join(path, folge)
        if os.path.isfile(folge_pfad):
            folge_name, folge_ext = os.path.splitext(folge)
            if folge in Animename:
                new_name = Animename.get(folge, [''])[0]
                neue_folge_name = f"{new_name}.{AnimeType}.E{Animename[folge][1]}{Gruppe}{folge_ext}"
                neue_folge_pfad = os.path.join(path, neue_folge_name)
                if os.path.exists(neue_folge_pfad):
                    print(f"Die Datei '{neue_folge_name}' existiert bereits.")
                    user_input = simpledialog.askstring("Datei existiert bereits", f"Die Datei '{neue_folge_name}' existiert bereits. Geben Sie einen anderen Namen ein oder drücken Sie 'Cancel', um den Vorgang abzubrechen:", parent=root)
                    if user_input is not None:
                        neue_folge_name = user_input
                        neue_folge_pfad = os.path.join(path, neue_folge_name)
                    else:
                        continue
                os.rename(folge_pfad, neue_folge_pfad)

    # Ordnername aktualisieren
    if folder_name != inhalt:
        # Überprüfen, ob im 'path' ein Ordner existiert, der genau den Namen 'folder_name' hat
        existing_folder_path = os.path.join(os.path.dirname(path), folder_name)
        if os.path.exists(existing_folder_path) and os.path.isdir(existing_folder_path):
            for file_name in os.listdir(path):
                source_file = os.path.join(path, file_name)
                destination_file = os.path.join(existing_folder_path, file_name)
                if os.path.isfile(source_file) and os.path.isfile(destination_file):
                    shutil.copyfile(source_file, destination_file)  # Daten überschreiben
            shutil.rmtree(path)  # Ursprünglichen Ordner löschen
        return

