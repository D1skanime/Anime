import os

def makethemagic(path, folder_name, AnimeType, Animename, Gruppe,inhalt):
    for folge in os.listdir(path):
        folge_pfad = os.path.join(path, folge)
        if os.path.isfile(folge_pfad):
            folge_name, folge_ext = os.path.splitext(folge)
            if folge in Animename:
                new_name = Animename.get(folge , [''])[0]
                neue_folge_name = f"{new_name}.{AnimeType}.{Animename[folge ][1]}{Gruppe}{folge_ext}"
                neue_folge_pfad = os.path.join(path, neue_folge_name)
                if os.path.exists(neue_folge_pfad):
                    print(f"Die Datei '{neue_folge_name}' existiert bereits.")
                    user_input = input("Geben Sie einen anderen Namen ein oder drücken Sie 'Enter', um den Vorgang abzubrechen: ")
                    if user_input:
                        neue_folge_name = user_input
                        neue_folge_pfad = os.path.join(path, neue_folge_name)
                    else:
                        continue
                os.rename(folge_pfad, neue_folge_pfad)
    
    # Ordnername aktualisieren
    if folder_name != inhalt:
        os.rename(path, os.path.join(os.path.dirname(path), folder_name))
        path = os.path.join(os.path.dirname(path), folder_name)  
    return 

