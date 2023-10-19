import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import pyqtSignal
from app import app
from style import apply_dark_theme

apply_dark_theme(app)

class FolderNameGUI(QWidget):
    ok_clicked = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self, inhalt, app):
        super().__init__()
        self.setWindowTitle("Ordnerbenennung")
        layout = QVBoxLayout()
        label = QLabel("Ordnername eingeben:")
        layout.addWidget(label)
        self.entry = QLineEdit(inhalt)
        self.entry.setStyleSheet("background-color: #f0f0f0; color: black;")  # Hintergrundfarbe und Textfarbe ändern
        layout.addWidget(self.entry)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("background-color: blue; color: white; font-weight: bold;")
        ok_button.clicked.connect(self.handle_button_click)  # app als Argument übergeben
        layout.addWidget(ok_button)
        self.setLayout(layout)
        self.new_folder_name = inhalt

    def handle_button_click(self):
        new_text = self.entry.text().strip()
        if new_text:
            self.new_folder_name = new_text
            self.ok_clicked.emit()
        else:
            QMessageBox.warning(self, "Eingabefehler", "Bitte geben Sie einen gültigen Ordnername ein.")

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def sizeHint(self):
        # Die Größe basierend auf dem aktuellen Textinhalt berechnen
        hint = super().sizeHint()
        text_width = self.fontMetrics().width(self.entry.text())
        hint.setWidth(max(hint.width(), text_width))
        return hint

def load_gui_and_get_folder_name(inhalt):
    app = QApplication.instance()
    if app is None:  # Wenn keine vorhanden ist, erstellen Sie eine neue
        app = QApplication([])
    gui = FolderNameGUI(inhalt, app)  # app als Argument übergeben
    gui.ok_clicked.connect(app.exit)
    gui.closed.connect(app.exit)
    gui.show()
    app.exec_()
    return gui.new_folder_name

SonderzeichenListe = ["/", "?", "*", "<", ">", "'", "|", ":"]

def Ordnername(inhalt):
    newOrdnerAnimename = load_gui_and_get_folder_name(inhalt)
    if not newOrdnerAnimename:
        raise ValueError("Ungültiger Ordnername: Der eingegebene Name ist leer.")

    for SonderZeichen in SonderzeichenListe:
        newOrdnerAnimename = newOrdnerAnimename.replace(SonderZeichen, "!" if SonderZeichen == "?" else "")

    return newOrdnerAnimename

if __name__ == "__main__":
    inhalt = "FFFFFdjhgiuodjfoidjofikpiodjficj.ffjfjjfjjf.fjfisjfiksoik-mkv"
    if not inhalt:
        print(f"Der angegebene Pfad '{inhalt}' existiert nicht.")
    else:
        result = Ordnername(inhalt)
        print(result)
