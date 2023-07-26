import os
import shutil
from PyQt5.QtWidgets import  QMessageBox


def rename_folder(path, folder_name, orgin_item):
    for item in os.listdir(path):
        if item == folder_name:
            move_data(item,path, orgin_item)
            return
    else:
        new_foldername_path = os.path.join(path, folder_name)
        existing_foldername_path = os.path.join(path, orgin_item)
        print(new_foldername_path)
        print(existing_foldername_path)
        try:
            os.rename(existing_foldername_path, new_foldername_path)
        except OSError as e:
            QMessageBox.critical(None, "Fehler beim Umbenennen", f"Fehler beim Umbenennen von {path}: {e.strerror}")

        return 
    
        # Kein Element mit dem Namen folder_name gefunden
    # Überprüfen, ob das Verzeichnis existiert und ein Verzeichnis ist
def move_data(item, path, orgin_item):
    print(item)
    print(path)
    destination_folder = os.path.join(path, item)
    existing_folder_path = os.path.join(path, orgin_item)
    print("source_file", destination_folder)
    print("existing_folder_path", existing_folder_path)

    for root, dirs, files in os.walk(existing_folder_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_folder, file)

            if os.path.exists(destination_file_path):
                try:
                    os.remove(destination_file_path)  # Vorhandene Datei im Zielverzeichnis löschen
                except OSError as e:
                    print(f"Fehler beim Löschen der Datei {destination_file_path}: {e.strerror}")

            try:
                shutil.copy2(source_file_path, destination_folder)  # Datei ins Zielverzeichnis kopieren und Metadaten beibehalten
                print(f"Datei kopiert: {file}")
            except OSError as e:
                print(f"Fehler beim Kopieren der Datei {file}: {e.strerror}")
    print("schlaufe ist fertig")


            

    if os.path.exists(existing_folder_path):
       shutil.rmtree(existing_folder_path)  # Ursprünglichen Ordner löschen
       print(f"Ursprünglicher Ordner gelöscht: {existing_folder_path}")


if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\Test"
    folder_name = "Demon.Slayer.Kimetsu 1"
    orgin_item = "Demon.Slayer.Kimetsu"
    existing_folder_path = 'C:\\Users\\admin\\Desktop\\Demon.Slayer.Kimetsu'
    if not path:
        print(f"Der angegebene Pfad '{path}' existiert nicht.")
    else:
        rename_folder(path, folder_name, orgin_item)        
