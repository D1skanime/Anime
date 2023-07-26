import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QInputDialog
from PyQt5.QtCore import pyqtSignal, QObject

class RenameDialog(QObject):
    name_entered = pyqtSignal(str)

    def get_new_name(self, default_name):
        app = get_application_instance()
        new_name, ok = QInputDialog.getText(None, "Datei existiert bereits", "Neuer Dateiname:", QLineEdit.Normal, default_name)
        if ok:
            self.name_entered.emit(new_name)

def get_application_instance():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

def makethemagic(path, folder_name, AnimeType, Animename, Gruppe, inhalt, dummy_files=None, dummy_folders=None):
    app = get_application_instance()
    rename_dialog = RenameDialog()
    new_name = None

    if dummy_files is None:
        dummy_files = []
    if dummy_folders is None:
        dummy_folders = []

    if not dummy_files and not dummy_folders:
        # Wenn keine Dummy-Daten übergeben wurden, verwende die echten Daten
        for folge in os.listdir(path):
            folge_pfad = os.path.join(path, folge)
            if os.path.isfile(folge_pfad):
                folge_name, folge_ext = os.path.splitext(folge)
                if folge in Animename:
                    new_name = Animename.get(folge, [''])[0]
                    # Überprüfung, ob einer der beiden Werte leer ist
                    if "" not in AnimeType:
                        # BONUS,OVA ONA WEB Spezial
                        neue_folge_name = f"{new_name}.{AnimeType[1]}.{AnimeType[0]}E{Animename[folge][1]}{Gruppe}{folge_ext}"
                    elif AnimeType[1] == "":
                        # Serie
                        neue_folge_name = f"{new_name}.{AnimeType[0]}E{Animename[folge][1]}{Gruppe}{folge_ext}"
                    else:
                        # Film AMV
                        neue_folge_name = f"{new_name} {Animename[folge][1]}{Gruppe}{folge_ext}"
                    neue_folge_pfad = os.path.join(path, neue_folge_name)
                    if os.path.exists(neue_folge_pfad):
                        rename_dialog.get_new_name(neue_folge_name)
                        new_name = None  # Warten auf Benutzerantwort
                    else:
                        try:
                            os.rename(folge_pfad, neue_folge_pfad)
                        except OSError as e:
                            QMessageBox.critical(None, "Fehler beim Umbenennen", f"Fehler beim Umbenennen von {folge}: {e.strerror}")


if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\Test\Demon.Slayer.Kimetsu"
    Animename = {'Demon.Slayer.Kimetsu.S01E02.mkv': ['Demon.Slayer.Kimetsu 3', '04'], 'Demon.Slayer.Kimetsu.S01E05.mkv': ['Demon.Slayer.Kimetsu 3', '06']}
    sourcelist = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv', '.webm', '.3gp', '.mpg', '.mpeg', '.rm', '.rmvb', '.vob', '.m4v']
    AnimeType = ('S01', '')
    Gruppe = ""
    inhalt = "Dämon"
    folder_name = 'Demon.Slayer.Kimetsu 3'

    # Erstellen von Dummy-Dateinamen und Dummy-Ordner
    dummy_file_names = ["file1.mp4", "file2.mkv", "file3.avi"]
    dummy_folder_names = ["folder1", "folder2", "folder3"]

    # Testen des Kopierens und Löschens von Dateien und Ordnern
    # Erstellen von Dummy-Dateinamen und -Ordnern, die in der Funktion kopiert und gelöscht werden
    dummy_files_to_copy = ["file1.mp4", "file2.mkv"]
    dummy_files_to_delete = ["file3.avi"]

    if not path:
        print(f"Der angegebene Pfad '{path}' existiert nicht.")
    else:
        makethemagic(path, folder_name, AnimeType, Animename, Gruppe, inhalt, dummy_file_names, dummy_folder_names)
        print("")
