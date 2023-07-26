import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QInputDialog, QDialog, QSizePolicy  # Importiere QSizePolicy
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QSize  
from PyQt5.QtGui import QPalette, QFont  
from app import app
from style import apply_dark_theme

apply_dark_theme(app)

class RenameDialog(QDialog):
    name_entered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neuer Dateiname")
        #self.setFixedSize(400, 150)  # Anfangsgröße festlegen
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)  # Setze die Größenrichtlinie des Dialogs auf Minimum

        layout = QVBoxLayout()

        self.label = QLabel("Datei existiert bereits")
        self.label.setStyleSheet("font-size: 16px; color: white;")
        layout.addWidget(self.label)

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Neuer Dateiname")
        layout.addWidget(self.line_edit)

        self.ok_button = QPushButton("OK")
        self.ok_button.setStyleSheet("font-size: 14px; padding: 6px; background-color: #4CAF50; color: white;")
        self.ok_button.clicked.connect(self.on_ok_button_clicked)
        layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setStyleSheet("font-size: 14px; padding: 6px; background-color: #f44336; color: white;")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)
        self.line_edit.setFocus()

        # Dunkles Hintergrund-Stylesheet für den Dialog und das Eingabefeld
        self.setStyleSheet("""
            QDialog {
                background-color: #333;
            }
            
            QLineEdit {
                background-color: #444;
                color: white;
                border: 1px solid #888;
                font-size: 14px;
                padding: 4px;
            }
        """)

    def on_ok_button_clicked(self):
        new_name = self.line_edit.text()
        self.name_entered.emit(new_name)
        self.accept()

    def get_new_name(self, Test_folgen):
        self.line_edit.setText(Test_folgen)  # Wert von Test_folgen in das Eingabefeld setzen
        self.adjustSize()  # Größe des Dialogs aktualisieren
        result = self.exec_()  # Dialog öffnen und warten, bis er geschlossen wird
        if result == QDialog.Accepted:
            return self.line_edit.text()
        else:
            return None

    def sizeHint(self):
        # Dynamische Größenanpassung basierend auf der Länge des Test_folgennamens
        font_metrics = self.line_edit.fontMetrics()
        text_width = font_metrics.boundingRect(self.line_edit.text()).width()
        return QSize(max(text_width + 150, 400), 150)


def get_application_instance():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

def makethemagic(path, folder_name, AnimeType, Animename, Gruppe, inhalt):
    app = get_application_instance(app)
    rename_dialog = RenameDialog()
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
                    neue_folge_pfad = os.path.join(path, rename_dialog.get_new_name(neue_folge_name))
                    os.rename(folge_pfad, neue_folge_pfad)
                else:
                    try:
                        os.rename(folge_pfad, neue_folge_pfad)
                    except OSError as e:
                        QMessageBox.critical(None, "Fehler beim Umbenennen", f"Fehler beim Umbenennen von {folge}: {e.strerror}")


def simulate_rename_dialog(Test_folgen):
    app = get_application_instance()
    rename_dialog = RenameDialog()
    print(rename_dialog.get_new_name(Test_folgen))


if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\Test\Demon.Slayer.Kimetsu"
    Animename = {'Demon.Slayer.Kimetsu.S01E01': ['namedjhfiojdkljkldjckljmckldjkljfkdjklcmkldmckldmckldmckldmckldmckldmckldmkldmkdmckld', '04'], 'Demon.Slayer.Kimetsu.S01E05.mkv': ['Demon.Slayer.Kimetsu 3', '06']}
    sourcelist = ['.mp4', '.mov', '.avi', '.mkv']
    AnimeType = ('S01', '')
    Gruppe = "test"
    inhalt = "Dämon"
    Test_folgen = "namedjhfiojdkljkldjckljmckldjkljfkdjklcmkldmckldmckldmckldmckldmckldmckldmkldmkdmckld.S0104test.mkv"
    folder_name = 'Demon.Slayer.Kimetsu 3'
    folgen = ["Demon.Slayer.Kimetsu.S01E01","Demon.Slayer.Kimetsu.S01E02.mkv","Demon.Slayer.Kimetsu.S01E05.mkv"]  # Setze hier den Standardnamen ein
    simulate_rename_dialog(Test_folgen)