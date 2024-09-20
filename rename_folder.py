import os
import shutil
from PyQt5.QtWidgets import  QMessageBox


def rename_folder(path, new_ordername, ordnername_orgin):
    #Erstelle backdrops ordner
    os.makedirs(os.path.join(path, "backdrops"))
    #Orderprüfem
    path = os.path.dirname(path)
    if ordnername_orgin == new_ordername:
        return new_ordername
    else:
        if os.path.exists(path) and os.path.isdir(path):
            
            for ordern_name in os.listdir(path):
                if ordern_name == new_ordername:
                    move_data(new_ordername, path, ordnername_orgin)
                    return
            else:
                new_foldername_path = os.path.join(path, new_ordername)
                existing_foldername_path = os.path.join(path, ordnername_orgin)
                try:
                    os.rename(existing_foldername_path, new_foldername_path)
                except OSError as e:
                    QMessageBox.critical(None, "Fehler beim Umbenennen", f"Fehler beim Umbenennen von {path}: {e.strerror}")

                return 

def move_data(new_ordername, path, ordnername_orgin):
    destination_folder = os.path.join(path, new_ordername)
    existing_folder_path = os.path.join(path, ordnername_orgin)

    for root, dirs, files in os.walk(existing_folder_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_folder, file)
            #Prüfen ob Datei schon im Zielorder existiert.
            if os.path.exists(destination_file_path):
                try:
                    # Vorhandene Datei im Zielverzeichnis löschen
                    os.remove(destination_file_path)  
                except OSError as e:
                    print(f"Fehler beim Löschen der Datei {destination_file_path}: {e.strerror}")

            try:
                # Datei ins Zielverzeichnis kopieren und Metadaten beibehalten
                shutil.copy2(source_file_path, destination_folder)  
                print(f"Datei kopiert: {file}")
            except OSError as e:
                print(f"Fehler beim Kopieren der Datei {file}: {e.strerror}")
    print("schlaufe ist fertig")
    if os.path.exists(existing_folder_path):
       shutil.rmtree(existing_folder_path)  # Ursprünglichen Ordner löschen
       print(f"Ursprünglicher Ordner gelöscht: {existing_folder_path}")


if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\test"
    ordnername_orgin = "test2"
    videofiles = {
        'A Town Where You Live.Bonus.S01E01-GruppeKampfkuchen.mkv': ['test3', 'A Town Where You Live', 'AMV', '', '02', '01-23', 'GruppeKampfkuchen', '.mkv','A Town Where You Live.Bonus.S01E01-GruppeKampfkuchen.mkv'],
        'MM__02.mkv': ['Test', 'A Town Where You Live', 'Film', '2012', '02', '02', 'GruppeKampfkuchen', '.mkv','A Town Where You Live.Bonus.S01E02-GruppeKampfkuchen.mkv'],
        'MM__03.mkv': ['Test', 'A Town Where You Live', '', '', '00', '03', 'GruppeKampfkuchen', '.mkv','A Town Where You Live.Bonus.S01E03-GruppeKampfkuchen.mkv']
    }
    rename_folder(path, videofiles[next(iter(videofiles))][0], ordnername_orgin) 
               
