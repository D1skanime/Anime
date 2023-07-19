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

def makethemagic(path, folder_name, AnimeType, Animename, Gruppe, inhalt):
    app = get_application_instance()
    rename_dialog = RenameDialog()
    new_name = None

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
                    neue_folge_name = f"{new_name}.{AnimeType[1]} {Animename[folge][1]}{Gruppe}{folge_ext}"
                neue_folge_pfad = os.path.join(path, neue_folge_name)
                if os.path.exists(neue_folge_pfad):
                    rename_dialog.get_new_name(neue_folge_name)
                    new_name = None  # Warten auf Benutzerantwort
                else:
                    try:
                        os.rename(folge_pfad, neue_folge_pfad)
                    except OSError as e:
                        QMessageBox.critical(None, "Fehler beim Umbenennen", f"Fehler beim Umbenennen von {folge}: {e.strerror}")
   
    if folder_name != inhalt:
        # Überprüfen, ob im 'path' ein Ordner existiert, der genau den Namen 'folder_name' hat
        existing_folder_path = os.path.join(os.path.dirname(path), folder_name)
        if os.path.exists(existing_folder_path) and os.path.isdir(existing_folder_path):
            for file_name in os.listdir(path):
                source_file = os.path.join(path, file_name)
                destination_file = os.path.join(existing_folder_path, file_name)
                if os.path.isfile(source_file) and os.path.isfile(destination_file):
                    try:
                        shutil.copyfile(source_file, destination_file)  # Daten überschreiben
                    except OSError as e:
                        QMessageBox.critical(None, "Fehler beim Kopieren", f"Fehler beim Kopieren von {source_file}: {e.strerror}")
            try:
                shutil.rmtree(path)  # Ursprünglichen Ordner löschen
            except OSError as e:
                QMessageBox.critical(None, "Fehler beim Löschen", f"Fehler beim Löschen des Ordners {path}: {e.strerror}")
        else:
            new_inhalt_folder_path = os.path.join(os.path.dirname(path), folder_name)
            try:
                os.rename(path, new_inhalt_folder_path)
            except OSError as e:
                QMessageBox.critical(None, "Fehler beim Umbenennen", f"Fehler beim Umbenennen von {path}: {e.strerror}")

    return folder_name
